from fastapi import FastAPI, HTTPException
from pathlib import Path
from pydantic import BaseModel

app = FastAPI()

class PathRequest(BaseModel):
    path: str

BASE_DIR = Path("/app/data")  # Carpeta base dentro del contenedor
BASE_DIR.mkdir(parents=True, exist_ok=True)  # Crear si no existe

@app.get("/")
def read_root():
    return {"message": "File manager up"}

@app.post("/mkdir")
def create_folder(request: PathRequest):
    path = BASE_DIR / request.path
    try:
        path.mkdir(parents=True, exist_ok=True)
        return {"message": f"Carpeta '{request.path}' creada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/touch")
def create_file(request: PathRequest):
    path = BASE_DIR / request.path
    try:
        path.parent.mkdir(parents=True, exist_ok=True)  # Crear directorio si es necesario
        path.touch(exist_ok=True)
        return {"message": f"Archivo '{request.path}' creado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/rm")
def delete_path(request: PathRequest):
    target = BASE_DIR / request.path
    if not target.exists():
        raise HTTPException(status_code=404, detail=f"'{request.path}' no existe")
    try:
        if target.is_dir():
            for item in target.iterdir():
                if item.is_file():
                    item.unlink()
                else:
                    delete_path(PathRequest(path=str(item.relative_to(BASE_DIR))))
            target.rmdir()
        else:
            target.unlink()
        return {"message": f"'{request.path}' eliminado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/exists")
def check_exists(request: PathRequest):
    return {"exists": (BASE_DIR / request.path).exists()}

@app.get("/ls")
def list_directory(request: PathRequest):
    path = BASE_DIR / request.path
    if not path.exists() or not path.is_dir():
        raise HTTPException(status_code=404, detail=f"Directorio '{request.path}' no encontrado")
    return {"content": [p.name for p in path.iterdir()]}

@app.get("/cat")
def read_file(request: PathRequest):
    path = BASE_DIR / request.path
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail=f"Archivo '{request.path}' no encontrado")
    try:
        return {"content": path.read_text()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
