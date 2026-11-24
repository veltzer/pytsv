# TOFIX

Findings from a code scan on 2026-10-04.

## High

- `src/pytsv/core.py:234` - `TsvWriter.write` does `self.io.write(buf.encode())` on a file opened in text mode (`mode="wt"`, line 144), so every write raises `TypeError: write() argument must be str, not bytes`; it also never writes a line terminator (the old `print(...)` at line 235 did). Every endpoint that produces TSV output is broken. Write `buf + "\n"` as str, and add a TsvWriter round-trip test (`tests/unit_tests/test_all.py` only exercises TsvReader).
- `src/pytsv/core.py:165-166` - for `*.tsv.gz` names (and `do_gzip=True`, line 180) the handle is stored in `self.io_gzip`, but `write()`/`close()` (lines 234, 238) use `self.io`, so gzip output fails with `AttributeError`; store it in `self.io`.
- `src/pytsv/core.py:95` - `itertools.chain(m, aggregates)` iterates the joined key string `m` character by character, so `aggregate` writes one column per character of the key; use `[m, *aggregates]` (or the original match fields).
- `src/pytsv/main.py:185` - `clean_by_field_num` compares `len(fields) == ConfigColumns.columns` (an int against a list), which is always false, so the output is always empty; take an int (e.g. `ConfigNumFields.num_fields`) and compare against that.
- `src/pytsv/main.py:324` - `majority` picks `max(p_dict.keys())`, the largest second-column value, not the one with the highest accumulated count the docstring (lines 305-308) describes; use `max(p_dict, key=p_dict.get)`.
- `src/pytsv/main.py:655-680` - `sample_by_column` reads `ConfigWeightValue`, `ConfigSampleSize` and `ConfigReplace` but registers only `ConfigInputFile`, `ConfigOutputFile`, `ConfigCheckUnique` (lines 650-652), so those options cannot be set from the command line; same in `sample_by_two_columns` (lines 764-780 use `ConfigWeightValue`, `ConfigCheckUnique`, `ConfigSampleSize`, `ConfigReplace`, none registered at lines 749-752). Add the configs to the decorators.
- `src/pytsv/main.py:708` - `sample_by_column_old` reads `ConfigSampleByColumnOld.sample_column`, which does not exist (`src/pytsv/configs.py:267-273` only defines `hits_mode`; the column lives in `ConfigSampleColumn`), so it raises `AttributeError`; it also uses unregistered `ConfigSampleSize`/`ConfigReplace` (lines 720, 723). Register the right configs.
- `src/pytsv/main.py:815` - `split_by_columns` formats `ConfigPattern.pattern` with only `key=`, but the default pattern is `"{key}_{i:04d}.tsv.gz"` (`src/pytsv/configs.py:306`), so it fails with `KeyError: 'i'`; pass `i` or use `final_pattern`.

## Medium

- `src/pytsv/main.py:568-573` - `split_by_columns_parallel` never merges the per-job files into the final ones: it only creates an empty file per key and the merge is commented out; implement the concatenation (and delete the intermediates) or remove the endpoint.
- `src/pytsv/main.py:113-136` - with `--parallel`, `check` validates all files in the process pool and then falls through and checks them all again sequentially; put the sequential loop in an `else`.
- `src/pytsv/core.py:132` - `group_by` returns `[output_file_template.format(m=m) for match in all_data]`, which repeats the last key's filename for every entry; use `format(m=match)`.
- `src/pytsv/main.py:224` - `drop_duplicates_by_columns` keys on a `frozenset` of the values, so rows `(a, b)` and `(b, a)` (or `(a, a)` vs `(a,)`) are treated as duplicates; use a `tuple`. Its description (line 209) is copied from `fix_columns` and is wrong too.
- `src/pytsv/main.py:530-532` / `src/pytsv/main.py:813-815` - field values go straight into output filenames, so a value with `/` or `..` writes outside the working directory or fails; sanitize the key before formatting the path.
- `doc/TODO.txt:5-9` - stale items: the package already uses pytconf (`src/pytsv/main.py:20`), has progress reporting, and the "move to pydmt" item is obsolete; prune the list to what is still open.

## Low

- `src/pytsv/main.py:527` - `logger.info("working on [{job_info.input_file}]")` lacks the `f` prefix, so it logs the literal braces.
- `pyproject.toml:15` - description reads "Pytsv is a the Swiss army knife" and disagrees with `config/project.lua:2`; fix the typo so both match.
- `src/pytsv/configs.py:203` - `bucket_number` help says "what column to histogram"; it is the number of buckets.
- `src/pytsv/core.py:296-297` - the non-ASCII assertion is repeated (already done at lines 287-288); and `core.py:191-192` re-checks `fields_to_clean is None` after it was just set. Remove the duplicates.
