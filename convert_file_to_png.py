from pathlib import Path
from os.path import basename
import os
from multiprocessing import Process
from threading import Thread
import numpy as np
import array
from math import ceil
from PIL import Image
import re


# 저장 위치
save_dir = 'C:\\Gather'


# hex를 이미지화 시켜주는 메소드
def bytes2png(f, width, compiler_version):

    undecodedByte = 'FF'

    file = f

    """
        Construct image name and return if file already exists
    """

    image_name = f.split('.')[0]
    image_buf = image_name.split('\\')
    image_name = image_buf[0] + '\\' + image_buf[1] + '\\' + compiler_version + '\\' + 'Images' + '\\' + image_buf[3] + '.png'

    if os.path.isfile(image_name):
        print('Image already exists: {}'.format(image_name))
        return

    # 이미지 저장 경로 설정
    # Images 폴더가 없으면 새로 생성
    if not os.path.exists(save_dir+'\\' + compiler_version + '\\Images'):
        os.mkdir(save_dir+'\\' + compiler_version + '\\Images')

    b_data = array.array('i')
    for line in open(file, 'r'):
        for byte in line.rstrip().split():
            # 각 라인마다 앞의 8개의 코드는 주소를 뜻하므로, 제외함.
            # 실제 데이터에서 가져올 때에는 주소 개념이 없음.

            # byte가 ??인 파트는 따로 처리하는 작업
            # 이 부분이 정확도에 크게 기여하는 곳이므로, 처리할 필요가 있음.
            if byte == '??':
                byte = undecodedByte

            # 간혹 byte 코드에 \\이라고 적힌 부분이 있어서 건너뛰어야 함.
            if byte.__contains__('\\'):
                continue

            b_data.append(int(byte, base=16))
            # 16진수 형태로 배열에 부착함

    i = 0
    while(True):
        print(i)
        i+=1
        if i*i <= len(b_data) and len(b_data) < (i+1)*(i+1):
            height = i+1
            width = i+1
            break

#    height = ceil(len(b_data) / width)
    if len(b_data) < (width * height):
        b_data += array.array('i', (0,) * (width * height - len(b_data)))
    image_buffer = np.fromiter(b_data, dtype=np.uint8).reshape((height, width))
    img = Image.fromarray(image_buffer, 'L')
    img.save(image_name)

    # list 폴더가 없다면 새로 생성
    if not os.path.exists(save_dir + '\\'+ compiler_version + '\\list'):
        os.mkdir(save_dir + '\\'+ compiler_version + '\\list')
    txtfile = save_dir + '\\'+ compiler_version + '\\list\\' + 'saveInstance.txt'

    with open(txtfile, mode='a+') as f:
        f.write(file.split('\\')[-1] + '\n')


# 리스트를 n개로 나누기
def chunkify(lst, n):
   return [lst[i::n] for i in range(n)]


# 파일을 읽어 데이터를 리스트로 반환
def read_file(file_path):
    try:
        data_list = []
        with open(file_path, mode="rb") as f:
            while True:
                buf = f.read(16)
                if not buf:
                    break
                else:
                    data_list.append(buf)

        return data_list

    except Exception as ex:
        print("[ERROR] : {0}".format(ex))
        raise Exception(ex) from ex


# data를 hex로 기록한 .txt파일 생성
def create_txt_file(file_name, data, compiler):

    file_path = save_dir + '\\' + compiler +'\\'+ file_name
    try:
        with open(file_path, mode="wb") as f:
            for i in data:
                f.write(b' '.join(['{:02x}'.format(int(x)).upper().encode() for x in list(i)]))
                f.write(b'\r\n')

            print("[생성 완료] {}".format(file_name))

    except Exception as e:
        print(e)

    return file_path


# 한 번에 여러 개의 hex file 만들기
def make_hex_files(list_of_file_path):
    for file_path in list_of_file_path:  # obj파일 리스트
        try:
            data_list = read_file(file_path)

            compiler = re.compile("gcc\d-O\d-x86_64").search(str(file_path))  # _64파일일때
            if compiler == None:
                compiler = re.compile("gcc\d-O\d-x86").search(str(file_path))  # _64파일일때
            compiler = compiler.group()  # 파일의 컴파일러 버전 추출

            create_txt_file(basename(file_path) + ".txt", data_list, compiler)
        except Exception:
            pass


