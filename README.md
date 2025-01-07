# Sistema de Contagem de Valores

Este é um sistema web simples que permite contar a frequência de valores inseridos pelos usuários, com persistência de dados e histórico de registros.

## Funcionalidades

- Interface web para inserção de valores
- Contagem persistente de valores únicos
- Histórico das últimas 10 ocorrências de cada valor
- API RESTful para processamento dos dados
- Armazenamento em SQLite

## Tecnologias Utilizadas

### Frontend
- HTML5
- JavaScript (Vanilla)
- CSS3

### Backend
- Python 3.10.9
- Flask (Framework Web)
- SQLite (Banco de Dados)
- Flask-CORS

## Pré-requisitos

- Python instalado
- Pip (gerenciador de pacotes do Python)

## Instalação

1. Clone o repositório
```bash
git clone https://github.com/Hactchubas/ProgScript
cd AP1\contador-projeto
```

2. Crie um ambiente virtual
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

## Como Executar

1. Ative o ambiente virtual (caso não esteja ativado)
```bash
# Windows
.\venv\Scripts\activate

# Linux/MacOS
source venv/bin/activate
```

2. Inicie o servidor backend
```bash
python app.py
```

3. Abra o arquivo `index.html` em um navegador web

O servidor estará rodando em `http://localhost:5000`

## Estrutura do Projeto

```
contador-projeto/
│
├── app.py              # Servidor Flask (backend)
├── index.html          # Interface do usuário (frontend)
├── requirements.txt    # Dependências do projeto
└── counter.db         # Banco de dados SQLite (criado automaticamente)
```

## API Endpoints

### POST /count
Registra um novo valor e retorna sua contagem atual.

**Corpo da requisição:**
```json
{
    "value": "string"
}
```

**Resposta:**
```json
{
    "status": "success",
    "count": number,
    "message": "string"
}
```

### GET /history/<value>
Retorna o histórico das últimas 10 ocorrências de um valor específico.

**Resposta:**
```json
{
    "status": "success",
    "value": "string",
    "history": ["timestamp1", "timestamp2", ...]
}
```
