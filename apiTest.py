from fastapi import FastAPI
import updateControlLists
import personasSancionadas

listControl=personasSancionadas.personasSancionadas()
controlList=updateControlLists
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Biach"}


@app.get("/control-lists")
async def root():
    return {"response": listControl.recuperar_todos_jsonTest()}