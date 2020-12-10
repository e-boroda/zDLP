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
#   zDLP file test_util.py
#
#

import pytest
#util = pytest.importorskip('.util')
import lib.util as util


def test_esc():
    assert util.esc("Text' with'' single' quotes.") == "Text'' with'''' single'' quotes."
    assert util.esc("Текст' с одинарными'' кавычками.") == "Текст'' с одинарными'''' кавычками."


def test_dedot():
    assert util.dedot('.dotted.с точкой') == 'dotted.с точкой'
    assert util.dedot('без точки.undotted') == 'без точки.undotted'


def test_get_tmp_name():
    n = 10000
    assert len({util.get_tmp_name() for _ in range(n)}) == n
    assert len({util.get_tmp_name('some_string') for _ in range(n)}) == n


if __name__ == '__main__':
    pass

