import json
import psycopg2
import datetime
import psycopg2.extras
from .postgres_db import DataBaseHandle

from bot import Config

#special_characters = ['!','#','$','%', '&','@','[',']',' ',']','_', ',', '.', ':', ';', '<', '>', '?', '\\', '^', '`', '{', '|', '}', '~']

"""
SETTINGS VARS

TIDAL_AUTH_TOKEN - Tidal main auth token
TIDAL_AUTH_DONE - Status of Tidal Session (True/False)
TIDAL_API_KEY_INDEX - Index of API Key Selected
TIDAL_QUALITY - Music quality

KKBOX_QUALITY - Quality Of KKBOX Tracks (128k, 192k, 320k, hifi, hires)
KKBOX_AUTH - Status of KKBOX Authentication (True/False)

QOBUZ_AUTH - Status of QOBUZ Authentication (True/False)

AUTH_CHATS - Chats where bot is allowed
AUTH_USERS - Users who can use bot
AUTH_ADMINS - Admins of the bot

"""

class BotSettings(DataBaseHandle):

    def __init__(self, dburl=None):
        if dburl is None:
            dburl = Config.DATABASE_URL
        super().__init__(dburl)

        settings_schema = """CREATE TABLE IF NOT EXISTS bot_settings (
            id SERIAL PRIMARY KEY NOT NULL,
            var_name VARCHAR(50) NOT NULL UNIQUE,
            var_value VARCHAR(2000) DEFAULT NULL,
            vtype VARCHAR(20) DEFAULT NULL,
            blob_val BYTEA DEFAULT NULL,
            date_changed TIMESTAMP NOT NULL
        )"""

        cur = self.scur()
        try:
            cur.execute(settings_schema)
        except psycopg2.errors.UniqueViolation:
            pass

        self._conn.commit()
        self.ccur(cur)

    def set_variable(self, var_name, var_value, update_blob=False, blob_val=None):
        vtype = "str"
        if isinstance(var_value, bool):
            vtype = "bool"
        elif isinstance(var_value, int):
            vtype = "int"

        if update_blob:
            vtype = "blob"

        sql = "SELECT * FROM bot_settings WHERE var_name=%s"
        cur = self.scur()

        cur.execute(sql, (var_name,))
        if cur.rowcount > 0:
            if not update_blob:
                sql = "UPDATE bot_settings SET var_value=%s , vtype=%s WHERE var_name=%s"
            else:
                sql = "UPDATE bot_settings SET blob_val=%s , vtype=%s WHERE var_name=%s"
                var_value = blob_val

            cur.execute(sql, (var_value, vtype, var_name))
        else:
            if not update_blob:
                sql = "INSERT INTO bot_settings(var_name,var_value,date_changed,vtype) VALUES(%s,%s,%s,%s)"
            else:
                sql = "INSERT INTO bot_settings(var_name,blob_val,date_changed,vtype) VALUES(%s,%s,%s,%s)"
                var_value = blob_val

            cur.execute(sql, (var_name, var_value, datetime.datetime.now(), vtype))

        self.ccur(cur)

    def get_variable(self, var_name):
        sql = "SELECT * FROM bot_settings WHERE var_name=%s"
        cur = self.scur()

        cur.execute(sql, (var_name,))
        if cur.rowcount <= 0:
            return None, None

        row = cur.fetchone()
        vtype = row[3]
        val = row[2]
        if vtype == "bool":
            val = row[2] == "true"
        elif vtype == "int":
            val = int(row[2])
        elif vtype == "str":
            val = str(row[2])
        return val, row[4]

    def __del__(self):
        super().__del__()

class AuthedUsers(DataBaseHandle):
    def __init__(self, dburl=None):
        if dburl is None:
            dburl = Config.DATABASE_URL
        super().__init__(dburl)
        table_schema = """CREATE TABLE IF NOT EXISTS authed_users (
            uid bigint
        )"""
        cur = self.scur()
        try:
            cur.execute(table_schema)
        except psycopg2.errors.UniqueViolation:
            pass
        self._conn.commit()
        self.ccur(cur)

    def set_users(self, var_value):
        sql = "SELECT * FROM authed_users"
        cur = self.scur()
        cur.execute(sql)
        sql = f"INSERT INTO authed_users VALUES({var_value})"
        cur.execute(sql)
        self.ccur(cur)

    def get_users(self):
        sql = "SELECT * FROM authed_users"
        cur = self.scur()
        cur.execute(sql)
        return cur.fetchall() if cur.rowcount > 0 else (None, None)

    def __del__(self):
        super().__del__()

