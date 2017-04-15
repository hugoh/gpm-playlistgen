#!/usr/bin/python

import argparse
import logging
import yaml
import sys
from gpmap.gpmap import GPMAP

def build_argparser():
    parser = argparse.ArgumentParser(description='Create playlists automatically.')
    parser.add_argument('config', type=file, help='Config file')
    parser.add_argument('--dry-run', action='store_true', help="Don't do any actual changes")
    parser.add_argument('--delete-all-playlists', action='store_true', help="Delete all generated playlists and exit immediately")
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
    cfg['dry-run'] = args.dry_run

    gpmap = GPMAP(cfg['auth']['user'], cfg['auth']['passwd'],
                  cfg['prefix'], debug_level,
                  library_cache=get_cache_path(cfg, 'libraryCache'),
                  db_cache=get_cache_path(cfg, 'dbFile'), dry_run=cfg['dry-run'])
    if args.delete_all_playlists:
        gpmap.cleanup_all_generated_playlists()
        sys.exit(0)
    gpmap.get_library()
    for playlist in cfg['playlists'].keys():
        gpmap.generate_playlist(playlist, cfg['playlists'][playlist])
