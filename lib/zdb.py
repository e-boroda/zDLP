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
#   zDLP file zdb.py
#
#


import os
import sqlite3
import click
import config as cfg
from lib.util import esc, get_tmp_name
from lib import logger, util

log = logger.get_logger(__name__)


class ZObj:
    def __init__(self, fields_list):
        (self.id,
         self.cid,
         self.protocol,
         self.host,
         self.root,
         self.path,
         self.mtime,
         self.size,
         self.status,
         self.reason) = fields_list

    def __repr__(self):
        return (self.id,
                self.cid,
                self.protocol,
                self.host,
                self.root,
                self.path,
                self.mtime,
                self.size,
                self.status,
                self.reason)

    def __str__(self):
        return self.__dict__


class ZObjGenerator:

    def __init__(self, obj_list):
        self.obj_iterator = iter(obj_list)

    def get(self):
        for obj in self.obj_iterator:
            yield ZObj(obj)


class ZDB:
    """
    Interface for ZDLP main DB
    """

    def __init__(self, root=cfg.DEFAULT_SCAN_ROOT_PATH, host=cfg.HOST_NAME, protocol='file', db_path=cfg.DB_PATH):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.protocol = protocol
        self.host = host
        self.root = esc(root)

    def reinitialize(self):
        """Create new DB structure"""
        self.cursor.execute(""" PRAGMA foreign_keys = OFF """)
        self.cursor.execute(""" DROP INDEX IF EXISTS obj_phrp """)
        self.cursor.execute(""" DROP TABLE IF EXISTS  obj """)
        self.cursor.execute(f""" CREATE TABLE IF NOT EXISTS obj (
                                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                cid INTEGER REFERENCES obj(id) ON DELETE CASCADE, 
                                protocol TEXT NOT NULL, 
                                host TEXT NOT NULL,
                                root TEXT NOT NULL,
                                path TEXT NOT NULL, 
                                mtime REAL NOT NULL, 
                                size INTEGER NOT NULL, 
                                status TEXT DEFAULT '{cfg.STATUS_NEW}', 
                                reason TEXT,
                                pwd_id INTEGER REFERENCES pwd(id),
                                FOREIGN KEY (protocol, host, root) 
                                REFERENCES root(protocol, host, root) 
                                ON DELETE CASCADE) """)
        self.cursor.execute(""" CREATE UNIQUE INDEX IF NOT EXISTS obj_phrp 
                                ON obj(protocol, host, root, path) """)
        self.cursor.execute(f""" CREATE INDEX IF NOT EXISTS obj_phr 
                                        ON obj(protocol, host, root) """)
        self.cursor.execute(""" DROP TABLE IF EXISTS root """)
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS root (
                                protocol TEXT NOT NULL,
                                host TEXT NOT NULL, 
                                root TEXT NOT NULL, 
                                description TEXT ,
                                PRIMARY KEY (protocol, host, root)) """)
        self.cursor.execute("""DROP TABLE IF EXISTS  pwd""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS pwd (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                pwd TEXT,
                                description TEXT )""")
        # self.cursor.execute("DROP TABLE IF EXISTS  proto_group")
        # self.cursor.execute("CREATE TABLE IF NOT EXISTS proto_group ("
        #                     "group TEXT NOT NULL CHECK group IN ('fs', 'db'), "
        #                     "protocol TEXT NOT NULL )")
        self.cursor.execute("""PRAGMA foreign_keys = ON""")

    def update_paths(self, path_list):
        """
        Update paths in obj table from new scan
        """
        # host_name = path_list[0][1]  # TODO if root_path not exists - got Index exception here
        tmp_tab_name = get_tmp_name()
        self.cursor.execute(f""" DROP TABLE IF EXISTS {tmp_tab_name} """)
        self.cursor.execute(f""" CREATE TABLE {tmp_tab_name} AS 
                                SELECT * FROM obj WHERE id is NULL """)
        log.debug(f"CREATE TABLE {tmp_tab_name}")
        self.cursor.executemany(f""" INSERT INTO {tmp_tab_name} (protocol, host, root, path, mtime, size) 
                                    VALUES (?, ?, ?, ?, ?, ?) """, path_list)
        self.cursor.execute(f""" CREATE INDEX IF NOT EXISTS {get_tmp_name()}
                                ON {tmp_tab_name.split('.')[1]}(protocol, host, root) """)
        self.cursor.execute(f""" CREATE INDEX IF NOT EXISTS {get_tmp_name()}
                                        ON {tmp_tab_name.split('.')[1]}(protocol, host, root, path) """)
        log.debug(f"INSERT INTO {tmp_tab_name.split('.')[1]}")
        # self.cursor.execute(f""" UPDATE {tmp_tab_name} SET root = ? """, (self.root,))
        # TODO -optimize next query (may be join condition) - very long time on large table
        # self.cursor.execute(f""" DELETE FROM obj WHERE id IN (
        #                         SELECT DISTINCT obj.id FROM obj
        #                             JOIN {tmp_tab_name} t ON
        #                                 obj.protocol == t.protocol AND
        #                                 obj.host == t.host AND
        #                                 obj.root == t.root
        #                         WHERE NOT EXISTS (
        #                             SELECT * FROM {tmp_tab_name} tmp WHERE
        #                                 -- obj.protocol == tmp.protocol AND
        #                                 -- obj.host == tmp.host AND
        #                                 -- obj.root == tmp.root AND
        #                                 obj.path == tmp.path
        #                                 )
        #                         ) """)
        self.cursor.execute(f""" DELETE FROM obj WHERE (protocol, host, root, path) IN (
                                    SELECT protocol, host, root, path FROM obj
                                    EXCEPT
                                    SELECT protocol, host, root, path FROM {tmp_tab_name}) """)

        log.debug(f"DELETE FROM obj WHERE... ")
        self.connection.commit()  # Only for tests, TODO - remove this in production
        # self.cursor.execute(f"""INSERT INTO obj
        #                         SELECT NULL, cid, protocol, host, root, path, mtime, size, status, reason
        #                         FROM {tmp_tab_name} tmp WHERE NOT EXISTS (
        #                             SELECT * FROM obj WHERE
        #                                 obj.protocol == tmp.protocol AND
        #                                 obj.host == tmp.host AND
        #                                 obj.root == tmp.root AND
        #                                 obj.path == tmp.path
        #                             ) """)
        self.cursor.execute(f"""INSERT INTO obj 
                                SELECT NULL, cid, protocol, host, root, path, mtime, size, status, reason 
                                    FROM {tmp_tab_name}
                                    WHERE (protocol, host, root, path) IN (
                                        SELECT protocol, host, root, path FROM {tmp_tab_name}
                                        EXCEPT
                                        SELECT protocol, host, root, path FROM obj ) """)
        log.debug(f"INSERT INTO obj...")
        # a very, very dumb code to upgrade records
        # please TODO make following actions with SQL query!
        tmp_tab_rows_list = self.cursor.execute(f""" SELECT * FROM {tmp_tab_name} """).fetchall()
        log.debug(f"SELECT * FROM {tmp_tab_name}... {len(tmp_tab_rows_list)} rows and go into cycle...")
        # for id1, cid1, proto1, host1, root1, path1, mtime1, size1, status1, reason1 in tmp_tab_rows_list:

        for i, obj1 in enumerate(ZObjGenerator(tmp_tab_rows_list).get()):
            # root1 = esc(root1)
            # path1 = esc(path1)
            obj1.root = esc(obj1.root)
            obj1.path = esc(obj1.path)
            obj_row = self.cursor.execute(f""" SELECT * FROM obj WHERE
                                                protocol == '{obj1.protocol}' AND 
                                                host == '{obj1.host}' AND
                                                root == '{obj1.root}' AND
                                                path == '{obj1.path}' """).fetchone()
            obj2 = ZObj(obj_row)
            obj2.root = esc(obj2.root)
            obj2.path = esc(obj2.path)
            # id2, cid2, proto2, host2, root2, path2, mtime2, size2, status2, reason2 = self.cursor.execute(f"""SELECT * FROM obj WHERE
            #                                                                                 protocol == '{proto1}' AND
            #                                                                                 host == '{host1}' AND
            #                                                                                 root == '{root1}' AND
            #                                                                                 path == '{path1}'""").fetchone()
            # root2 = esc(root2)
            # path2 = esc(path2)
            if obj1.mtime != obj2.mtime or obj1.size != obj2.size:  # object was changed
                self.cursor.execute(f"""UPDATE obj SET 
                                        mtime = {obj1.mtime}, 
                                        size = {obj1.size}, 
                                        status = '{cfg.STATUS_NEW}'
                                        WHERE 
                                            protocol == '{obj2.protocol}' AND 
                                            host == '{obj2.host}' AND 
                                            root == '{obj2.root}' AND
                                            path == '{obj2.path}' """)
        self.connection.commit()
        # return self.cursor.rowcount

    def get_paths(self):
        """Select and return obj list for check"""
        if cfg.MUST_USE_CONTAINERS:
            protocols = [util.dedot(ext_name) for ext_name in cfg.CONTAINERS]  # TODO use util.get_file_protocols()
            protocols.append(self.protocol)

            sql_get_paths = f"""SELECT * FROM obj 
                                        WHERE
                                            protocol IN {str(tuple(protocols))} AND
                                            host == '{self.host}' AND
                                            root == '{self.root}' AND
                                            (status == '{cfg.STATUS_NEW}' OR 
                                                status IS NULL) """
        else:
            sql_get_paths = f"""SELECT * FROM obj 
                                        WHERE
                                            protocol == '{self.protocol}' AND
                                            host == '{self.host}' AND
                                            root == '{self.root}' AND
                                            (status == '{cfg.STATUS_NEW}' OR 
                                                status IS NULL) """
        return self.cursor.execute(sql_get_paths).fetchall()

    def get_all_paths(self):
        """Select and return obj list for check for all roots"""
        return self.cursor.execute(f"""SELECT * FROM obj 
                                        WHERE
                                            protocol == '{self.protocol}' AND
                                            host == '{self.host}' AND
                                            (status == '{cfg.STATUS_NEW}' 
                                                OR status IS NULL) """).fetchall()

    def get_all_roots(self):
        roots = list()
        for row in self.cursor.execute(f"""SELECT root FROM root 
                                            WHERE
                                                protocol == '{self.protocol}' AND
                                                host == '{self.host}' """).fetchall():
            roots.append(row[0])
        return roots

    def get_root(self):
        return self.root

    def get_host(self):
        return self.host

    def get_protocol(self):
        return self.protocol

    def set_protocol(self, protocol):
        self.protocol = protocol

    def set_host(self, host):
        self.host = host

    def set_root(self, root):
        self.root = esc(root)

    def mark_as_ok(self, path):
        self.mark_obj(cfg.STATUS_OK, None, path)

    def mark_as_failed(self, reason, path):
        self.mark_obj(cfg.STATUS_FIND, reason, path)

    def mark_as_error(self, reason, path):
        self.mark_obj(cfg.STATUS_ERR, reason, path)

    def mark_as_new(self, path):
        self.mark_obj(cfg.STATUS_NEW, None, path)

    def mark_as_pass(self, reason, path):
        self.mark_obj(cfg.STATUS_PASS, reason, path)

    def mark_obj(self, status, reason, path):
        """
        mark obj with different statuses with there reason
        """
        # print (status, path, host, protocol)
        self.cursor.execute(f""" UPDATE obj SET 
                                    status = ?, 
                                    reason = ? 
                                WHERE 
                                    protocol == ? AND 
                                    host == ? AND 
                                    root == ? AND 
                                    path == ? """,
                            (status, reason, self.protocol, self.host, self.root, path))
        self.connection.commit()

    def reset_all_paths(self):
        self.cursor.execute(f""" UPDATE obj SET 
                                    status='New', 
                                    reason = NULL 
                                WHERE 
                                    -- protocol == '{self.protocol}' AND
                                    host == '{self.host}' """)
        self.connection.commit()

    def add_root(self, protocol, host, root, description):
        self.cursor.execute(""" INSERT INTO root (protocol, host, root, description)
                                VALUES (?, ?, ?, ?) """,
                            (protocol, host, root, description))
        self.connection.commit()

    def del_host(self):
        self.clean_host()
        self.cursor.execute(f""" DELETE FROM root 
                                    WHERE 
                                        host == '{self.host}' """)
        self.connection.commit()

    def del_all_roots(self):
        self.clean_all_roots()
        self.cursor.execute(f""" DELETE FROM root 
                                    WHERE 
                                        host == '{self.host}' AND 
                                        protocol == '{self.protocol}' """)
        self.connection.commit()

    def del_root(self):
        self.clean_root()
        self.cursor.execute(f""" DELETE FROM root 
                                    WHERE 
                                        protocol == '{self.protocol}' AND 
                                        host == '{self.host}' AND 
                                        root =='{self.root}' """)
        self.connection.commit()

    def clean_root(self):
        self.cursor.execute(f""" DELETE FROM obj 
                                    WHERE 
                                        protocol == '{self.protocol}' AND 
                                        host == '{self.host}' AND 
                                        root == '{self.root}'  """)
        self.connection.commit()

    def clean_all_roots(self):
        self.cursor.execute(f""" DELETE FROM obj 
                                    WHERE 
                                        host == '{self.host}' AND 
                                        protocol == '{self.protocol}' """)
        self.connection.commit()

    def clean_host(self):
        self.cursor.execute(f""" DELETE FROM obj 
                                    WHERE 
                                        host == '{self.host}' """)
        self.connection.commit()

    def get_obj(self, status=cfg.STATUS_FIND):
        return self.cursor.execute(f"""SELECT * FROM obj 
                                        WHERE
                                            protocol == '{self.protocol}' AND
                                            host == '{self.host}' AND
                                            status == '{status}' """).fetchall()

    def get_host_obj(self, host=cfg.HOST_NAME, status=cfg.STATUS_FIND):
        return self.cursor.execute(f"""SELECT * FROM obj 
                                                WHERE
                                                    -- protocol == '{self.protocol}' AND
                                                    host == '{host}' AND
                                                    status == '{status}' """).fetchall()

    def get_all_obj(self, status=cfg.STATUS_FIND):
        return self.cursor.execute(f"""SELECT * FROM obj 
                                                WHERE
                                                    -- protocol == '{self.protocol}' AND
                                                    -- host == '{self.host}' AND
                                                    status == '{status}' """).fetchall()

    def copy_remote_files(self, server, host, status):
        dir_name = os.path.join(cfg.ARCHIVE_PATH, host)
        os.mkdir(dir_name)
        protocols = util.get_file_protocols()
        sql = f""" SELECT DISTINCT path FROM obj 
                    WHERE host == '{host}' 
                    AND protocol IN {str(tuple(protocols))} 
                    AND status == '{status}' 
                    ORDER BY path """
        for path in self.cursor.execute(sql).fetchall():
            log.debug(f"Copy {host}:{path}...")
            local = os.path.join(dir_name, path)
            util.get_remote_file(server, remote_path=path, local_path=local)
            log.debug(f"... to {local}")



@click.command()
@click.confirmation_option(prompt='Are you sure you want to REINITIALIZE the db? All data will be lost!')
def reinit():
    ZDB().reinitialize()
    print(f"Initialization success.")


if __name__ == '__main__':
    reinit()
