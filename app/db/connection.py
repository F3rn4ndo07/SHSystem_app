from __future__ import annotations

import os
from dotenv import load_dotenv

# Carga variables del .env ubicado en la raíz del proyecto
load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "shsystem_app")  #
DB_DRIVER = os.getenv("DB_DRIVER", "psycopg2")  #

DATABASE_URL = f"postgresql+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
