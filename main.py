from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from log_service import CAMINHO_LOG, gravar_log, ler_logs

app = FastAPI()


class LogEntrada(BaseModel):
    level: Literal["INFO", "WARNING", "ERROR"]
    message: str

    @field_validator("message")
    @classmethod
    def validar_mensagem(cls, valor: str) -> str:
        if "\n" in valor or "\r" in valor:
            raise ValueError("A mensagem não pode conter quebras de linha.")

        mensagem = valor.strip()

        if not 1 <= len(mensagem) <= 200:
            raise ValueError("A mensagem deve ter entre 1 e 200 caracteres.")

        return mensagem


@app.post("/logs", status_code=201)
def criar_log(entrada: LogEntrada):
    try:
        registro = gravar_log(
        entrada.level,
        entrada.message,
        caminho=CAMINHO_LOG
        )

        return {
            "status": "registrado",
            "entry": registro
        }

    except OSError:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível gravar o log."
        ) from None

@app.get("/logs")
def consultar_logs():
    try:
        logs = ler_logs(caminho=CAMINHO_LOG)

        return {
            "total": len(logs),
            "logs": logs
        }

    except OSError:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível ler o log."
        )