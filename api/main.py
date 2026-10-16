from fastapi import FastAPI

app = FastAPI(
    title="API de Gestão de Pedidos",
    description="Laboratório de investigação de incidentes em APIs REST",
    version="1.0.0"
)

@app.get("/health")
def verificar_estado():
    return {
        "status": "ok",
        "message": "API em funcionamento"
    }
