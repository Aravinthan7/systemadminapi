from fastapi import FastAPI

app=FastAPI()

@app.get('/checkservice')
async def root():
    return {"message":"Check Service"}