#!/usr/bin/env python
import sys
import argparse
import logging
import json
# sources
import abc
import cspan
import millercenter
import tapp

# each command should be a function from an argparse opts object to an iterable
# of standard speech dicts
commands = {
    'abc': lambda opts: (abc.fetch(page_url) for page_url in opts.args),
    'cspan': lambda opts: (cspan.fetch(program_id) for program_id in opts.args),
    'millercenter': lambda opts: millercenter.fetch_speeches(),
    'tapp': lambda opts: (tapp.fetch(pid) for pid in opts.args),
    'tapp-inaugurals': lambda opts: tapp.fetch_inaugurals(),
    'tapp-election2016': lambda opts: tapp.fetch_election2016(),
}

verbosity_levels = [logging.WARN, logging.INFO, logging.DEBUG, logging.NOTSET]

def main():
    parser = argparse.ArgumentParser(
        description='Scrape major news outlet articles',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', action='count', default=0,
        help='log extra information (repeat for even more, up to 3)')
    parser.add_argument('command', choices=commands, help='Command')
    parser.add_argument('args', nargs='*', help='arguments to command')
    opts = parser.parse_args()

    logging.basicConfig(level=verbosity_levels[opts.verbose])

    command = commands[opts.command]
    for obj in command(opts):
        sys.stdout.write(json.dumps(obj, sort_keys=True, ensure_ascii=False))
        sys.stdout.write('\n')
        sys.stdout.flush()

if __name__ == '__main__':
    main()