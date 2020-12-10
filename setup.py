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
#   zDLP file setup.py
#
#

from setuptools import setup

setup(
    name='zDLP',
    version='0.1.0',
    packages=['lib', 'lib.SQL', 'lib.test', 'win', 'test'],
    url='',
    license='Apache 2.0',
    author='Eugene Borodin',
    author_email='eugene.borodin at gmail.com',
    description='DLP system'
)
