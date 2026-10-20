from pathlib import Path

CAMINHO_LOG = Path(__file__).resolve().parent / "app.log"


def gravar_log(level, message, caminho=CAMINHO_LOG):
    registro = f"[{level}] {message}"

    with open(caminho, "a", encoding="utf-8") as arquivo:
        arquivo.write(registro + "\n")

    return registro

def ler_logs(caminho=CAMINHO_LOG):
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
            return conteudo.splitlines()

    except FileNotFoundError:
        return []