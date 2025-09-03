from app.db.session import get_session
from sqlalchemy import text

def test_connection():
    session = get_session()
    result = session.execute(text("SELECT 1")).scalar()
    assert result == 1
    session.close()
