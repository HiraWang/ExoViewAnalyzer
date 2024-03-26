import argparse
import csv
import logging
import os
import sys
import time

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


def main(path, level):
    logging.basicConfig(format='%(levelname)s: %(message)s', level=level)
    logging.info('path of csv file is ready')
    logging.debug('path of csv file: %s' % path)

    if '.csv' in path and os.path.isfile(path):
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
        logging.info('start organizing the result:  %s' % result_name)
        fp = open(result_name, "w")
        for i in range(len(result)):
            fp.write(antibody[i])
            for j in range(len(result[i])):
                fp.write(',' + RESULT_ATTRIBUTE[j] + ',' + str(result[i][j]) + '\n')
                if j == 0:
                    print('%5s %s %5d' % (antibody[i], RESULT_ATTRIBUTE[j], result[i][j]))
        fp.close()
    else:
        logging.error('invalid path!')


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Tool is run in normal mode')
        print('---------------------------------------\n' +
              'normal mode arguments:\n' +
              '<your path>    set the path of csv file\n' +
              'help           show command list\n' +
              'exit           exit program\n' +
              '---------------------------------------')
        while True:
            print('Please enter the path of csv file')
            command = input()
            if command == 'exit':
                exit()
            elif command == 'help':
                print('---------------------------------------\n' +
                      'normal mode arguments:\n' +
                      '<your path>    set the path of csv file\n' +
                      'help           show command list\n' +
                      'exit           exit program\n' +
                      '---------------------------------------')
            else:
                main(command, logging.INFO)
                time.sleep(1)
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
