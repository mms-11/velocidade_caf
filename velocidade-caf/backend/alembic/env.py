import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from dotenv import load_dotenv
import app.models.user
import app.models.jump
import app.models.mark


# Carrega .env
load_dotenv()

# Config do Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Importa Base e MODELOS para o autogenerate enxergar
from app.db.session import Base
# IMPORTANTE: importe todos os modelos aqui
import app.models.user  # ex.: User

target_metadata = Base.metadata


def get_url() -> str:
    # Lê do .env
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL não definido no ambiente")
    return url


def run_migrations_offline():
    """Modo offline: gera SQL sem abrir conexão."""
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,   # detecta mudanças de tipo
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Modo online: executa direto no banco (async)."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    async def do_run_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(
                lambda sync_conn: context.configure(
                    connection=sync_conn,
                    target_metadata=target_metadata,
                    compare_type=True,  # detecta mudanças de tipo
                )
            )
            with context.begin_transaction():
                context.run_migrations()

    import asyncio
    asyncio.run(do_run_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
