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
#   zDLP file util.py
#
#

import os
import tempfile
import datetime
import re
from unrar import rarfile
import config as cfg
# from lib.finder import Finder
from . import logger

log = logger.get_logger(__name__)


def esc(string):
    """
    Escape strings for SQLite queries
    """
    return string.replace("'", "''")


def get_datetime_from_timestamp(timestamp, fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.fromtimestamp(timestamp).strftime(fmt)


def get_tmp_name(schema='temp'):
    schema = cfg.TMP_DB_SCHEMA
    return ".".join((schema, 'obj_')) + next(tempfile._get_candidate_names())


def dedot(name: str):
    return name[1:] if name.startswith('.') else name


def get_file_protocols():
    return {'file'}.update([dedot(ext) for ext in cfg.CONTAINERS])


def read_file(path, block_size=cfg.BLOCK_SIZE):
    with open(path, 'rb') as f:
        while True:
            block = f.read(block_size)
            if block:
                yield block
            else:
                return


def get_remote_file(server, remote_path_name, local_path_name):
    with open(local_path_name, 'wb') as f:
        for block in server.read_file(remote_path_name):
            f.write(block)


def list_files(root):
    for entry in os.scandir(root):
        name = entry.name
        ftype = 'd' if entry.is_dir() else 'f'
        stat = entry.stat()
        mtime = get_datetime_from_timestamp(stat.st_mtime)
        yield ftype, mtime, name


def open_rar(rarfile_module: rarfile, path, passwd=None):
    """
    Open rar archive using unrar module,
    also realise smart behaviour - apply a list of predefined passwords to encrypted rar archive
    if passwd param is not set. Look at DEFAULT_ARC_PASSWORDS in configuration.
    :param rarfile_module: unrar.rarfile module instance
    :param path: path to rar file (string)
    :param passwd: password string
    :return: unrar.rarfile.RarFile() instance (rar handle)
    """
    try:
        return rarfile_module.RarFile(path, pwd=passwd)
    except RuntimeError as err:  # if no password given
        if str(err).find('Archive is encrypted') != -1:
            for passwd in cfg.DEFAULT_ARC_PASSWORDS:  # TODO - store passwords encrypted in db
                try:
                    return rarfile_module.RarFile(path, pwd=passwd)
                except rarfile_module.BadRarFile as e:  # Bad password
                    continue
            raise err



def extract_rar(rar: rarfile.RarFile, rar_entry: rarfile.RarInfo, tmp_dir_name, passwd=None):
    """
    Extract rar entry from archive using unrar module,
    also realise smart behaviour - apply a list of predefined passwords to encrypted rar entry
    if passwd param is not set. Look at DEFAULT_ARC_PASSWORDS in configuration.
    :param rar: unrar.rarfile.RarFile instance
    :param rar_entry: unrar.rarfile.RarInfo instance
    :param tmp_dir_name: path to tmp dir (string)
    :param passwd: password string
    :return: Nothing
    """
    try:
        rar.extract(rar_entry.filename, tmp_dir_name, pwd=passwd)
        log.debug(f"===>Extracted:{rar_entry.filename} to {tmp_dir_name} without pwd")
        return
    except (rarfile.BadRarFile, RuntimeError) as err:  # Only if no password given
        log.debug(f"===>Can't extract:{rar_entry.filename} to {tmp_dir_name} without pwd: {str(err)}")
        if str(err).startswith('Bad header data') or \
            str(err).startswith('File is encrypted'):  # may be file is encrypted
            for passwd in cfg.DEFAULT_ARC_PASSWORDS:  # TODO - store passwords encrypted in db
                try:
                    rar.extract(rar_entry.filename, tmp_dir_name, pwd=passwd)
                    log.debug(f"===>Extracted:{rar_entry.filename} to {tmp_dir_name} with pwd")
                    return
                except (rarfile.BadRarFile, RuntimeError) as e:  # Bad password
                    log.debug(f"===>Can't extract:{rar_entry.filename} to {tmp_dir_name} with pwd: {str(e)}")
                    continue
            raise err


def find_rar_volume_num(path: str):
    for regexp in cfg.CONTAINER_VOLUMES['rar']:
        result = re.search(regexp, path, re.IGNORECASE)  # extract volume number
        if result:
            n = int(result.group(1))
            log.debug(f"===>Detect:{path} as volume {n}")
            return n if re.search('part', regexp) else n+1  # aligns numbers in new & old rar volumes numeration


def extract_rar_volumes(rar: rarfile.RarFile, tmp_dir_name):
    volumes = list()
    for entry in rar.infolist():
        num = find_rar_volume_num(entry.filename)
        if num:  # find any volume
            if num == 1:  # main volume
                log.debug(f'===>Pass main volume:{entry.filename}, would be extracted later, tmp={tmp_dir_name}')
                continue
            else:
                log.debug(f'===>Extracting volume:{entry.filename} to {tmp_dir_name}')
                extract_rar(rar, entry, tmp_dir_name)
                volumes.append(entry)
    for entry in volumes:
        log.debug(f"===>Delete:{entry.filename} from file list")
        if entry.filename in rar.NameToInfo:
            del rar.NameToInfo[entry.filename]
        del rar.filelist[rar.filelist.index(entry)]
    # log.debug(rar.printdir()) - broken output

