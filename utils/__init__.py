"""
------------------------------------------
@File       : __init__.py
@CreatedOn  : 2023/2/25 11:09
------------------------------------------
"""
from os.path import dirname

from .logger import Logger

project_root_dir = dirname(dirname(__file__))
log = Logger(log_dir=f"{project_root_dir}/logs").log
