<%!
    import config.project
    import user.personal
    line = '=' * (len(config.project.project_name)+2)
%>${line}
*${config.project.project_name}*
${line}

![build](https://github.com/veltzer/${config.project.project_name}/workflows/build/badge.svg)
