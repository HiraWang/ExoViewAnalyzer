import os, sys, csv, argparse, logging

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
def main(path, log_level):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)
    logging.info('path of csv file is ready')
    logging.debug("path of csv file: %s" % path)

    if '/' in path and os.path.isfile(path):
        logging.info('start analyzing the csv file: %s' % path)
        with open(path, newline='') as csvfile:
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
                    # print('antibody:')
                    antibody_name = ''
                    for i in range(len(row)):
                        if i % offset == 1:
                            antibody.append(row[i])
                            antibody_name += row[i] + ' '
                    # print(antibody_name)
                # if cnt == 3:
                #     print('channel:')
                #     print(row[1], row[2], row[3], row[4])

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

        result_name = str(path.split('.csv')[0]) + "_result.csv"
        logging.info('start organizing the result %s' % result_name)
        fp = open(result_name, "w")
        for i in range(len(result)):
            fp.write(antibody[i])
            for j in range(len(result[i])):
                fp.write(',' + RESULT_ATTRIBUTE[j] + ',' + str(result[i][j]) + '\n')
        fp.close()
    else:
        logging.info('invalid path!')


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Tool is run in normal mode')
        while True:
            print('Please enter the path of csv file')
            command = input()
            if command != 'exit':
                main(command, logging.INFO)
            else:
                exit()
    else:
        print('Tool is run in cmd line mode')
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "path",
            help="path of csv file")
        parser.add_argument(
            "-v",
            "--verbose",
            help="increase output verbosity",
            dest="verbose",
            action="store_true")

        args = parser.parse_args()
        print("positional arg:", args.path)
        print("optional   arg:", args.verbose)

        # Setup logging
        if args.verbose:
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO

        main(args.path, log_level)
