from pydantic import *


class User(BaseModel):
    username: str
    email: str
    password: str
    profileimage: str
    role: str
    addinfo: str
    userid: str
    systemno: str
    sessionid: str


class UserLogin(BaseModel):
    userid: str
    password: str


class Session(BaseModel):
    userid: str


class getQueries(BaseModel):
    userid: str


class newquery(BaseModel):
    queries: str
    userid: str
    querytype: str
    opendate: str
    closedate: str
    processtype: str


class updatequery(BaseModel):
    id: int
    userid: str
    process: str
    closedate: str
    querytype: str


class deletequery(BaseModel):
    id: int


class insertasset(BaseModel):
    assetid: str
    grpname: str
    slno: str
    owntype: str
    company: str
    statustyp: str
    assetdescrp: str
    process: str
    gen: str
    ram: str
    hdd: str
    makedescrp: str
    empid: str
    username: str
    dept: str
    loc: str
    remarks: str
    purchasevendor: str
    purchasedate: str
    warantydate: str
    warantystatus: str


class deleteasset(BaseModel):
    id: int
    slno: str


class updateasset(BaseModel):
    id: int
    assetid: str
    grpname: str
    slno: str
    owntype: str
    company: str
    statustyp: str
    assetdescrp: str
    process: str
    gen: str
    ram: str
    hdd: str
    makedescrp: str
    empid: str
    username: str
    dept: str
    loc: str
    remarks: str
    purchasevendor: str
    purchasedate: str
    warantydate: str
    warantystatus: str

class InsertMovement(BaseModel):
    type:str
    imaco:str
    datecol:str
    assetno:str
    empid:str
    empname:str
    dept:str
    location:str
    companies:str
    assettyp:str
    model:str
    assetstickeravial:str
    remarks:str
    serialno:str
    softinstalled:str
    ithead:str
    depthead:str
    hrincharge:str
    returned:str

class DeleteMovement(BaseModel):
    id:int

class GetMovement(BaseModel):
    serialno:str

class UpdateMovement(BaseModel):
    id:int
    type:str
    imacno:str
    datecol:str
    assetno:str
    empid:str
    empname:str
    dept:str
    location:str
    companies:str
    assettyp:str
    model:str
    assetstickeravial:str
    remarks:str
    serialno:str
    softinstalled:str
    ithead:str
    depthead:str
    hrincharge:str
    returned:str

