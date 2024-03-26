import argparse
import csv
import logging
import os
import sys
import time

g_antibody_name = None
g_channel_name = None

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


# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


def main(path, level):
    logging.basicConfig(format='%(levelname)s: %(message)s', level=level)
    logging.info('path of csv file is ready')
    logging.debug('path of csv file: %s' % path)

    if '.csv' in path and os.path.isfile(path):
        logging.info('start analyzing the csv file: %s' % path)
        with open(path, newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
            cnt = 1
            row_cnt = sum(1 for f in data)
            csvfile.seek(0)
            data = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
            antibody = []
            result = [[0] * 13 for i in range(4)]
            offset = 5

            printProgressBar(0, row_cnt, prefix='Progress:', suffix='Complete', length=50)
            for row in data:
                printProgressBar(cnt, row_cnt, prefix='Progress:', suffix='Complete', length=50)
                if cnt == 1:
                    sample = row[0]
                    # print('sample:', sample)
                if cnt == 2:
                    antibody_name = ''
                    for i in range(len(row)):
                        if i % offset == 1:
                            antibody.append(row[i])
                            antibody_name += ('%5s' % row[i]) + ' '
                if cnt == 3:
                    channel_name = ''
                    for i in range(4):
                        channel_name += ('%5s' % row[i + 1]) + ' '
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
        return antibody_name, channel_name
    else:
        logging.error('invalid path!')
        return None, None


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Tool is run in normal mode')
        print('----------------------------------------\n' +
              'normal mode arguments:\n' +
              '<your path>    set the path of csv file\n' +
              'help           show command list\n' +
              'info           show antibody and channel\n' +
              'exit           exit program\n' +
              '----------------------------------------')
        while True:
            print('')
            command = input()
            if command == 'exit':
                exit()
            elif command == 'info':
                if g_antibody_name is not None and g_channel_name is not None:
                    print('antibody: ', g_antibody_name)
                    print('channel : ', g_channel_name)
                else:
                    print('Please enter the path of csv file first')
            elif command == 'help':
                print('----------------------------------------\n' +
                      'normal mode arguments:\n' +
                      '<your path>    set the path of csv file\n' +
                      'help           show command list\n' +
                      'info           show antibody and channel\n' +
                      'exit           exit program\n' +
                      '----------------------------------------')
            else:
                g_antibody_name, g_channel_name = main(command, logging.INFO)
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
