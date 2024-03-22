import csv, argparse, logging

CSV_PATH = ''
RESULT_ATTRIBUTE = ['Total number of particles',
                    'IM>0 & (CD63>0 OR CD81>0)',
                    'IM>0 & (CD63>0 OR CD81>0) AND FITC>0',
                    'IM>0 & (CD63>0 OR CD81>0) AND FITC=0',
                    'IM>0 & (CD63=0 AND CD81=0)',
                    'IM>0 & (CD63=0 AND CD81=0) AND FITC>0',
                    'IM>0 & (CD63=0 AND CD81=0) AND FITC=0',
                    'IM=0 & (CD63>0 OR CD81>0)',
                    'IM=0 & (CD63>0 OR CD81>0) AND FITC>0',
                    'IM=0 & (CD63>0 OR CD81>0) AND FITC=0',
                    'IM=0 & (CD63=0 AND CD81=0)',
                    'IM=0 & (CD63=0 AND CD81=0) AND FITC>0',
                    'IM=0 & (CD63=0 AND CD81=0) AND FITC=0']


# Gather our code in a main() function
def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    logging.info("You passed an argument.")
    logging.debug("Your Argument: %s" % args.argument)

    if '/' in args.argument:
        print('start analyzing the csv file', args.argument)
        with open(args.argument, newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
            cnt = 1
            antibody = []
            result = [[0] * 13 for i in range(4)]
            offset = 5

            for row in data:
                if cnt == 1:
                    sample = row[0]
                    # print('sample:', sample)
                if cnt == 2:
                    print('antibody:')
                    antibody_name = ''
                    for i in range(len(row)):
                        if i % offset == 1:
                            antibody.append(row[i])
                            antibody_name += row[i] + ' '
                    print(antibody_name)
                if cnt == 3:
                    print('channel:')
                    print(row[1], row[2], row[3], row[4])

                if cnt >= 4:
                    for i in range(len(row) // 5):
                        # i: 0 1 2 3
                        # CD63 1, CD81 2, FITC 3, IM 4
                        if row[i * 5 + 1] == '':
                            continue
                        cd63 = int(row[i * 5 + 1])
                        cd81 = int(row[i * 5 + 2])
                        fitc = int(row[i * 5 + 3])
                        im = float(row[i * 5 + 4])

                        if row[i * 5 + 1] != '':
                            result[i][0] += 1
                        if im > 0 and (cd63 > 0 or cd81 > 0):
                            result[i][1] += 1
                            if fitc > 0:
                                result[i][2] += 1
                            if fitc == 0:
                                result[i][3] += 1
                        if im > 0 and (cd63 == 0 and cd81 == 0):
                            result[i][4] += 1
                            if fitc > 0:
                                result[i][5] += 1
                            if fitc == 0:
                                result[i][6] += 1
                        if im == 0 and (cd63 > 0 or cd81 > 0):
                            result[i][7] += 1
                            if fitc > 0:
                                result[i][8] += 1
                            if fitc == 0:
                                result[i][9] += 1
                        if im == 0 and (cd63 == 0 and cd81 == 0):
                            result[i][10] += 1
                            if fitc > 0:
                                result[i][11] += 1
                            if fitc == 0:
                                result[i][12] += 1
                    # print(cnt, result[0])
                cnt += 1

        result_name = str(args.argument.split('.csv')[0]) + "_result.csv"
        print('start organizing the result', result_name)
        fp = open(result_name, "w")
        for i in range(len(result)):
            fp.write(antibody[i])
            for j in range(len(result[i])):
                fp.write(',' + RESULT_ATTRIBUTE[j] + ',' + str(result[i][j]) + '\n')
        fp.close()


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
