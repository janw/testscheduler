from itertools import chain
from glob import iglob
from os import chdir
from testscheduler import application

BLACKLISTED_DIRS = ["__pycache__/"]


def get_testfiles():
    base_dir = application.config["TESTFILES_DIR"]

    chdir(base_dir)
    available_files = iglob("./**/test*.py", recursive=True)

    available_dirs = filter(
        lambda x: all((t not in x for t in BLACKLISTED_DIRS)),
        iglob("./**/", recursive=True),
    )

    return sorted(chain(available_files, available_dirs))


testfiles = get_testfiles()