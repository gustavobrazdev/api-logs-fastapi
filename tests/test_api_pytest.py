from fastapi.testclient import TestClient
import main


def test_get_logs_sem_arquivo(tmp_path, monkeypatch):
    caminho = tmp_path / "app.log"

    monkeypatch.setattr(main, "CAMINHO_LOG", caminho)

    cliente = TestClient(main.app)

    resposta = cliente.get("/logs")

    assert resposta.status_code == 200

    assert resposta.json() == {
        "total": 0,
        "logs": []
    }

    assert not caminho.exists()


def test_post_log_valido(tmp_path, monkeypatch):
    caminho = tmp_path / "app.log"

    monkeypatch.setattr(main, "CAMINHO_LOG", caminho)

    cliente = TestClient(main.app)

    resposta = cliente.post(
        "/logs",
        json={
            "level": "INFO",
            "message": "Cadastro concluído."
        }
    )

    assert resposta.status_code == 201

    assert resposta.json() == {
        "status": "registrado",
        "entry": "[INFO] Cadastro concluído."
    }

    assert caminho.read_text(encoding="utf-8") == (
        "[INFO] Cadastro concluído.\n"
    )


def test_post_duas_mensagens_e_get(tmp_path, monkeypatch):
    caminho = tmp_path / "app.log"

    monkeypatch.setattr(main, "CAMINHO_LOG", caminho)

    cliente = TestClient(main.app)

    resposta1 = cliente.post(
        "/logs",
        json={
            "level": "INFO",
            "message": "Cadastro realizado."
        }
    )


    resposta2 = cliente.post(
        "/logs",
        json={
            "level": "WARNING",
            "message": "Estoque baixo."
        }
    )

    assert resposta1.status_code == 201
    assert resposta2.status_code == 201

    conteudo_antes = caminho.read_text(encoding="utf-8")

    resposta_get = cliente.get("/logs")

    assert resposta_get.status_code == 200

    assert resposta_get.json() == {
        "total": 2,
        "logs": [
            "[INFO] Cadastro realizado.",
            "[WARNING] Estoque baixo."
        ]
    }

    conteudo_depois = caminho.read_text(encoding="utf-8")

    assert conteudo_antes == conteudo_depois


def test_post_mensagens_duplicadas(tmp_path, monkeypatch):
    caminho = tmp_path / "app.log"

    monkeypatch.setattr(main, "CAMINHO_LOG", caminho)

    cliente = TestClient(main.app)

    mensagem = {
        "level": "ERROR",
        "message": "Falha ao realizar login."
    }

    resposta1 = cliente.post("/logs", json=mensagem)
    resposta2 = cliente.post("/logs", json=mensagem)

    assert resposta1.status_code == 201
    assert resposta2.status_code == 201

    resposta_get = cliente.get("/logs")

    assert resposta_get.status_code == 200

    assert resposta_get.json() == {
        "total": 2,
        "logs": [
            "[ERROR] Falha ao realizar login.",
            "[ERROR] Falha ao realizar login."
        ]
    }

    assert caminho.read_text(encoding="utf-8") == (
        "[ERROR] Falha ao realizar login.\n"
        "[ERROR] Falha ao realizar login.\n"
    )


def test_post_mensagens_invalidas(tmp_path, monkeypatch):
    caminho = tmp_path / "app.log"

    monkeypatch.setattr(main, "CAMINHO_LOG", caminho)

    cliente = TestClient(main.app)

    # Primeiro, registramos uma mensagem válida
    resposta_valida = cliente.post(
        "/logs",
        json={
            "level": "INFO",
            "message": "Registro válido."
        }
    )

    assert resposta_valida.status_code == 201

    conteudo_antes = caminho.read_text(encoding="utf-8")

    mensagens_invalidas = [
        "",
        "   ",
        None,
        123,
        "Primeira linha\nSegunda linha",
        "Mensagem com\rquebra",
        "A" * 201
    ]

    # Testar cada mensagem inválida
    for mensagem in mensagens_invalidas:
        resposta = cliente.post(
            "/logs",
            json={
                "level": "INFO",
                "message": mensagem
            }
        )

        assert resposta.status_code == 422

        # O arquivo não pode ser modificado
        assert caminho.read_text(encoding="utf-8") == conteudo_antes


