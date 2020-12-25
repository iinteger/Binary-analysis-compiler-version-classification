# main.c
from convert_file_to_png import file_to_hex_multiprocessing
from multiprocessing import freeze_support
from time import time

#save_dir = 'C:\\Gather\\'  # binutils
save_dir = 'C:\\Gather2\\'  # coreutils
undecodedByte = 'FF'

if __name__ == '__main__':

    freeze_support()

    #drive = "binutils\\"
    drive = "coreutils\\"

    try:
        start_time = time()

        file_to_hex_multiprocessing(drive, "o", 4)

        end_time = time()

        print("WorkingTime : {0:0.6f} sec\n".format(end_time - start_time))

        input("Press Enter key to exit...")

    except PermissionError as e:
        print(e)