# 여러개의 hex file들을 이미지로 변환
def make_img_files(list_of_file_path, compiler_version):
    for file_path in list_of_file_path:
        try:
            # bytes2png(file_path, 256, compiler_version)  # 사이즈별 이미지 크기를 같게

            # 사이즈별 이미지 크기를 다르게
            file_size = os.path.getsize(str(file_path))
            print(file_size)
            if (file_size < 10 * 1024):
                bytes2png(file_path, 32, compiler_version)
            elif (file_size < 30 * 1024):
                bytes2png(file_path, 64, compiler_version)
            elif (file_size < 60 * 1024):
                bytes2png(file_path, 128, compiler_version)
            elif (file_size < 100 * 1024):
                bytes2png(file_path, 256, compiler_version)
            elif (file_size < 200 * 1024):
                bytes2png(file_path, 384, compiler_version)
            elif (file_size < 500 * 1024):
                bytes2png(file_path, 512, compiler_version)
            elif (file_size < 1000 * 1024):
                bytes2png(file_path, 768, compiler_version)
            else:
                bytes2png(file_path, 1024, compiler_version)

        except Exception as e:
            raise e


# 멀티프로세싱 적용
# num_of_proc : 사용할 프로세스 개수
def file_to_hex_multiprocessing(file_path, file_ext, num_of_proc):

    """
    :param file_path: 파일이 있는 디렉토리 (주로 C:, D: 등 드라이브 디렉토리를 사용)
    :param file_ext: hex파일로 변환할 파일의 확장자명 (점 제외하고 입력)
    :param num_of_proc: (멀티프로세싱에 사용할 프로세스 개수)

    """

    '''
    hex파일로 변환
    '''
    lst = []

    dir_list = []
    compiler_list = []
    black_list = ["C:\\Windows", ]  # Windows 폴더는 변환 대상에서 제외

    # C:\\ 에 위치한 폴더들(black_list 제외)을 리스트에 추가
    for p in Path(file_path).glob("*"):
        if not(str(p) in black_list):
            dir_list.append(p)
            compiler = re.compile("gcc\d-O\d.*").search(str(p)).group()  # 컴파일러 버전 추출
            if compiler not in compiler_list:
                compiler_list.append(compiler)
    print("컴파일러 : ", compiler_list)
    # dir_list에 있는 폴더에 있는 파일들 모두 검색 (recursively)
    for d in dir_list:
        try:
            for path in Path(d).glob("**\\*"):
                try:
                    # 0.5KB < 파일크기 < 5MB 인 파일만 변환
                    if (0.01*1024) < os.path.getsize(str(path)) < (50*1024*1024):
                        if os.path.isfile(path) == True:
                            if str(path).split("\\")[-1].__contains__(".") == False:  # 실핼파일은 .이 없음
                                print(path)
                                lst.append(path)

                except OSError as e:
                    print(e)

        except FileNotFoundError as e:
            print(e)

    print("파일갯수 : ",len(lst))


    for f in compiler_list:  # 컴파일러 버전별 폴더생성
        if not os.path.exists(save_dir + "\\" + str(f)):
            os.mkdir(save_dir + "\\" + str(f))

    # 멀티프로세싱을 위한 task 나누기
    task_list = chunkify(lst, num_of_proc)

    processes = []  # 프로세스 객체를 담을 리스트

    print("Converting exe_file to hex_file...")

    # exe파일들을 hex로 변환한 파일 생성
    for task in task_list:
        process = Process(target=make_hex_files, args=(task, ))
        processes.append(process)
        process.start() # 프로세스 시작

    for proc in processes:
        proc.join()

    print("exe파일의 hex값 추출 완료")

    '''
    이미지로 변환
    '''


    for i in compiler_list:  # 버전으로 구분한 폴더별로 실행
        # 재사용을 위한 리스트 비우기
        processes.clear()
        lst.clear()
        task_list.clear()
        for p in Path(save_dir+'\\'+i).glob("*.txt"):
            lst.append(str(p))
        # 멀티프로세싱을 위한 task 나누기
        task_list = chunkify(lst, num_of_proc)
        print("이미지로 변환 시작")
        print("변환 중...")

        # hex파일들을 이미지로 변환한 파일 생성
        for task in task_list:
            process = Process(target=make_img_files, args=(task,i))
            processes.append(process)
            process.start()  # 프로세스 시작

        for proc in processes:
            proc.join()

        print(i, "이미지 변환 완료")
