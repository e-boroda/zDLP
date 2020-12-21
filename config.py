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
#   zDLP file config.py
#
#

# main configurable params & constants
# import sys
# import os
import os.path
import platform
import socket
import re

assert os.name in ('posix', 'nt'), "Unsupported OS"

LOCAL_TEST = False  # Not use xml-rpc server for testing
TMP_DB_SCHEMA = 'temp'  # use 'temp', to drop tmp tables, or 'main' to save it for inspections
ZDLP_PATH = '/home/eugene/PycharmProjects/zdlp' if os.name == 'posix' else 'C:\\Users\\eugene\\work\\zdlp'
TMP_DIR_PATH = '/tmp' if os.name == 'posix' else 'C:\\Windows\\Temp'
TEST_DATA_PATH = os.path.join(ZDLP_PATH, 'test', 'data')
DB_PATH = os.path.join(ZDLP_PATH, 'main.sqlite')
LOG_PATH = os.path.join(ZDLP_PATH, 'zdlp.log')
ARCHIVE_PATH = os.path.join(TMP_DIR_PATH, 'zdlp_archive')
DB_VERSION = 1
LOG_VERSION = 1  # TODO make log to SQLite db

# RPC_SERVER = HOST_NAME = os.uname().nodename  # not work on Win
RPC_SERVER = 'localhost'
# HOST_NAME = platform.uname().node  # TODO failed socket.getaddrinfo() if hostname has national characters
HOST_NAME = socket.gethostname() # more portable
RPC_PORT = 8000
RPC_SERVER_PROXY_URL = f'http://{RPC_SERVER}:{RPC_PORT}'
BLOCK_SIZE = 1024  # bytes


# Object's status TODO refactor it to dict
STATUS_OK = 'OK'  # check passed, no pattern find
STATUS_FIND = '!!!'  # check passed, find pattern
STATUS_ERR = 'Err'  # check no passed due to error
STATUS_NEW = 'New'  # new or changed obj, need to be checked
STATUS_PROC = 'proc'  # object in process
STATUS_PASS = 'pass'  # ignore archive volume, process it different way

FILE_EXTENTIONS = {
 '.csv',
 '.doc',
 '.docx',
 '.eml',
 '.epub',
 '.gif',
 '.htm',
 '.html',
 '.jpeg',
 '.jpg',
 '.json',
 '.log',
 # '.mp3',
 '.msg',
 '.odt',
 # '.ogg',
 '.pdf',
 '.png',
 '.pptx',
 '.ps',
 '.psv',
 '.rtf',
 '.tff',
 '.tif',
 '.tiff',
 '.tsv',
 '.txt',
 # '.wav',
 '.xls',
 '.xlsx'}

MUST_USE_CONTAINERS = True
CONTAINERS = {'.rar', '.zip'}
CONTAINER_VOLUMES = {'rar': (r'\.part(\d+)\.rar$', r'\.r(\d\d)$'),
                     'zip': (r'\.(\d+)\.zip$', r'\.z\d\d)$')
                     }

CSV_SEPARATOR = '|'

RE = {
 'dsp': {'pattern': r'Д[\W_-]?С[\W_-]?П',
         'flags': re.IGNORECASE|re.MULTILINE|re.UNICODE},  # ДСП,"ДСП ", ЛДСП, __ДСП__, _Д_С_П_, =Д-С-П=
 'dsp1': {'pattern': 'для служебного (ис)?пользования',
          'flags': re.IGNORECASE|re.MULTILINE},
 'dsp2': {'pattern': 'Конфиденциально',
          'flags': re.IGNORECASE|re.MULTILINE},
 'dsp3': {'pattern': 'Коммерческая тайна',
          'flags': re.MULTILINE|re.MULTILINE}
}

DEFAULT_SCAN_ROOT_PATH = TEST_DATA_PATH
# '/home/eugene/work/test' if os.name == 'posix' else 'C:\\Users'
# DEFAULT_SCAN_ROOT_PATH = os.path.join(TEST_DATA_PATH, 'containers')
DEFAULT_ARC_PASSWORDS = ('P@$$w0rd', '1qazZAQ!', '3edcCDE#')
# DEFAULT_LOGIN = 'eugene'
