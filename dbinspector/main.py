# -*- coding: utf-8 -*-
import sys
import yaml
import os
import subprocess
import pkg_resources
import argparse



from dbinspector.db_inspector import PgDbInspector

__db_schema_dot = "dbschema.dot"
__db_schema = "dbschema"

def parse_arg(args):
    # parse arguments
    parser = argparse.ArgumentParser(description='Visualize a relational database Schema')
    parser.add_argument('-u', '--url', action='store', help=
        '''the URL of the database, something looks like `postgresql://<dbuser>:<dbpass>@localhost:5432/<db>`.        
        This argument replace the parameter `dbUrl` in the configuration file.''')

    parser.add_argument('-o', '--output', action='store', help=
        '''the output directory, where generated files are saved.        
        This option replaces the parameter `outputDir` in configuration file.''')

    parser.add_argument('-f', '--format', action='store', help=
        '''the format type of generated graphic, which the Package GraphViz supports. Some of them are
        'pdf', 'png', 'svg'. More information here: http://www.graphviz.org/doc/info/output.html         
         This option replaces the configuration parameter `formatType` in the 
        configuration file.''')

    parser.add_argument('-c', '--config', action='store', help=
    '''the configuration file, if not provided the default configuration are used.''')

    parser.add_argument('-p', '--print-template', action='store_true', dest='print_t', help=
    '''print the default configuration file and quit.''')

    parsed_args = parser.parse_args(args)

    if parsed_args.print_t:
        print ( pkg_resources.resource_string(__name__, 'config.yaml' ).decode('UTF-8') )
        sys.exit(0)

    if parsed_args.config:
        with open(parsed_args.config) as f:
            config = yaml.load(f)
    else:
        with pkg_resources.resource_stream(__name__, 'config.yaml' ) as f:
            config = yaml.load(f)

    # check URL of database
    if parsed_args.url:
        config['dbUrl'] = parsed_args.url
    if not 'dbUrl' in config.keys():
        raise ValueError('The URL of Database must be configurated by option -u in command line or dbUrl in configuration file.')
    # check ouputDir
    if parsed_args.output:
        config['outputDir'] = parsed_args.output
    if not 'outputDir' in config.keys():
        config['outputDir'] = 'inspection-result'
    # check output format
    if parsed_args.format:
        config['formatType'] = parsed_args.format
    if not 'formatType' in config.keys():
        config['formatType'] = 'png'

    return config

def visual_db(config):
    """the common user's routine"""
    # inspect database
    db_url = config["dbUrl"].strip()
    inspector = PgDbInspector(db_url)

    db_graph = inspector.inspect()
    db_graph.apply_style(config)
    # make dot output
    outputDir = config["outputDir"]
    os.makedirs(outputDir, exist_ok=True)
    db_schema_file = os.path.join(outputDir, __db_schema_dot)
    with open(db_schema_file, "w") as db_schema:
        db_schema.write(db_graph.to_dot())

    # call dot
    print(config["formatType"])
    subprocess.run(["dot", "-T" + config["formatType"], "-o",
                    str(os.path.join(outputDir, __db_schema + "." + config["formatType"])),
                    str(db_schema_file)]
                   )
    pass


if __name__ == "__main__":
    """ Main Routine """
    config = parse_arg(sys.argv[1:])
    visual_db(config)