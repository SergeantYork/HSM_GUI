import os
import sys
import platform

from my_operation_window import OperationWindow

PATH = os.path.dirname(os.path.realpath(__file__))
WIDTH = 1200
HEIGHT = 800


def create_and_start_collecting_to_log_file():

    # initialize and append log file
    f = open("log_file.txt", 'a')
    f.write("log file:")
    f.close()

    check_os = platform.system()
    if check_os == 'Windows':
        # insert same method for windows
        print("you need to solve this windows")

    if check_os == 'Linux':
        # open our log file
        se = so = open("log_file.txt", 'w')

        # re-open stdout without buffering
        sys.stdout = os.fdopen(sys.stdout.fileno(), 'w')
        # redirect stdout and stderr to the log file opened above
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())


def main():
    create_and_start_collecting_to_log_file()

    operation_window = OperationWindow()
    operation_window.mainloop()


if __name__ == "__main__":
    main()
