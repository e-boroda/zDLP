#
#     Copyright  2020  Eugene Borodin (eugene.borodin at gmail.com)
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#    --------
#   zDLP file scanner.py
#
#

import os
import os.path
import sys
from datetime import datetime
import tempfile
from unrar import rarfile
import config as cfg
import lib.util as util
# import src.lib.zdb as db
# from lib.common import AbstractScanner, UnknownContainerType
#from lib.util import open_rar, dedot
from . import logger

log = logger.get_logger(__name__)


class Scanner:
    """
    Object paths scanner
    """
    def __init__(self, root=cfg.DEFAULT_SCAN_ROOT_PATH, host=cfg.HOST_NAME, protocol="file"):
        self.protocol = protocol
        self.host = host
        self.root = root
        self.n_obj_scanned = 0
        self.obj_list = list()
        # self.cache_dir = tempfile.TemporaryDirectory()
        # self.cache = list()

    def set_root(self, root):
        self.root = root

    def get_root(self):
        return self.root

    def set_host(self, host):
        self.host = host

    def get_host(self):
        return self.host

    def set_protocol(self, protocol):
        self.protocol = protocol

    def get_protocol(self):
        return self.protocol

    def get_n_obj_scanned(self):
        return self.n_obj_scanned

    def inc_n_obj_scanned(self):
        self.n_obj_scanned += 1

    def clean_data(self):
        self.n_obj_scanned = 0
        self.obj_list = list()

    def scan_file(self):
        for root, dirs, f_names in os.walk(self.root):
            # print('in os.walk:', root, dirs, f_names)
            for f_name in f_names:
                #print('in for:', root, f_name)
                file_path = os.path.join(root, f_name)
                file_ext = os.path.splitext(file_path)[1].lower()
                log.debug(f"=>{file_path}")
                if file_ext in cfg.FILE_EXTENTIONS:
                    try:
                        file_mtime = os.path.getmtime(file_path)
                        file_size = os.path.getsize(file_path)
                    except FileNotFoundError as err:
                        log.warning(f"Problems with {file_path}:{str(err)}")
                        continue
                    self.inc_n_obj_scanned()
                    self.obj_list.append((self.protocol, self.host, self.root, file_path, file_mtime, file_size))
                elif file_ext in cfg.CONTAINERS:
                    store_protocol = self.protocol
                    self.protocol = util.dedot(file_ext)
                    file_mtime = os.path.getmtime(file_path)
                    file_size = os.path.getsize(file_path)
                    self.inc_n_obj_scanned()
                    self.obj_list.append((self.protocol, self.host, self.root, file_path, file_mtime, file_size))
                    self.protocol= store_protocol
        return self.obj_list

    def scan_rar(self, in_recursion=False):
        rar = util.open_rar(rarfile, self.root)
        for entry in rar.infolist():
            if entry.flag_bits == 32:  # dir entry
                continue
            file_path = os.path.join(self.root, entry.filename)
            # file_path = entry.filename
            file_ext = os.path.splitext(file_path)[1].lower()
            log.debug(f"=>{file_path}")
            if file_ext in cfg.FILE_EXTENTIONS:
                # file_mtime = datetime(*entry.date_time).timestamp()  # TODO  entry.date_time can return 60 secs :[]
                file_mtime = 0.
                file_size = entry.file_size
                self.inc_n_obj_scanned()
                self.obj_list.append((self.protocol, self.host, self.root, file_path, file_mtime, file_size))
            elif file_ext in cfg.CONTAINERS:
                # file_mtime = datetime(*entry.date_time).timestamp()  # TODO  bug in unrar: entry.date_time can return 60 secs :[]
                file_mtime = 0.
                file_size = entry.file_size
                store_protocol = self.protocol
                self.protocol = util.dedot(file_ext)  # set protocol to current container type
                self.root = file_path
                self.inc_n_obj_scanned()
                self.obj_list.append((self.protocol, self.host, self.root, file_path, file_mtime, file_size))
                self.protocol = store_protocol
        return self.obj_list

    def scan(self, in_recursion=False):
        # in_recursion = (sys._getframe(0).f_code.co_name == sys._getframe(1).f_code.co_name)  # TODO - not work. especially from debugger
        if not in_recursion:
            self.clean_data()
        if self.protocol == "file":
            self.scan_file()
        elif self.protocol == "rar": # TODO realize containers scanner,
            # self.scan_rar(in_recursion=in_recursion)  # TODO ... archives scan
            pass
        elif self.protocol == 'oracle':
            pass  # TODO ... database scan
        return self.obj_list

    def unpack_container(self):
        if self.protocol == 'rar':
            util.unpack_rar()
        elif self.protocol == 'zip':
            util.unpack_zip()
        else:
            raise



if __name__ == '__main__':
    scanner = Scanner(sys.argv[1])
    path_list = scanner.scan()
    for (protocol, host, path, mtime, size) in path_list:
        print(protocol, host, datetime.fromtimestamp(mtime).strftime('%Y.%m.%d-%H:%M:%S'),
              round(size/1024, 2), 'K\t', path)
    print(f"Collect info for {scanner.get_n_obj_scanned()} files.")
    print(len(path_list))
