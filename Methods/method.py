from DB import db
from Models import UserModel
import uuid

class Methods():
    #Global variables declared
    conn = db.Mysqlconfig.conn
    cur = db.Mysqlconfig.cursor
    err =db.Mysqlconfig.error
    #--------
    def updatesession(id):
         tuuid=uuid1()
         sql_query=f"CALL update_sessionid_sp({id},{tuuid})"
         cur.execute(sql_query)
         result=cur.fetchone()
         return ''
         