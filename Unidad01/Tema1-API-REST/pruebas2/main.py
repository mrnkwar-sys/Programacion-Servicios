from fastapi import FastAPI
from routers import elfs, presents

app = FastAPI(title="API Christmas Workshop")

app.include_router(elfs.router, prefix="/elfs", tags=["Elfs"])
app.include_router(presents.router, prefix="/presents", tags=["Presents"])


@app.get("/")
def main():
    return {"message": "Welcome to the Christmas Workshop"}
