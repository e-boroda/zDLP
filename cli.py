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
#   zDLP file cli.py - CLI for manager
#
#

import xmlrpc.client
from datetime import datetime
import click
from lib.zdb import ZDB, ZObj, ZObjGenerator
import config as cfg
from lib.util import dedot
from lib import logger


log = logger.get_logger(__name__)

# 4 testing only, must be on server side
if cfg.LOCAL_TEST:
    from lib.extractor import Extractor
    from lib.finder import Finder
    from lib.scanner import Scanner

    def check_object(path, protocol):
        (status, value) = Extractor(path, protocol).extract()
        # log.debug(path)
        # log.debug(value)
        return Finder(value).find() if status == cfg.STATUS_PROC else (status, value)


def get_server(host):
    proxy_url = f'http://{host}:{cfg.RPC_PORT}'  # TODO - problem with nonASCII chars in hostname!!!
    return xmlrpc.client.ServerProxy(proxy_url)


def scan_objects(server, db):
    log.info(f"Scanning for objects")
    server.set_protocol(db.get_protocol())
    server.set_root(db.get_root())
    path_list = server.scan()
    list_len = server.get_n_obj_scanned()
    log.info(f"{list_len} objects scanned")
    db.update_paths(path_list)
    # print (f"{rowcount} rows inserted.")
    # if cfg.MUST_USE_CONTAINERS:
    #     log.info(f"Scanning for containers")
    #     for name in cfg.CONTAINERS:
    #         protocol = dedot(name)
    #         server.set_protocol(protocol)
    #         db.set_protocol(protocol)
    #         containers_lis = db.get_paths()
    #         log.debug(f'find {protocol} containers => {len(containers_lis)}')
    #         for container in containers_lis:
    #             container_path = container[5]
    #             log.info(f'container => {container_path}')
    #             server.set_root(container_path)
    #             path_list = server.scan()
    #             list_len = server.get_n_obj_scanned()
    #             log.info(f"{list_len} containers  scanned")
    #             db.update_paths(path_list)
    return db.get_paths()


def check_objects(server, db, paths):
    for (id_, cid, proto, host, root, path, mtime, size, stat, reason) in paths:
        dt = datetime.fromtimestamp(mtime).strftime('%Y.%m.%d-%H:%M:%S')
        (status, value) = server.check_object(path, proto) if not cfg.LOCAL_TEST else check_object(path, proto)
        db.set_protocol(proto)
        if status == cfg.STATUS_OK:
            db.mark_as_ok(path)
        elif status == cfg.STATUS_FIND:
            db.mark_as_failed(value, path)
        elif status == cfg.STATUS_ERR:
            db.mark_as_error(value, path)
        elif status == cfg.STATUS_PASS:
            db.mark_as_pass(value, path)
        else:
            log.error(f"Unexpected obj status returned:{status}, while processing {proto}:{host}:{path}")
        log.debug(f"{id_} {proto}:{host}:{path}\t {dt} {round(size / 1024, 2)}K {status} {value}")


@click.group()
def cli():
    pass

# ----------------- CLI commands
@cli.command()
@click.option('--host', default=cfg.HOST_NAME, prompt="Host name", help='Host name')
@click.option('--proto', default='file', prompt="Host type", help='Enter access protocol (file, oracle, mssql ...)')
@click.option('--root', default=cfg.DEFAULT_SCAN_ROOT_PATH, prompt="Root path", help='Root path')
# @click.option('--login', default=cfg.DEFAULT_LOGIN, prompt="Admin login", help='Admin login')
# @click.option('--password', prompt=True, confirmation_prompt=True, hide_input=True)
@click.option('--description', default='',  prompt="Description", help='Description')
def add_root(proto, host,  root, description):
    db = ZDB()
    db.add_root(proto, host, root, description)
    click.secho(f"Add new root => {proto}:{host}:{root} = {description}", color='green')


@cli.command()
@click.option('--host', default=cfg.HOST_NAME, prompt="Host name", help='Host name')
@click.option('--proto', default='file', prompt="Host type", help='Enter access protocol (file, oracle, mssql ...)')
@click.option('--root', default=cfg.DEFAULT_SCAN_ROOT_PATH, prompt="Root path", help='Root path')
def del_root(root, host, proto):
    db = ZDB(root, host, proto)
    db.del_root()
    click.secho(f"Delete root => {root} from {proto}:{host}", color='green')


@cli.command()
@click.option('--host', default=cfg.HOST_NAME, prompt="Host name", help='Host name')
@click.option('--proto', default='file', prompt="Host type", help='Enter access protocol (file, oracle, mssql ...)')
def del_all_roots(host, proto):
    db = ZDB(host=host, protocol=proto)
    db.del_all_roots()
    click.secho(f"Delete all roots from => {proto}:{host} ", color='green')


@cli.command()
@click.option('--host', default=cfg.HOST_NAME, prompt="Host name", help='Host name')
@click.option('--proto', default='file', prompt="Host type", help='Enter access protocol (file, oracle, mssql ...)')
@click.option('--root', default=cfg.DEFAULT_SCAN_ROOT_PATH, prompt="Root path", help='Root path')
def clean_root(root, host, proto):
    db = ZDB()
    db.set_protocol(proto)
    db.set_host(host)
    db.set_root(root)
    db.clean_root()
    click.secho(f"Cleaning => {proto}:{host}:{root}", color='green')


