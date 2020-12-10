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
#   zDLP file test_textract.py
#
#

#import pytest

##import pdb
##pdb.set_trace()

import textract


PATH_TIFF = r'C:\Users\eugene\work\zdlp\test\data\дсп.tif'

def test_process():
    text = textract.process(PATH_TIFF, lang='rus+eng')
    print(text)


test_process()
