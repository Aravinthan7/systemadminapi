from fastapi import FastAPI, Request, HTTPException
from DB import db
from Models import UserModel

# Global variables declared
app = FastAPI()
conn = db.Mysqlconfig.conn
cur = db.Mysqlconfig.cursor
err = db.Mysqlconfig.error
# --------


@app.get('/checkservice')
async def root() -> dict:
    return {"message": "Check Service"}


@app.post('/signup')
async def Signup(usersignup: UserModel.User):
    try:

        cur.callproc("Signup_sp", args=(
                     usersignup.username,
                     usersignup.email,
                     usersignup.password,
                     usersignup.profileimage,
                     usersignup.role,
                     usersignup.addinfo,
                     usersignup.userid,
                     usersignup.systemno,
                     usersignup.sessionid
                     )
                     )
        conn.commit()

        # Fetch the result of the procedure
        cur.execute("SELECT @_Signup_sp_0")
        message = cur.fetchone()[0]

        return {status: 200, 'detail': '', "message": message}
    except db.Mysqlconfig.error as err:
        # conn.rollback()
        return HTTPException(status=500, detail=f"Database error: {err._full_msg}", message=err.msg)
    finally:
        cur.close()
        conn.close()


@app.post('/login')
async def Login(request: Request, user: UserModel.UserLogin):
    try:
        sql_query = "CALL Login_sp(%s, %s)"
        cur.execute(sql_query, (user.userid, user.password))
        result = cur.fetchone()
        return result

    except err:
        return err


@app.post('/sessioncheck')
async def session(session: UserModel.Session):
    try:
        sql_query = f"CALL Checksession_sp({session.userid})"
        cur.execute(sql_query)
        result = cur.fetchone()
        returndata = {"status": True, "data": result}
        return returndata
    except err:
        return err


@app.post('/updatesession')
async def sessionupdate(session: UserModel.Session):
    try:
        tuuid = uuid1()
        sql_query = f"CALL update_sessionid_sp({session.userid},{tuuid})"
        cur.execute(sql_query)
        result = cur.fetchone()
        returndata = {"status": True, "data": result, "msg": ''}
        return returndata

    except err:
        return err


@app.post('/getqueries')
async def getqureis(user: UserModel.getQueries):
    try:
        sql_query = f"Call Queries_sp({user.userid})"
        cur.execute(sql_query)
        result = cur.fetchone()
        returndata = {'status': True, "data": result, "msg": ""}
        return returndata
    except err:
        return {'status': False, "data": [], "msg": err}


@app.post('/Insertquery')
async def Insertquery(query: UserModel.newquery):
    try:
        sql_query = f"Call InsertQuery_sp({query.queries},{query.userid},{query.quertype},{query.opendate},{query.closedate},{query.process})"
        cur.execute(sql_query)
        result = cur.fetchone()
        returndata = {"status": True, "data": result, "msg": ""}
        return returndata
    except err:
        return {'status': False, "data": [], "msg": err}


@app.put('/updatequery')
async def updatequery(query: UserModel.updatequery):
    try:
        sql_query = f"Call UpdateQueries_sp({query.id},{query.userid},{query.process},{query.closedate},{query.querytype})"
        cur.execute(sql_query)
        result = cur.fetchone()
        returndata = {"status": True, "data": result, "msg": ""}
        return returndata
    except err:
        return {'status': False, "data": [], "msg": err}


@app.delete('/deletequery')
async def deletequery(query: UserModel.deletequery):
    try:
        sql_query = f"Call DeleteQuries_sp({query.id})"
        cur.execute(sql_query)
        result = cur.fetchone()
        returndata = {"status":True, "data": result, "msg": ""}
        return returndata
    except err:
        return  {'status': False, "data": [], "msg": err}



