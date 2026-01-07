from logging.config import fileConfig
import os

from alembic import context
from sqlalchemy import create_engine, pool
from dotenv import load_dotenv

import models  # ต้องมี Base อยู่ในนี้

# โหลด .env
load_dotenv()

# Alembic Config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ใช้ DATABASE_URL ตรง ๆ (dev mode)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not found in .env")

# metadata สำหรับ autogenerate
target_metadata = models.Base.metadata


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    engine = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
