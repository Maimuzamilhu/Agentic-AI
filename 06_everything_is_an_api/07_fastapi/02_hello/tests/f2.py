from fastapi import FastAPI


app : FastAPI = FastAPI()

@app.get("/notifications/")
async def notifications(filers:str):
    return {"data": f"filer{filers}"}