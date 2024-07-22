from fastapi import FastAPI, Request, HTTPException, Header, status
from DB import db
from Models import UserModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse


# Global variables declared
app = FastAPI()
conn = db.Mysqlconfig.conn
cur = db.Mysqlconfig.cursor
err = db.Mysqlconfig.error
# --------

#Middleware for global authorization
@app.middleware("http")
async def global_auth_middleware(request: Request, call_next):
    # Skip authentication for /docs and /redoc endpoints
    encryptheader=request.headers.get('encryption')
    if encryptheader != None and  encryptheader!= False and  encryptheader!='False' and encryptheader==True:
        pass
    elif encryptheader==False:
        return await call_next(request)
    else:
    # if request.url.path.startswith("/docs") or request.url.path.startswith("/redoc"):
        return await call_next(request)

# Example: Check for Authorization header with Bearer token


@app.get('/checkservice')
async def root(dataencrypt: bool = Header(None), user_agent: str = Header(None),
               x_token: List[str] = Header(None), q: Optional[str] = None) -> dict:
    return {"message": "Check Service", "useragent": user_agent}


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

        return {"status": 200, 'detail': '', "message": message}
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
        result = {
            "status": True,
            "data": [{
                "username": result[0],
                "email": result[1],
                "password": result[3],
                "profileimage": result[4],
                "role": result[5],
                "addinfo": result[6],
                "userid": result[7],
                "systemno": result[8],
                "sessionid": result[9]
            }],
            "msg": ''

        }
        return result

    except err:
        return err


@app.post('/sessioncheck')
async def session(session: UserModel.Session):
    try:
        sql_query = f"CALL Checksession_sp('{session.userid}')"
        cur.execute(sql_query)
        result = cur.fetchone()
        returndata = {"status": True, "data": result}
        return returndata
    except err as e:
        return {'status': False, "data": [], "msg": e}
    finally:
        cur.close()
        conn.close()


@app.post('/updatesession')
async def sessionupdate(session: UserModel.Session):
    try:
        tuuid = uuid1()
        sql_query = f"CALL update_sessionid_sp('{session.userid}','{tuuid}')"
        cur.execute(sql_query)
        result = cur.fetchone()
        returndata = {"status": True, "data": result, "msg": ''}
        return returndata

    except err as e:
        return {'status': False, "data": [], "msg": e}
    finally:
        cur.close()
        conn.close()


@app.post('/getqueries')
async def getqureis(user: UserModel.getQueries):
    try:
        sql_query = f"Call Queries_sp('{user.userid}')"
        cur.execute(sql_query)
        conn.commit()
        result = cur.fetchall()
        returndata = {'status': True, "data": result, "msg": ""}
        return returndata
    except err as e:
        return {'status': False, "data": [], "msg": e}
    finally:
        cur.close()
        conn.close()


@app.post('/Insertquery')
async def Insertquery(query: UserModel.newquery):
    try:
        sql_query = f"CALL InsertQuery_sp('{query.queries}', '{query.userid}', '{query.querytype}', '{query.opendate}', '{query.closedate}', '{query.processtype}')"
        cur.execute(sql_query)
        conn.commit()
        result = cur.fetchone()
        if 'Message' in result:
            result = result['Message']

        returndata = {"status": True, "data": "", "msg": result}
        return returndata
    except err as e:
        conn.rollback()
        return {'status': False, "data": [], "msg": str(e)}
    finally:
        cur.close()
        conn.close()


@app.put('/updatequery')
async def updatequery(query: UserModel.updatequery):
    try:
        sql_query = f"Call UpdateQueries_sp('{query.id}','{query.userid}','{query.process}','{query.closedate}','{query.querytype}')"
        cur.execute(sql_query)
        result = cur.fetchone()
        if 'Message' in result:
            result = result['Message']
        returndata = {"status": True, "data": '', "msg": result}
        return returndata
    except err as e:
        return {'status': False, "data": [], "msg": e}

    finally:
        cur.close()
        conn.close()


@app.delete('/deletequery')
async def deletequery(query: UserModel.deletequery):
    try:
        sql_query = f"Call DeleteQuries_sp({query.id})"
        cur.execute(sql_query)
        result = cur.fetchone()
        if 'Message' in result:
            result = result['Message']
        returndata = {"status": True, "data": "", "msg": result}
        return returndata
    except err as e:
        return {'status': False, "data": [], "msg": e}

    finally:
        cur.close()
        conn.close()


@app.post('/Insertasset')
async def InsertAsset():
    try:
        pass
    except err as e:
        return {'status': False, "data": [], "msg": e}
    finally:
        cur.close()
        conn.close()


