#!/usr/bin/python

import argparse
import logging
import yaml
from gpmap.gpmap import GPMAP

def build_argparser():
    parser = argparse.ArgumentParser(description='Create playlists automatically.')
    parser.add_argument('config', type=file, help='Config file')
    return parser

def get_cache_path(cfg, cache_type):
    try:
        return cfg['dev'][cache_type]
    except:
        return None

if __name__ == '__main__':
    argparser = build_argparser()
    args = argparser.parse_args()
    cfg = yaml.load(args.config)
    debug_level = logging.INFO
    try:
        if cfg['dev']['debug'] == True:
            debug_level = logging.DEBUG
    except:
        pass
    gpmap = GPMAP(cfg['auth']['user'], cfg['auth']['passwd'],
                  cfg['prefix'], debug_level,
                  library_cache=get_cache_path(cfg, 'libraryCache'),
                  db_cache=get_cache_path(cfg, 'dbFile'))
    gpmap.get_library()
    gpmap.cleanup_previous_playlists()
    for playlist in cfg['playlists'].keys():
        gpmap.generate_playlist(playlist, cfg['playlists'][playlist])
