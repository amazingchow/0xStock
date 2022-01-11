# -*- coding: utf-8 -*-
import logging
import mysql.connector
import mysql.connector.pooling
import os

from mysql.connector import errorcode
from .singleton import Singleton


@Singleton
class MySQLConnector():
    def __init__(self):
        self.host = os.environ.get("MYSQL_HOST")
        if self.host is None or len(self.host) == 0:
            raise Exception("MYSQL_HOST must be set!!!")
        self.port = os.environ.get("MYSQL_PORT")
        if self.port is None or len(self.port) == 0:
            raise Exception("MYSQL_PORT must be set!!!")
        self.username = os.environ.get("MYSQL_USERNAME")
        if self.username is None or len(self.username) == 0:
            raise Exception("MYSQL_USERNAME must be set!!!")
        self.password = os.environ.get("MYSQL_PASSWORD")
        if self.password is None or len(self.password) == 0:
            raise Exception("MYSQL_PASSWORD must be set!!!")

        self.logger = logging.getLogger('stock_db')
        self.logger.setLevel(logging.INFO)
        _formatter = logging.Formatter("[%(asctime)-15s][%(levelname)-5s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        _file_handler = logging.FileHandler('logs/stock_db.log', 'w')
        _file_handler.setFormatter(_formatter)
        self.logger.addHandler(_file_handler)

    def init_conn(self, db: str):
        try:
            dbconfig = {
                "host": self.host,
                "port": self.port,
                "user": self.username,
                "password": self.password,
                "database": db,
                "allow_local_infile": True
            }
            self.cnxpool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="mysql-conn-pool", pool_size=8, **dbconfig
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise Exception("Invalid MYSQL_USERNAME or MYSQL_PASSWORD")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise Exception("Database {} does not exist".format(db))
            else:
                raise Exception("Unknown err: {}".format(err))
        cnx = self.cnxpool.get_connection()
        if not cnx.is_connected():
            raise Exception("MySQL Server can not be connected ({}:{}@{}:{})".format(
                self.username, self.password, self.host, self.port
            ))
        else:
            self.logger.debug("Connect to MySQL Server ({}:{})".format(
                self.host, self.port
            ))
        cnx.close()

    def release_conn(self):
        # TODO: How to release the pooling resources?
        self.logger.debug("Disconnect from MySQL Server ({}:{})".format(
            self.host, self.port
        ))

    def load_data_infile(self, stmt: str):
        cnx = self.cnxpool.get_connection()
        cur = cnx.cursor()
        try:
            cur.execute(stmt)
            cnx.commit()
        except mysql.connector.Error as err:
            cnx.rollback()
            self.logger.error("LOAD DATA INFILE err: {}".format(err))
        finally:
            cur.close()
            cnx.close()

    def query(self, stmt: str):
        cnx = self.cnxpool.get_connection()
        cur = cnx.cursor()
        result = object()
        try:
            cur.execute(stmt)
            result = cur.fetchall()
        except mysql.connector.Error as err:
            self.logger.error("QUERY err: {}".format(err))
        finally:
            cur.close()
            cnx.close()
        return result

    def delete(self, stmt: str):
        cnx = self.cnxpool.get_connection()
        cur = cnx.cursor()
        try:
            cur.execute(stmt)
            cnx.commit()
        except mysql.connector.Error as err:
            cnx.rollback()
            self.logger.error("DELETE err: {}".format(err))
        finally:
            cur.close()
            cnx.close()