class AuthedAdmins(DataBaseHandle):
    def __init__(self, dburl=None):
        if dburl is None:
            dburl = Config.DATABASE_URL
        super().__init__(dburl)
        table_schema = """CREATE TABLE IF NOT EXISTS authed_admins (
            uid bigint
        )"""
        cur = self.scur()
        try:
            cur.execute(table_schema)
        except psycopg2.errors.UniqueViolation:
            pass
        self._conn.commit()
        self.ccur(cur)

    def set_admins(self, var_value):
        sql = "SELECT * FROM authed_admins"
        cur = self.scur()
        cur.execute(sql)
        sql = f"INSERT INTO authed_admins VALUES({var_value})"
        cur.execute(sql)
        self.ccur(cur)

    def get_admins(self):
        sql = "SELECT * FROM authed_admins"
        cur = self.scur()
        cur.execute(sql)
        return cur.fetchall() if cur.rowcount > 0 else (None, None)

    def __del__(self):
        super().__del__()

class AuthedChats(DataBaseHandle):
    def __init__(self, dburl=None):
        if dburl is None:
            dburl = Config.DATABASE_URL
        super().__init__(dburl)
        table_schema = """CREATE TABLE IF NOT EXISTS authed_chats (
            uid bigint
        )"""
        cur = self.scur()
        try:
            cur.execute(table_schema)
        except psycopg2.errors.UniqueViolation:
            pass
        self._conn.commit()
        self.ccur(cur)

    def set_chats(self, var_value):
        sql = "SELECT * FROM authed_chats"
        cur = self.scur()
        cur.execute(sql)
        sql = f"INSERT INTO authed_chats VALUES({var_value})"
        cur.execute(sql)
        self.ccur(cur)

    def get_chats(self):
        sql = "SELECT * FROM authed_chats"
        cur = self.scur()
        cur.execute(sql)
        return cur.fetchall() if cur.rowcount > 0 else (None, None)

    def __del__(self):
        super().__del__()


"""
ON_TASK - True/False (For ANTI SPAM)
"""
class UserSettings(DataBaseHandle):
    shared_users = {}

    def __init__(self, dburl=None):
        if dburl is None:
            dburl = Config.DATABASE_URL
        super().__init__(dburl)

        cur = self.scur()

        table = """CREATE TABLE IF NOT EXISTS user_settings (
            user_id VARCHAR(50) NOT NULL,
            json_data VARCHAR(1000) NOT NULL
        )"""

        try:
            cur.execute(table)
        except psycopg2.errors.UniqueViolation:
            pass

        self.ccur(cur)

    def set_var(self, user_id, var_name, var_value):
        user_id = str(user_id)
        sql = "SELECT * FROM user_settings WHERE user_id=%s"
        cur = self.scur(dictcur=True)

        user = self.shared_users.get(user_id)
        if user is not None:
            self.shared_users[user_id][var_name] = var_value
        else:
            cur.execute(sql, (user_id,))
            if cur.rowcount > 0:
                user = cur.fetchone()
                jdata = user.get("json_data")
                jdata = json.loads(jdata)
                jdata["LANGUAGE"] = var_value
                self.shared_users[user_id] = jdata
            else:
                self.shared_users[user_id] = {var_name: var_value}

        cur.execute(sql, (user_id,))
        if cur.rowcount > 0:
            insql = "UPDATE user_settings SET json_data = %s where user_id=%s"
            cur.execute(insql, (json.dumps(self.shared_users.get(user_id)), user_id))

        else:
            insql = "INSERT INTO user_settings(user_id, json_data) VALUES(%s, %s)"
            cur.execute(insql, (user_id, json.dumps(self.shared_users.get(user_id))))

        self.ccur(cur)

    def get_var(self, user_id, var_name):
        user_id = str(user_id)
        # search the cache
        user = self.shared_users.get(user_id)
        if user is not None:
            return user.get(var_name)
        cur = self.scur(dictcur=True)

        cur.execute("SELECT * FROM user_settings WHERE user_id=%s", (user_id, ))
        if cur.rowcount <= 0:
            return None

        user = cur.fetchone()
        jdata = user.get("json_data")
        jdata = json.loads(jdata)
        self.shared_users[user_id] = jdata
        return jdata.get(var_name)

set_db = BotSettings()
users_db = AuthedUsers()
admins_db = AuthedAdmins()
chats_db = AuthedChats()
user_settings = UserSettings()