import os
import hashlib
from datetime import datetime
import functools
from pathlib import Path
import utils

class VersionMaintainer:
    def __init__(self, versions_dir: str, silent_mode: bool):
        self.__versions_dir = versions_dir

        startup_log = None
        if not os.path.exists(self.__versions_dir):
            os.makedirs(self.__versions_dir)
            startup_log = f'Created directory {utils.format_text(self.__versions_dir)} for versions data storage'
        else:
            startup_log = f'Using directory {utils.format_text(self.__versions_dir)} for versions data storage'

        if not silent_mode:
            print(startup_log)
            self.__print_initial_log()
        
    def get_version_number(self, prefix: str) -> int:
        version_path = self.__get_path(prefix)

        if not os.path.exists(version_path):
            return 0

        return int(self.__get_version_number(utils.read_utf8(version_path).splitlines()))

    def bump_version_number(self, prefix: str) -> int:
        v = self.get_version_number(prefix) + 1

        version_path = self.__get_path(prefix)
        os.makedirs(os.path.dirname(version_path), exist_ok=True)

        with open(version_path, mode='w', encoding='utf8') as f:
            fprint = functools.partial(print, file=f)
            fprint(f'# {prefix}')
            fprint(f'# Updated: {datetime.utcnow().isoformat()} UTC')
            fprint(f'{v}')

        return v

    def __get_key(self, prefix: str) -> str:
        return hashlib.md5(prefix.encode()).hexdigest()

    def __get_path(self, prefix: str) -> str:
        key = self.__get_key(prefix)
        return os.path.join(self.__versions_dir, key[0], key[1:])

    def __print_initial_log(self) -> str:
        header_printed = False

        for z in Path(self.__versions_dir).rglob('*/*'):
            if not header_printed:
                header_printed = True
                print('Current versions:')
            splitted = utils.read_utf8(z).splitlines()
            version = self.__get_version_number(splitted)
            print(f'    {splitted[0][2:]}.{utils.format_text(version)}')
        
        print(f'All new jobs will start from {utils.format_text(0)} version.')

    def __get_version_number(self, lines: list[str]) -> int:
        return next(l for l in lines if not l.startswith('#'))
