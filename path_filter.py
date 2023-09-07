from os.path import splitext
from pathlib import Path


def file_filter(dir_path: str, depth: int = 0, suffix=None, key_str: str = None):
    """
    1) Generator。
    2) 遍历 dir_path 目录下的路径，返回文件路径。
    3) 注意：这里的路径使用'/'。
    :param dir_path:    str     要遍历的目录路径
    :param depth:       int     扫描的深度 0: 当前目录; 1: 当前目录的下一级目录，以此类推，数字每增加1，扫描深度加1
    :param suffix:      str     返回的路径中包含特定后缀，如 ".py" 或者 "py"，默认None，没有后缀限制
    :param key_str:     str     返回的路径中包含特定的关键词
    """

    # 设定当前目录的表示值
    current_dir_level = 0

    if suffix:
        suffix = ('.' + suffix) if not suffix.startswith('.') else suffix

    # _path 输出的是绝对路径
    for path in Path(dir_path).absolute().iterdir():
        tmp_path = str(path)

        if path.is_dir():
            if current_dir_level < depth:
                yield from file_filter(tmp_path, depth - 1, suffix, key_str)

        else:
            found = []
            if suffix:
                if splitext(tmp_path)[-1] == suffix:
                    found.append(True)
                else:
                    found.append(False)

            if key_str:
                if key_str in tmp_path:
                    found.append(True)
                else:
                    found.append(False)

            # 在加了suffix或key_str条件后，如果没有找到符合条件的路径，found会得到一个False(如，[False])
            # all: 所有值都为True时，返回True。即加了条件后，该条路径符合满足所有条件的需求，则返回True
            # 还有一点值得注意，all([])的值为True。即，当不加任何条件的时候，依然返回路径
            if all(found):
                yield tmp_path


def demo():
    test_path = './'
    depth = 0  # 当前目录
    suffix = ".py"  # 搜索后缀为".py"的文件
    key_str = '_'  # 并且路径中包含'_'
    res = file_filter(test_path, depth=depth)
    for i in res:
        print(i)


if __name__ == "__main__":
    demo()
