from fastapi import FastAPI
from .db import Base, engine
from .routes import router
# cria tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Cobranças 🚀")

# inclui rotas
app.include_router(router)

@app.get("/")
def root():
    return {"msg": "API de Cobranças rodando 🚀"}
