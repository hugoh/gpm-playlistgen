#!/usr/bin/python

import argparse
import yaml
import sys
from gpmplgen import *
import logging


def build_argparser():
    parser = argparse.ArgumentParser(description='Create playlists automatically.')
    parser.add_argument('config', type=file, help='Config file')
    parser.add_argument('--dry-run', action='store_true', help="Don't do any actual changes")
    parser.add_argument('--delete-all-playlists', action='store_true',
                        help="Delete all generated playlists and exit immediately")
    parser.add_argument('--force', action='store_true', help="Regenerate all playlists")
    return parser


def get_cache_path(cfg, cache_type):
    try:
        return cfg['dev'][cache_type]
    except KeyError:
        return None


if __name__ == '__main__':
    argparser = build_argparser()
    args = argparser.parse_args()
    cfg = yaml.load(args.config)
    debug_level = logging.INFO
    try:
        if cfg['dev']['debug']:
            debug_level = logging.DEBUG
    except KeyError:
        pass

    try:
        gpmplgen = GPMPlGen(cfg['auth']['user'], cfg['auth']['passwd'],
                            cfg['prefix'], debug_level,
                            library_cache=get_cache_path(cfg, 'libraryCache'),
                            db_cache=get_cache_path(cfg, 'dbFile'),
                            force=args.force, dry_run=args.dry_run)
        if args.delete_all_playlists:
            gpmplgen.get_library(get_songs=False)
            gpmplgen.cleanup_all_generated_playlists()
            sys.exit(0)
        gpmplgen.get_library()
        i = 0
        for playlist in cfg['playlists'].keys():
            i += 1
            gpmplgen.generate_playlist(playlist, cfg['playlists'][playlist])
        logging.info("Generated %d auto playlists" % i)
    except GPMPlGenException as e:
        logging.fatal(e)
        logging.fatal("Exiting...      :-(")
        sys.exit(1)
