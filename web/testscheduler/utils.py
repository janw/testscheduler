from testscheduler import application

from os.path import join, pathsep
from glob import iglob


def get_testfiles():
    base_dir = application.config["TESTFILES_DIR"]
    prefix_len = len(base_dir) + len(pathsep)
    available_files = iglob(join(base_dir, "**/test*.py"), recursive=True)
    unprefixed_files = map(lambda x: x[prefix_len:], available_files)

    return sorted(unprefixed_files)
