from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "¡Hola Mundo desde FastAPI con uv!"}




#uv run fastapi dev main.py