import argparse
import hashlib
from concurrent.futures import ThreadPoolExecutor
from os import makedirs, remove
from os.path import exists
from threading import Lock

from wheel.util import log

from path_filter import file_filter

FILE_HASH = set()
REMOVED = 0
COUNT = 0
HASH_LOCK = Lock()
FILE_LOCK = Lock()
COUNT_LOCK = Lock()


def calc_hash(file_path: str, tag: str = 'MD5') -> str:
    with open(file_path, 'rb') as f:
        return hashlib.new(tag, f.read()).hexdigest()


def check_dir(dir_path):
    """如果目录不存在则创建"""
    if not exists(dir_path):
        makedirs(dir_path)


def worker(file_path: str):
    global FILE_HASH, REMOVED, COUNT
    hash_value = calc_hash(file_path)

    file_existed = False

    with HASH_LOCK:
        if hash_value not in FILE_HASH:
            FILE_HASH.add(hash_value)

        else:
            file_existed = True

    if file_existed:
        try:
            remove(file_path)
            with FILE_LOCK:
                REMOVED += 1
                log.info(f"NO.{REMOVED}: 文件删除成功：{file_path}")

        except Exception as err:
            log.error(f'文件删除失败: {file_path} | error: {err}')

    with COUNT_LOCK:
        COUNT += 1

        if COUNT % 10 == 0:
            log.info(f"COUNT: {COUNT}")


def work(file_dir: str, worker_number: int):
    with ThreadPoolExecutor(worker_number) as pool:
        for i in file_filter(file_dir, 7):
            pool.submit(worker, i)


def cli():
    parser = argparse.ArgumentParser(description='Demo: python3 run.py d:/test_dir')
    parser.add_argument('dir_path', metavar='dir_path', help="需要去重的文件所在目录的全路径")

    # 解析命令
    args = parser.parse_args()
    return args.dir_path


def main():
    threads = 6
    work(cli(), threads)


if __name__ == '__main__':
    main()
