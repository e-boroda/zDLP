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
#   zDLP file extractor.py
#
#

import os.path
import tempfile
import textract
from json.decoder import JSONDecodeError
from zipfile import BadZipFile
from xlrd.biffh import XLRDError
from pptx.exc import PackageNotFoundError
from unrar import rarfile
import lib.util as util
import config as cfg
from . import logger

log = logger.get_logger(__name__)


class AbstractExtractor:
    """
    Abstract extractor for text info from different objects
    """
    def __init__(self, path, root, protocol='file', passwd=None):
        self.protocol = protocol
        # self.root = root
        self.path = path
        self.passwd = passwd

    def extract(self):
        raise NotImplemented


class Extractor:
    """Extract text info from files with textract framework"""

    def __init__(self, path, protocol, passwd=None):
        self.protocol = protocol
        # self.root = root
        self.path = path
        self.passwd = passwd
        self.container_status = cfg.STATUS_ERR
        self.container_message = ''

    def clean_data(self):
        log.debug("==>Cleaning object data")
        self.container_status = cfg.STATUS_ERR
        self.container_message = ''

    def add_message(self, msg):
        self.container_message += msg

    def extract(self, in_recursion=False):
        if not in_recursion:
            self.clean_data()
        if self.protocol == 'file':
            return self.extract_text()
        elif self.protocol == 'rar':
            return self.extract_rar()
        elif self.protocol == 'zip':
            return self.extract_zip()
        else:
            raise ValueError('Unknown protocol')

    def extract_text(self):
        try:
            log.debug(f"==>Textracting from: {self.path}")
            txt = textract.process(self.path, encoding='utf_8', language='rus')
            return cfg.STATUS_PROC, str(txt, 'utf-8')
        except TypeError as err:  # fail to proc some pdf types by default behaviour
            log.debug(f"==>Textract: {self.path} TypeError:{str(err)}")
            return cfg.STATUS_ERR, f"TypeError in extract:{str(err)}"
        except UnicodeDecodeError as err:
            log.debug(f"==>Textract {self.path} UnicodeDecodeError:{str(err)}")
            return cfg.STATUS_ERR, f"UnicodeDecodeError in extract:{str(err)}"
        except textract.exceptions.ShellError as se:
            return (cfg.STATUS_ERR, f"ShellError in extract:{str(se)}")
        except textract.exceptions.MissingFileError as mfe:
            return (cfg.STATUS_ERR, f"MissingFileError in extract:{str(mfe)}")
        except JSONDecodeError as jde:
            return (cfg.STATUS_ERR, f"JSONDecodeError in extract:{str(jde)}")
        except BadZipFile as bzf:
            return (cfg.STATUS_ERR, f"BadZipFile in extract:{str(bzf)}")
        except XLRDError as xlrde:
            return (cfg.STATUS_ERR, f"XLRDError in extract:{str(xlrde)}")
        except ValueError as err:
            log.debug(f"==>Textract:{self.path} ValueError:{str(err)}")
            return cfg.STATUS_ERR, f"ValueError in extract:{str(err)}"
        except AttributeError as err:
            log.debug(f"==>Textract:{self.path} AttributeError:{str(err)}")
            return cfg.STATUS_ERR, f"AttributeError in extract:{str(err)}"
        except PermissionError as err:
            log.debug(f"==>Textract:{self.path} PermissionError:{str(err)}")
            return cfg.STATUS_ERR, f"PermissionError in extract:{str(err)}"
        except PackageNotFoundError as err:
            log.debug(f"==>Textract:{self.path} PackageNotFoundError:{str(err)}")
            return cfg.STATUS_ERR, f"PackageNotFoundError in extract:{str(err)}"
        except RecursionError as err:
            log.debug(f"==>Textract:{self.path} RecursionError (maybe bs4 lib?):{str(err)}")
            return cfg.STATUS_ERR, f"RecursionError in extract (maybe bs4 lib?):{str(err)}"
        except MemoryError as err:
            log.debug(f"==>Textract:{self.path} MemoryError:{str(err)}")
            return cfg.STATUS_ERR, f"MemoryError in extract:{str(err)}"



    def extract_zip(self):
        return cfg.STATUS_ERR, "==>extract_zip not implemented yet"

    def extract_rar(self):
        find_volnum = util.find_rar_volume_num(self.path)
        if find_volnum and find_volnum != 1:
            log.debug(f"==>Ignore volume {find_volnum}:{self.path}")
            return cfg.STATUS_PASS, 'ignore archive volume, process it different way'  # in extract_rar_volumes()
        log.debug(f"==>Opening rar:{self.path}")
        try:
            rar = util.open_rar(rarfile, self.path, self.passwd)
        except (RuntimeError, rarfile.BadRarFile) as err:  # if no password given, permissions denied or bad format
            #if str(err).startswith('Archive is encrypted'):
            return cfg.STATUS_ERR, str(err)

        with tempfile.TemporaryDirectory() as tmp_dir_name:
            log.debug(f"==>Use:{tmp_dir_name} as tmp dir")
            try:
                util.extract_rar_volumes(rar, tmp_dir_name)  # if find them, except 1st
            except rarfile.BadRarFile as err:
                msg = f"==>Can't extract volumes for:{self.path} to {tmp_dir_name}\nBadRarFile:{str(err)}"
                self.add_message(msg)
                log.debug(msg)

            for entry in rar.infolist():
                if entry.flag_bits == 32:  # dir entry
                    log.debug(f"==>Pass dir entry:{entry.filename}")
                    continue
                # file_path = entry.filename  # os.path.join(self.root, entry.filename)
                # file_path = entry.filename
                file_ext = os.path.splitext(entry.filename)[1].lower()
                log.debug(f"==>List rar entry: {entry.filename}")
                if file_ext in cfg.FILE_EXTENTIONS:
                    # file_path = os.path.join(self.path, entry.filename)
                    # file_ext = os.path.splitext(file_path)[1].lower()
                    tmp_path_name = os.path.join(tmp_dir_name, entry.filename)
                    log.debug(f"==>Extracting file:{entry.filename} to {tmp_dir_name}")
                    try:
                        util.extract_rar(rar, entry, tmp_dir_name)
                    except rarfile.BadRarFile as err:
                        msg = f"==>Can't extract:{entry.filename} to {tmp_dir_name}\nBadRarFile:{str(err)}"
                        self.add_message(msg)
                        log.debug(msg)
                        continue
                    except ValueError as err:
                        msg = f"==>Can't extract:{entry.filename} to {tmp_dir_name}\nValueError:{str(err)}"
                        self.add_message(msg)
                        log.debug(msg)
                        continue
                    store_path, self.path = self.path, tmp_path_name
                    status, message = self.extract_text()
                    if status == cfg.STATUS_PROC:
                        self.container_status = cfg.STATUS_PROC
                    msg = f'==>Textract:{os.path.join(store_path, entry.filename)}\n{message}\n'
                    self.add_message(msg)
                    log.debug(f'==>Textract:{tmp_path_name}\n{message}\n')
                    self.path = store_path
                elif file_ext in cfg.CONTAINERS:
                    log.debug(f"==>Extract container:{entry.filename} to {tmp_dir_name}")
                    try:
                        util.extract_rar(rar, entry, tmp_dir_name)
                    except rarfile.BadRarFile as err:
                        msg = f"==>Can't extract:{os.path.join(self.path, entry.filename)}\nBadRarFile:{str(err)}"
                        self.add_message(msg)
                        log.debug(f"==>Can't extract:{entry.filename} to {tmp_dir_name}\nBadRarFile:{str(err)}")
                        continue
                    tmp_path_name = os.path.join(tmp_dir_name, entry.filename)
                    store_protocol, self.protocol = self.protocol, util.dedot(file_ext)  # set protocol to current container type
                    store_path, self.path = self.path, tmp_path_name
                    log.debug(f"==>Proc container:{self.path}")
                    self.extract(in_recursion=True)
                    self.protocol = store_protocol
                    self.path = store_path
        return self.container_status if self.container_message != '' else cfg.STATUS_OK, self.container_message
        #return self.container_status, self.container_message
