🏃‍♀️ Velocidade CAF — Plataforma de Acompanhamento de Performance Atlética










🚀 Visão Geral

O Velocidade CAF é uma aplicação moderna para registro, análise e acompanhamento de desempenho esportivo de atletas e treinadores.
Desenvolvido com FastAPI no backend e CockroachDB como banco distribuído, o projeto visa oferecer uma base sólida e escalável para futuras versões PWA e integração com sensores e APIs esportivas.

🧩 Arquitetura
velocidade-caf/
├── backend/
│   ├── app/
│   │   ├── api/             ← Rotas FastAPI (v1/)
│   │   ├── core/            ← Configs gerais (settings, security)
│   │   ├── db/              ← Conexão e sessão com CockroachDB
│   │   ├── models/          ← Modelos ORM (SQLAlchemy)
│   │   ├── schemas/         ← Schemas Pydantic (entrada e saída)
│   │   ├── services/        ← Lógica de negócio
│   │   └── main.py          ← Aplicação FastAPI principal
│   ├── alembic/             ← Migrações automáticas do banco
│   ├── .env                 ← Variáveis de ambiente
│   ├── requirements.txt
│   └── README.md
└── frontend/
    └── (a ser adicionado: React/Next.js via Netlify)

⚙️ Stack Tecnológica
Camada	Tecnologia	Descrição
Backend	FastAPI
	API moderna e performática em Python
Banco	CockroachDB
	Banco SQL distribuído, compatível com PostgreSQL
ORM	SQLAlchemy 2.0
	Mapeamento objeto-relacional
Migrações	Alembic
	Controle de versão do schema
Validação	Pydantic v2
	Schemas e validações robustas
Deploy (futuro)	Netlify + Render	Frontend e Backend independentes
🧠 Entidades Principais
Entidade	Descrição
User	Usuário base (atleta ou treinador)
AthleteProfile	Perfil completo do atleta
CoachProfile	Perfil profissional do treinador
Jump	Registros de saltos verticais com métricas automáticas
Mark	Marcas de competição/testes com vento e pace calculado
🧰 Instalação Local
1️⃣ Clonar o repositório
git clone https://github.com/mms-11/velocidade-caf.git
cd velocidade-caf/backend

2️⃣ Criar e ativar ambiente virtual
python -m venv .venv
source .venv/Scripts/activate  # Windows PowerShell

3️⃣ Instalar dependências
pip install -r requirements.txt

4️⃣ Subir banco CockroachDB local
docker run -d --name crdb \
  -p 26257:26257 -p 8080:8080 \
  cockroachdb/cockroach:latest start-single-node --insecure

5️⃣ Criar banco caf
docker exec -it crdb ./cockroach sql --insecure -e "CREATE DATABASE caf;"

6️⃣ Configurar .env
DATABASE_URL=cockroachdb+psycopg://root@localhost:26257/caf?sslmode=disable

7️⃣ Rodar migrações
alembic upgrade head

8️⃣ Executar API
uvicorn app.main:app --reload


📍 Acesse: http://127.0.0.1:8000/docs

🧪 Modelos já mapeados

✅ User

✅ AthleteProfile

✅ CoachProfile

✅ Jump

✅ Mark

Com índices, constraints e relacionamentos testados no CockroachDB:

SHOW TABLES FROM caf;

🔄 Próximos Passos
Etapa	Status	Descrição
Schemas Pydantic	✅	Estruturas de entrada e saída
Rotas FastAPI	🔄	CRUDs + filtros (usuários, saltos, marcas)
Serviços	🔄	Regras de negócio (médias, recordes)
Autenticação	⚪	JWT + OAuth Google
Frontend PWA	⚪	React + Netlify
Deploy Backend	⚪	Render / Railway com Cockroach Cloud
👩‍💻 Autora

Mariana Melo dos Santos
💻 Desenvolvedora Backend e Pesquisadora — CIn/UFPE
📧 mms11@cin.ufpe.br

🌐 github.com/mms-11

📄 Licença

Este projeto é distribuído sob a licença MIT
.
Sinta-se livre para usar, estudar e contribuir!

✨ “A performance é consequência da consistência.” — Velocidade CAF
