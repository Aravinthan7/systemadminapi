from pydantic import *
class User(BaseModel):
    username:str
    email:str
    password:str
    profileimage:str
    role:str
    addinfo:str
    userid:str
    systemno:str
    sessionid:str

class UserLogin(BaseModel):
    userid:str
    password:str

class Session(BaseModel):
    userid:str

class getQueries(BaseModel):
    userid:str
class newquery(BaseModel):
    quries:str
    userid:str
    querytype:str
    opendate:str
    closedate:str
    process:str

class updatequery(BaseModel):
    id:int
    userid:str
    process:str
    closedate:str
    querytype:str
class deletequery(BaseModel):
    id:int
    

