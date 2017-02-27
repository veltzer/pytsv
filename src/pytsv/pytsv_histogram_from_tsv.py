#!/usr/bin/python3

import logging
from collections import defaultdict

import click
import scipy.stats
from pypipegzip import pypipegzip

from api.catalog import StorageDetails, CatalogOpenMode
from api.catalog_factory import CatalogTypes, CatalogFactory

logging.basicConfig()
logger = logging.getLogger(__name__)


@click.command()
@click.option('--catalog-type', required=True, type=click.Choice(CatalogTypes.names_for_click()))
@click.option('--catalog-name', required=True, type=str)
@click.option('--input_file1', required=True, type=str)
@click.option('--input_file2', required=True, type=str)
@click.option('--output_file', required=True, type=str)
def main(catalog_type, catalog_name, input_file1, input_file2, output_file):
    """ compares two category, product, query files """
    sd = StorageDetails()
    sd.name = catalog_name
    catalog_type_member = CatalogTypes[catalog_type]
    catalog = CatalogFactory.create_catalog(catalog_type=catalog_type_member)
    catalog.open(sd, CatalogOpenMode.READ)
    counters1 = defaultdict(int)
    counters2 = defaultdict(int)
    for i, input_file in enumerate([input_file1, input_file2]):
        with pypipegzip.open(input_file, "rt") as input_file_handle:
            for line in input_file_handle:
                line = line.rstrip()
                parts = line.split("\t")
                if len(parts) == 4:
                    inc = int(parts[3])
                else:
                    inc = 4
                category_id = parts[0]
                if i == 0:
                    counters1[category_id] += inc
                if i == 1:
                    counters2[category_id] += inc
    all_keys = set(counters1.keys())
    all_keys.union(set(counters2.keys()))
    v1, v2 = [], []
    with open(output_file, "wt") as output_file_handle:
        for key in sorted(all_keys, key=lambda x: counters1[x], reverse=True):
            cat_name = catalog.category_name_from_category_id(key)
            print(",".join([key, cat_name, str(counters1[key]), str(counters2[key])]), file=output_file_handle)
            v1.append(int(counters1[key]))
            v2.append(int(counters2[key]))
    # calculate the correlation between the two vectors
    # print(numpy.correlate(v1, v2))
    print(scipy.stats.stats.pearsonr(v1, v2))


if __name__ == '__main__':
    main()
