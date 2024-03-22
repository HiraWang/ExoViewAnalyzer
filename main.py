import csv, argparse, logging

CSV_PATH = ''

COMMAND_ANALYZE = 'ana'


# Gather our code in a main() function
def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    logging.info("You passed an argument.")
    logging.debug("Your Argument: %s" % args.argument)

    if '/' in args.argument:
        print('start setting the csv path', args.argument)
        with open(args.argument, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                print(', '.join(row))

    if args.argument == COMMAND_ANALYZE:
        print('start analyzing the csv file')


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Does a thing to some stuff.",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')

    parser.add_argument(
        "argument",
        help="pass ARG to the program",
        metavar="ARG")
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")
    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)
