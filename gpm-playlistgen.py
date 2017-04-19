#!/usr/bin/python

import argparse
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


if __name__ == '__main__':
    argparser = build_argparser()
    args = argparser.parse_args()

    cfg = Config()
    cfg.fromYaml(args.config)
    cfg.fromCli(args)

    try:
        gpmplgen = GPMPlGen(cfg)
        if cfg.delete_all_playlists:
            gpmplgen.get_library(get_songs=False)
            gpmplgen.cleanup_all_generated_playlists()
            sys.exit(0)
        gpmplgen.get_library()
        i = 0
        for playlist in cfg.playlists.keys():
            i += 1
            gpmplgen.generate_playlist(playlist, cfg.playlists[playlist])
        logging.info("Generated %d auto playlists" % i)
    except GPMPlGenException as e:
        logging.fatal(e)
        logging.fatal("Exiting...      :-(")
        sys.exit(1)
