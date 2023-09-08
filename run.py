import hashlib
from os import makedirs
from os.path import dirname, exists, join as path_join
from shutil import move
import argparse

from path_filter import file_filter


def calc_hash(file_path: str, tag: str = 'MD5') -> str:
    with open(file_path, 'rb') as f:
        return hashlib.new(tag, f.read()).hexdigest()


def check_dir(dir_path):
    """如果目录不存在则创建"""
    if not exists(dir_path):
        makedirs(dir_path)


def work(file_dir: str):
    to_dir = path_join(dirname(file_dir), "backup")
    check_dir(to_dir)

    total, moved = 0, 0
    file_hash = set()

    print("Parsing ...")
    for i in file_filter(file_dir, 5):
        total += 1
        hash_value = calc_hash(i)

        if hash_value not in file_hash:
            file_hash.add(hash_value)

        else:
            move(i, to_dir)
            moved += 1

        if total % 100 == 0:
            print(f"[Moved/total: {moved}/{total}]")
    print(f"[Moved/total: {moved}/{total}]")


def cli():
    parser = argparse.ArgumentParser(description='Demo: python3 run.py d:/test_dir')
    parser.add_argument('dir_path', metavar='dir_path', help="需要去重的文件所在目录的全路径")

    # 解析命令
    args = parser.parse_args()
    return args.dir_path


def main():
    work(cli())


if __name__ == '__main__':
    main()
