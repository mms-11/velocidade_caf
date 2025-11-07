<div align="center">

# 🏃‍♀️ Velocidade CAF

### Plataforma de Acompanhamento de Performance Atlética

[![GitHub](https://img.shields.io/badge/GitHub-mms--11-181717?style=for-the-badge&logo=github)](https://github.com/mms-11/velocidade_caf)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![CockroachDB](https://img.shields.io/badge/CockroachDB-6933FF?style=for-the-badge&logo=cockroachdb&logoColor=white)](https://www.cockroachlabs.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

**Desenvolvido por Mariana Melo dos Santos | CIn/UFPE**

[📖 Visão Geral](#-visão-geral) • [🚀 Instalação](#-instalação-local) • [🧩 Arquitetura](#-arquitetura) • [🔄 Roadmap](#-próximos-passos)

</div>

---

## 🚀 Visão Geral

O **Velocidade CAF** é uma aplicação moderna para **registro, análise e acompanhamento de desempenho esportivo** de atletas e treinadores. Desenvolvido com **FastAPI** no backend e **CockroachDB** como banco distribuído, o projeto visa oferecer uma base sólida e escalável para futuras versões PWA e integração com sensores e APIs esportivas.

### 💡 Por que Velocidade CAF?

- 🎯 **Foco em Performance**: Métricas automáticas de saltos, pace e recordes
- 📊 **Análise Profunda**: Acompanhamento histórico e estatísticas avançadas
- 🌐 **Escalável**: Arquitetura distribuída pronta para crescer
- 🔐 **Seguro**: Autenticação JWT e validações robustas
- 📱 **Moderno**: Preparado para evolução PWA

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Stack Tecnológica](#️-stack-tecnológica)
- [Entidades Principais](#-entidades-principais)
- [Arquitetura](#-arquitetura)
- [Instalação Local](#-instalação-local)
- [Modelos do Banco](#-modelos-já-mapeados)
- [Próximos Passos](#-próximos-passos)
- [Autora](#-autora)
- [Licença](#-licença)

---

## ⚙️ Stack Tecnológica

<div align="center">

| Camada | Tecnologia | Descrição |
|--------|-----------|-----------|
| **Backend** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) | API moderna e performática em Python |
| **Banco** | ![CockroachDB](https://img.shields.io/badge/CockroachDB-6933FF?style=flat-square&logo=cockroachdb&logoColor=white) | Banco SQL distribuído, compatível com PostgreSQL |
| **ORM** | ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square) | Mapeamento objeto-relacional 2.0 |
| **Migrações** | ![Alembic](https://img.shields.io/badge/Alembic-8CA1AF?style=flat-square) | Controle de versão do schema |
| **Validação** | ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat-square) | Schemas e validações robustas v2 |
| **Deploy** | ![Netlify](https://img.shields.io/badge/Netlify-00C7B7?style=flat-square&logo=netlify&logoColor=white) + ![Render](https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=white) | Frontend e Backend independentes |

</div>

---

## 🧠 Entidades Principais

| Entidade | Descrição |
|----------|-----------|
| **User** | Usuário base (atleta ou treinador) |
| **AthleteProfile** | Perfil completo do atleta |
| **CoachProfile** | Perfil profissional do treinador |
| **Jump** | Registros de saltos verticais com métricas automáticas |
| **Mark** | Marcas de competição/testes com vento e pace calculado |

---

## 🧩 Arquitetura

```
velocidade-caf/
├── backend/
│   ├── app/
│   │   ├── api/           ← Rotas FastAPI (v1/)
│   │   ├── core/          ← Configs gerais (settings, security)
│   │   ├── db/            ← Conexão e sessão com CockroachDB
│   │   ├── models/        ← Modelos ORM (SQLAlchemy)
│   │   ├── schemas/       ← Schemas Pydantic (entrada e saída)
│   │   ├── services/      ← Lógica de negócio
│   │   └── main.py        ← Aplicação FastAPI principal
│   ├── alembic/           ← Migrações automáticas do banco
│   ├── .env               ← Variáveis de ambiente
│   ├── requirements.txt
│   └── README.md
└── frontend/
    └── (a ser adicionado: React/Next.js via Netlify)
```

---

## 🧰 Instalação Local

### Pré-requisitos

- [Python](https://www.python.org/) 3.8+
- [Docker](https://www.docker.com/) (para CockroachDB)
- [Git](https://git-scm.com)

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/mms-11/velocidade-caf.git
cd velocidade-caf/backend
```

### 2️⃣ Criar e ativar ambiente virtual

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Linux/Mac
source .venv/bin/activate
```

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Subir banco CockroachDB local

```bash
docker run -d \
  --name crdb \
  -p 26257:26257 \
  -p 8080:8080 \
  cockroachdb/cockroach:latest \
  start-single-node --insecure
```

### 5️⃣ Criar banco `caf`

```bash
docker exec -it crdb ./cockroach sql --insecure -e "CREATE DATABASE caf;"
```

### 6️⃣ Configurar `.env`

```bash
DATABASE_URL=cockroachdb+psycopg://root@localhost:26257/caf?sslmode=disable
```

### 7️⃣ Rodar migrações

```bash
alembic upgrade head
```

### 8️⃣ Executar API

```bash
uvicorn app.main:app --reload
```

### 📍 Acesse a documentação interativa

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Modelos já mapeados

✅ **User**  
✅ **AthleteProfile**  
✅ **CoachProfile**  
✅ **Jump**  
✅ **Mark**

Com índices, constraints e relacionamentos testados no CockroachDB:

```sql
SHOW TABLES FROM caf;
