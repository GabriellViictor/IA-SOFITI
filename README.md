# RBC - Sistema de Recomendação Baseada em Casos

Este projeto é uma API para recomendação de locais, acomodações e procedimentos médicos baseada em dados históricos, construída com FastAPI e machine learning.

---

## Sumário

- [Pré-requisitos](#pré-requisitos)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Rodando o Projeto](#rodando-o-projeto)
  - [Com Docker (Recomendado)](#com-docker-recomendado)
  - [Sem Docker (Ambiente Local)](#sem-docker-ambiente-local)
- [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
- [Utilizando a API](#utilizando-a-api)
  - [Endpoints](#endpoints)
  - [Exemplo de Uso](#exemplo-de-uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Observações e Dicas](#observações-e-dicas)

---

## Pré-requisitos

- Python 3.10+
- PostgreSQL com os dados necessários
- [Docker](https://www.docker.com/products/docker-desktop) (opcional, recomendado)

---

## Configuração do Ambiente
**Configure o arquivo `.env`:**
   Crie um arquivo `.env` na raiz do projeto com as informações do seu banco de dados:
   ```
   DB_HOST=seu_host
   DB_PORT=sua_porta
   DB_NAME=nome_do_banco
   DB_USER=usuario
   DB_PASSWORD=senha
   DB_TEST_NAME=nome_do_banco_teste
   ```

---

## Rodando o Projeto

### Com Docker (Recomendado)

1. **Build da imagem:**
   ```sh
   docker build -t rbc-app ./app
   ```

2. **Execute o container:**
   ```sh
   docker run --env-file .env -p 8000:8000 rbc-app
   ```

3. **Acesse a API:**
   - [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)
   - [http://localhost:8000/health](http://localhost:8000/health)

### Sem Docker (Ambiente Local)

1. **Crie um ambiente virtual e ative:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Execute a aplicação:**
   ```sh
   uvicorn app.main:app --reload        
   ```

---

## Configuração do Banco de Dados

- Certifique-se de que o banco PostgreSQL está acessível e populado com as tabelas e dados necessários.
- Os parâmetros de conexão são definidos no arquivo `.env`.

---

## Utilizando a API

### Endpoints

- **GET `/health`**  
  Verifica se a API está online.

- **POST `/recommend/local`**  
  Recomendação de locais.
  - **Body:**  
    ```json
    {
      "tipogui": "string",
      "codcon": "string",
      "codmed": "string"
    }
    ```
  - **Resposta:**  
    Lista de objetos com `code` e `description`.

- **POST `/recommend/acomodacao`**  
  Recomendação de acomodações.
  - **Body:**  
    ```json
    {
      "tipogui": "string",
      "codcon": "string",
      "codloc": "string",
      "codmed": "string"
    }
    ```
  - **Resposta:**  
    Lista de objetos com `code` e `description`.

- **POST `/recommend/procedimentos`**  
  Recomendação de procedimentos (histórico geral e últimos 6 meses).
  - **Body:**  
    ```json
    {
      "tipogui": "string",
      "codcon": "string",
      "codloc": "string",
      "acomoda": "string",
      "codmed": "string"
    }
    ```
  - **Resposta:**  
    ```json
    {
      "recomendacoes_geral": [
        {"code": "40202038", "description": ""},
        {"code": "40201082", "description": ""}
      ],
      "recomendacoes_6_meses": [
        {"code": "31602231", "description": ""},
        {"code": "40202550", "description": ""}
      ]
    }
    ```
---

## Estrutura do Projeto

```
RBC/
│
├── app/
│   ├── api/           # Rotas da API
│   ├── core/          # Lógica de recomendação e ML
│   ├── database/      # Conexão e queries SQL
│   ├── schemas/       # Schemas Pydantic
│   ├── utils/         # Handlers e utilitários
│   ├── main.py        # Inicialização FastAPI
│   └── Dockerfile     # Dockerfile do projeto
├── requirements.txt
├── .env
└── .gitignore
```
