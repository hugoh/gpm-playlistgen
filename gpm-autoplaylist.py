#!/usr/bin/python

import argparse
import logging
import yaml
from gpmap.gpmap import GPMAP

def build_argparser():
    parser = argparse.ArgumentParser(description='Create playlists automatically.')
    parser.add_argument('config', type=file, help='Config file')
    parser.add_argument('--pl-prefix', action='store', default='[GPMAP]',
                        help='prefix for playlists created')
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
    try:
        if cfg['dev']['debug'] == True:
            debug_level = logging.DEBUG
    except:
        debug_level = logging.INFO
    gpmap = GPMAP(args.pl_prefix, debug_level,
                  library_cache=get_cache_path(cfg, 'libraryCache'),
                  db_cache=get_cache_path(cfg, 'dbFile'))
    #gpmap.login(cfg['auth']['user'], cfg['auth']['passwd'])
    gpmap.get_library()
    for playlist in cfg['playlists'].keys():
        gpmap.generate_playlist(playlist, cfg['playlists'][playlist])
