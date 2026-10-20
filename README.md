# API de Logs — AC1

## 1. Sobre o projeto

Desenvolvi essa API utilizando Python e FastAPI com o objetivo de registrar e consultar mensagens de log.

As mensagens são salvas no arquivo `app.log`, permitindo que os registros continuem armazenados mesmo depois que a aplicação é encerrada.

A API trabalha com três níveis de log: `INFO`, `WARNING` e `ERROR`.

## 2. Tecnologias utilizadas

- Python 3.14.6
- FastAPI
- Uvicorn
- Pydantic
- Unittest
- Pytest
- HTTPX

## 3. Estrutura do projeto

```text
log_api/
├── main.py
├── log_service.py
├── requirements.txt
├── README.md
└── tests/
    ├── __init__.py
    ├── test_log_service_unittest.py
    └── test_api_pytest.py
```

- `main.py`: contém as rotas da API e as validações dos dados.
- `log_service.py`: responsável por gravar e ler as mensagens do arquivo.
- `tests/test_log_service_unittest.py`: testes das funções de gravação e leitura.
- `tests/test_api_pytest.py`: testes das rotas da API.
- `tests/__init__.py`: arquivo de inicialização da pasta de testes.
- `requirements.txt`: bibliotecas necessárias para executar o projeto.
- `README.md`: documentação do projeto.
- `resultados_testes.txt`: resultados das execuções dos testes.
- `app.log`: arquivo criado automaticamente quando uma mensagem é registrada.

## 4. Como instalar

Primeiro, é necessário ter o Python instalado.

Dentro da pasta do projeto, crie um ambiente virtual:

`python -m venv .venv`

No Windows, ative o ambiente:

`.\.venv\Scripts\Activate.ps1`

Depois, instale as bibliotecas:

`python -m pip install -r requirements.txt`

## 5. Como executar

Para iniciar a API, execute:

`python -m uvicorn main:app --reload`

Depois, abra a documentação interativa no navegador:

`http://127.0.0.1:8000/docs`

Por essa página, é possível testar as rotas de cadastro e consulta dos logs.

## 6. Funcionalidades

### POST /logs

Essa rota recebe uma mensagem e a salva no arquivo `app.log`.

Exemplo de dados enviados:

`{"level": "INFO", "message": "Cadastro concluído."}`

Quando a mensagem é registrada corretamente, a API retorna HTTP 201 e informa qual registro foi salvo.

### GET /logs

Essa rota consulta as mensagens já registradas.

Ela retorna a quantidade total de registros e uma lista com as mensagens na ordem em que foram gravadas.

Se o arquivo ainda não existir ou estiver vazio, a API retorna HTTP 200 com `{"total": 0, "logs": []}`.

## 7. Validações

Para evitar registros inválidos, coloquei algumas regras na API.

O nível precisa ser `INFO`, `WARNING` ou `ERROR`, exatamente com essas letras.

A mensagem precisa ser um texto com no mínimo 1 e no máximo 200 caracteres. Também são removidos os espaços do início e do fim, e não são permitidas quebras de linha.

Se algum dado estiver inválido, a API retorna HTTP 422 e não grava a mensagem.

Se acontecer algum problema durante a leitura ou gravação do arquivo, a API retorna HTTP 500 com uma mensagem informando o erro.

## 8. Testes automatizados

Criei testes utilizando `unittest` e `pytest` para verificar o funcionamento do projeto.

### Unittest

Usei o `unittest` para testar diretamente as funções do `log_service.py`.

Os testes verificam a criação do arquivo, a gravação de mensagens, os registros duplicados, os caracteres especiais, a persistência e as falhas de leitura e escrita.

Para executar:

`python -m unittest discover -s tests -p "test_log_service_unittest.py" -v`

### Pytest

Usei o `pytest` com o `TestClient` do FastAPI para testar as requisições HTTP.

Os testes verificam as rotas GET e POST, a validação dos dados    