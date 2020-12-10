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
#   zDLP file finder.py
#
#

import re
import config as cfg
from . import logger

log = logger.get_logger(__name__)


class Finder:
    def __init__(self, text, regexp=cfg.RE['dsp']['pattern'], re_flags=cfg.RE['dsp']['flags']):
        self.text = text
        self.regexp = regexp
        self.re_flags = re_flags

    def set_regexp(self, regexp):
        self.regexp = regexp

    def set_re_flags(self, re_flags):
        self.re_flags = re_flags

    def set_text(self, text):
        self.text = text

    def find(self):
        try:
            search = re.search(self.regexp, self.text, self.re_flags)
        except TypeError as te:
            return cfg.STATUS_ERR, f"TypeError in finder:{str(te)}"
        return (cfg.STATUS_FIND, search.group()) if search else (cfg.STATUS_OK, None)