@app.get('/GetAsset')
async def GetAsset():
    try:
        sql_query = f"Call GetAsset_sp"
        cur.execute(sql_query)
        result = cur.fetchall()
        returndata = {"status": True, "data": result, "msg": ""}
        return returndata
    except err as e:
        return {'status': False, "data": [], "msg": e}
    finally:
        cur.close()
        conn.close()


@app.post('/UpdateAsset')
async def UpdateAsset(query: UserModel.updateasset):
    try:
        sql_query = f"Call UpdateAsset_sp('{query.id}','{query.assetid}','{query.grpname}','{query.slno}','{query.owntype}','{query.company}','{query.statustyp}','{query.assetdescrp}','{query.process}','{query.gen}','{query.ram}','{query.hdd}','{query.makedescrp}','{query.empid}','{query.username}','{query.dept}','{query.loc}','{query.remarks}','{query.purchasevendor}','{query.purchasedate}','{query.warantydate}','{query.warantystatus}')"
        cur.execute(sql_query)
        result = cur.fetchone()
        if 'Message' in result:
            result = result['Message']
        returndata = {"status": True, "data": '', "msg": result}
        return returndata
    except err as e:
        return {'status': False, "data": [], "msg": e}
    finally:
        cur.close()
        conn.close()

@app.delete('/DeleteAsset')
async def DeleteAsset(query: UserModel.deleteasset):
    try:
        sql_query = f"Call DeleteAsset_sp('{query.id}','{query.slno}')"
        cur.execute(sql_query)
        result = cur.fetchone()
        if 'Message' in result:
            result = result['Message']
        returndata = {"status": True, "data": '', "msg": result}
        return returndata
    except err as e:
        return {'status': False, "data": [], "msg": e}
    finally:
        cur.close()
        conn.close()

@app.post('/InsertMovement')
async def InsertMovement(query: UserModel.InsertMovement):
    try:
        sql_query = f"Call InsertMovement_sp('{query.type}','{query.imaco}','{query.datecol}','{query.assetno}','{query.empid}','{query.empname}','{query.dept}','{query.location}','{query.companies}','{query.assettyp}','{query.model}',{query.assetstickeravial},'{query.remarks}','{query.serialno}','{query.softinstalled}','{query.remarks}','{query.serialno}','{query.softinstalled}','{query.ithead}','{query.depthead}','{query.hrincharge}','{query.returned}')"
        cur.execute(sql_query)
        result = cur.fetchone()
        if 'Message' in result:
            result = result['Message']
        returndata = {"status": True, "data": '', "msg": result}
        return returndata

    except err as e:
        return {'status': False, "data": [], "msg": e}
    finally:
        cur.close()
        conn.close()

@app.put('/UpdateMovement')
async def UpdateMovement(query: UserModel.UpdateMovement):
    try:
        sql_query = f"Call UpdateMovement_sp('{query.id}','{query.type}','{query.imacno}','{query.datecol}','{query.assetno}','{query.empid}','{query.empname}','{query.dept}','{query.location}','{query.companies}','{query.assettyp}','{query.model}','{query.assetstickeravial}','{query.remarks}','{query.serialno}','{query.softinstalled}','{query.ithead}','{query.depthead}','{query.hrincharge}','{query.returned}')"
        cur.execute(sql_query)
        result = cur.fetchone()
        if 'Message' in result:
            result = result['Message']
        returndata = {"status": True, "data": '', "msg": result}
        return returndata
    except err as e:
        return {'status': False, "data": [], "msg": e}
    finally:
        cur.close()
        conn.close()

@app.delete('/DeleteMovement')
async def DeleteMovement(query:UserModel.DeleteMovement):
    try:
        sql_query = f"Call DeleteMovement_sp('{query.id}')"
        cur.execute(sql_query)
        result = cur.fetchone()
        if 'Message' in result:
            result = result['Message']
        returndata = {"status": True, "data": '', "msg": result}
        return returndata
    except err as e:
        return {'status': False, "data": [], "msg": e}
    finally:
        cur.close()
        conn.close()

@app.get('/GetMovement')
async def GetMovement(query:UserModel.GetMovement):
    try:
        sql_query = f"Call GetMovement_sp('{query.serialno}')"
        cur.execute(sql_query)
        result = cur.fetchone()
        if 'Message' in result:
            result = result['Message']
        returndata = {"status": True, "data": '', "msg": result}
        return returndata
    except err as e:
        return {'status': False, "data": [], "msg": e}
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
