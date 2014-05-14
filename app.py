#!/usr/bin/python

import sys
import argparse
import os.path

from reader import Parser
from outputer import Outputer

args = None


if __name__=='__main__':
        """ Specialist function for validating the given filename for the input
        file from the command line. If the file exists and is readable, the
        file object is returned."""
        def is_valid_file(arg_parser, arg):
                if not os.path.exists(arg):
                        arg_parser.error('The file %s does not exist!'%arg)
                else:
                        return open(arg,'r')    #return an open file handle

        """ Initalise the command line argument parser to read in the user
        options."""
        arg_parser = argparse.ArgumentParser(
                description='Parse and xml file from the data archive into a format suitable for loading into Caddies.'
        )

        """ Add the input filename argument."""
        arg_parser.add_argument(
                '-i',
                dest='infilename',
                required=True,
                help='Input file to be parsed',
                metavar="FILE",
                type=lambda x: is_valid_file(arg_parser,x)
        )

        """ Add the output filename argument."""
        arg_parser.add_argument(
                '-o',
                dest='outfilename',
                required=False,
                help='Output file',
                metavar="FILE",
                default=""
        )

        """ Add the number of processes to be used in cleaning stage.
        DEPRECATED."""
        arg_parser.add_argument(
                '--processes',
                dest='np',
                required=False,
                help='Number of processes to be used for the cleaning stage',
                type=int,
                default=4
        )

        """ Add the flag to signal using all default answers to questions,
        without asking the user. Designed to be used in batch running."""
        arg_parser.add_argument(
                '--defaults',
                action='store_true',
                required=False,
                help='Use default values for every user decision (recommended for headless running)'
        )

        args = arg_parser.parse_args()

def main(_infile, _outfilename, _np=4, _defaults=False, _silent=False):

        #Initalise parser to read through xml file
        parser = Parser(_infile, _np, _defaults, _silent)

        parser.run()

        parser.output()

        parser.clean()

        parser.output()

        parser.separateInstructions()

        parser.validate()

        #Initalise outputer to write out the sql file from the data parsed by the parser
        outputer = Outputer(parser.getData(), _silent)

        """ Small piece of code to use input file name as the default output
        filename if no other filename was specified using '-o'."""
        if _outfilename == "":
                outfile = os.path.splitext(_infile.name)[0] + '.sql'
        else:
                outfile = _outfilename

        outputer.write(outfile)

        return 0

if __name__=='__main__':
    sys.exit(main(args.infilename, args.outfilename, args.np, args.defaults))
