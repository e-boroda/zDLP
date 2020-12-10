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
#   zDLP file server.py
#
#

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import config as cfg
from lib.scanner import Scanner
from lib.extractor import Extractor
from lib.finder import Finder
from lib import logger

log = logger.get_logger(__name__)


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

    def log_message(format, *args, **kwargs):
        pass


def check_object(path, protocol):
    (status, value) = Extractor(path, protocol).extract()
    log.debug(path)
    log.debug(value)
    return Finder(value).find() if status == cfg.STATUS_PROC else (status, value)
    # if status == cfg.STATUS_PROC:
    #     return Finder(value).find()
    # elif status == cfg.STATUS_ERR:
    #     return status, value


def get_object(path, protocol='file'):
    if protocol == 'file':
        with open(path, mode='rb') as file:  # b is important -> binary
            return file.read()
    elif protocol == 'zip':
        ...  # TODO


def create_server(bind_host='', bind_port=cfg.RPC_PORT):
    """Create an XML-RPC server instance"""
    server = SimpleXMLRPCServer((bind_host, bind_port),
                                requestHandler=RequestHandler, allow_none=True)
    server.register_introspection_functions()
    # @server.register_function
    server.register_function(check_object)
    server.register_function(get_object)
    server.register_instance(Scanner(), allow_dotted_names=True)
    server.register_multicall_functions()
    # @server.register_function
    # @server.register_function
    # server.register_function(Scanner.get_n_obj_scanned)
    return server


# def start_server(server_instance):
#     t = threading.Thread(target=server_instance.serve_forever, name='server_instance', daemon=True)
#     t.start()
#     #log.info(f'Serving XML-RPC on {...} port {...}')
#     return t

if __name__ == '__main__':
    # Run the server's main loop
    log.info(f'Serving XML-RPC on {...} port {...}')
    create_server().serve_forever()
    # thread = start_server(srv)
    # input("Enter <ENTER> to exit server")
    # srv.shutdown()
    # srv.server_stop()