@cli.command()
@click.option('--host', default=cfg.HOST_NAME, prompt="Host name", help='Host name')
def reset_host(host):
    db = ZDB(host=host)
    db.reset_all_paths()
    click.secho(f"Reset all paths as not checked for host => {host} ", color='green')


@cli.command()
@click.option('--host', default=cfg.HOST_NAME, prompt="Host name", help='Host name')
def clean_host(host):
    db = ZDB(host=host)
    db.clean_host()
    click.secho(f"Cleaning all paths for host => {host} ", color='green')


@cli.command()
@click.option('--host', default=cfg.HOST_NAME, prompt="Host name", help='Host name')
def del_host(host):
    db = ZDB(host=host)
    db.del_host()
    click.secho(f"Completely delete host => {host} ", color='green')


@cli.command()
@click.option('--status', default=cfg.STATUS_FIND, prompt="What status?", help='list all objects with given status')
def list_all(status):
    """
    List all records with given status
    :param: status
    :return: print all records with given status on stdout
    """
    db = ZDB()
    print(cfg.CSV_SEPARATOR.join(ZObj(range(10)).__dict__.keys()))
    for row in db.get_all_obj(status):
        print(cfg.CSV_SEPARATOR.join([str(s) for s in row]))


@cli.command()
@click.option('--host', default=cfg.HOST_NAME, prompt="Host name", help='Host name')
@click.option('--proto', default='file', prompt="Host type", help='Enter access protocol (file, oracle, mssql ...)')
@click.option('--root', default=cfg.DEFAULT_SCAN_ROOT_PATH, prompt="Root path", help='Root path')
def scan_root(root, host, proto):
    srv = get_server(host) if not cfg.LOCAL_TEST else Scanner(root=root, host=host, protocol=proto)
    cfg.LOCAL_TEST or log.info(f"Connect to {cfg.RPC_SERVER_PROXY_URL} XML-RPC server")
    db = ZDB(root, host, proto)
    paths = scan_objects(srv, db)
    log.info(f"Updating changed objects in database for root {proto}:{host}:{root}")
    log.info(f"Got {len(paths)} changed paths for check")


@cli.command()
@click.option('--root', default=cfg.DEFAULT_SCAN_ROOT_PATH, prompt="Root path", help='Root path')
@click.option('--host', default=cfg.HOST_NAME, prompt="Host name", help='Host name')
@click.option('--proto', default='file', prompt="Host type", help='Enter access protocol (file, oracle, mssql ...)')
def check_root(root, host, proto):
    srv = get_server(host) if not cfg.LOCAL_TEST else Scanner(root=root, host=host)
    cfg.LOCAL_TEST or log.info(f"Connect to http://{host}:{cfg.RPC_PORT} XML-RPC server")
    cfg.LOCAL_TEST or log.info(f"Available RPC methods:{str(srv.system.listMethods())}")
    db = ZDB(root=root, host=host, protocol=proto)
    db.set_root(root)
    log.info(f"Updating changed objects in database for {proto}:{host}:{root}")
    paths = scan_objects(srv, db)
    log.info(f"Got {len(paths)} changed paths for check")
    #log.debug(paths)
    log.info(f"Check objects...")
    check_objects(srv, db, paths)
    log.info(f"Work done! Look at DB for results.")


@cli.command()
@click.option('--host', default=cfg.HOST_NAME, prompt="Host name", help='Host name')
def check_host(host):
    srv = get_server(host) if not cfg.LOCAL_TEST else Scanner(host=host)
    cfg.LOCAL_TEST or log.info(f"Connect to {cfg.RPC_SERVER_PROXY_URL} XML-RPC server")
    cfg.LOCAL_TEST or log.info(f"Available RPC methods:{str(srv.system.listMethods())}")
    db = ZDB(host=host)
    for root in db.get_all_roots():
        db.set_root(root)
        paths = scan_objects(srv, db)
        log.info(f"Updating changed objects in database for {root}")
        log.info(f"Got {len(paths)} changed paths for check")
        log.info(f"Check objects...")
        check_objects(srv, db, paths)
        log.info(f"Work done! Look at ZDB for results.")


@cli.command()
@click.option('--host', prompt="Host name", help='Host name from where copy file')
@click.option('--path', prompt="Root path", help='Root path')
@click.option('--to-dir', default=cfg.TMP_DIR_PATH, prompt="Destination dir", help='Destination dir')
def copy_file_from(host, path, to_dir):
    pass


@cli.command()
@click.option('--host', default=cfg.HOST_NAME, prompt="Host name", help='Host name')
@click.option('--root', default=cfg.DEFAULT_SCAN_ROOT_PATH, prompt="Root path", help='Root path')
def list_files_from(host, root):
    srv = get_server(host) if not cfg.LOCAL_TEST else ...
    for ftype, mtime, name in srv.list_files(root):
        print(f"{ftype} {mtime} {name}")


if __name__ == '__main__':
    cli()
