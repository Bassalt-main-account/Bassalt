from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    """ Ruta principal que solo devuelve 'Hola' """
    return {"message": "Hola"}