def test_limites_e_espacos_mensagem(tmp_path, monkeypatch):
    caminho = tmp_path / "app.log"

    monkeypatch.setattr(main, "CAMINHO_LOG", caminho)

    cliente = TestClient(main.app)

    casos = [
        ("A", "[INFO] A"),
        ("B" * 200, "[INFO] " + "B" * 200),
        ("   Cadastro concluído.   ", "[INFO] Cadastro concluído.")
    ]

    for mensagem, registro_esperado in casos:
        resposta = cliente.post(
            "/logs",
            json={
                "level": "INFO",
                "message": mensagem
            }
        )

        assert resposta.status_code == 201

        assert resposta.json() == {
            "status": "registrado",
            "entry": registro_esperado
        }

    logs = caminho.read_text(encoding="utf-8").splitlines()

    assert logs == [registro for _, registro in casos]


def test_niveis_invalidos(tmp_path, monkeypatch):
    caminho = tmp_path / "app.log"

    monkeypatch.setattr(main, "CAMINHO_LOG", caminho)

    cliente = TestClient(main.app)

    # Primeiro, registrar uma mensagem válida
    resposta_valida = cliente.post(
        "/logs",
        json={
            "level": "INFO",
            "message": "Primeiro registro."
        }
    )

    assert resposta_valida.status_code == 201

    conteudo_antes = caminho.read_text(encoding="utf-8")

    niveis_invalidos = ["DEBUG", "info"]

    for nivel in niveis_invalidos:
        resposta = cliente.post(
            "/logs",
            json={
                "level": nivel,
                "message": "Mensagem de teste."
            }
        )

        assert resposta.status_code == 422

        assert caminho.read_text(encoding="utf-8") == conteudo_antes


def test_campos_obrigatorios_ausentes(tmp_path, monkeypatch):
    caminho = tmp_path / "app.log"

    monkeypatch.setattr(main, "CAMINHO_LOG", caminho)

    cliente = TestClient(main.app)

    # Primeiro, gravamos uma mensagem válida
    resposta_valida = cliente.post(
        "/logs",
        json={
            "level": "INFO",
            "message": "Registro válido."
        }
    )

    assert resposta_valida.status_code == 201

    conteudo_antes = caminho.read_text(encoding="utf-8")

    # Requisições com campos obrigatórios ausentes
    casos_invalidos = [
        {"message": "Cadastro concluído."},
        {"level": "INFO"},
        {}
    ]

    for dados in casos_invalidos:
        resposta = cliente.post("/logs", json=dados)

        assert resposta.status_code == 422

        assert caminho.read_text(encoding="utf-8") == conteudo_antes


def test_falha_gravacao_retorna_500(tmp_path, monkeypatch):
    # Usar uma pasta como se fosse o arquivo de log
    monkeypatch.setattr(main, "CAMINHO_LOG", tmp_path)

    cliente = TestClient(main.app)

    resposta = cliente.post(
        "/logs",
        json={
            "level": "ERROR",
            "message": "Falha no sistema."
        }
    )

    assert resposta.status_code == 500

    assert resposta.json() == {
        "detail": "Não foi possível gravar o log."
    }

def test_falha_leitura_retorna_500(tmp_path, monkeypatch):
    # Utilizar uma pasta no lugar do arquivo de log
    monkeypatch.setattr(main, "CAMINHO_LOG", tmp_path)

    cliente = TestClient(main.app)

    resposta = cliente.get("/logs")

    assert resposta.status_code == 500

    assert resposta.json() == {
        "detail": "Não foi possível ler o log."
    }    