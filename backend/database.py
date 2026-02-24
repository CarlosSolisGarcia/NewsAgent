import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text,
    create_engine,
    declarative_base,
)
from sqlalchemy.orm import Session, sessionmaker

Base = declarative_base()

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class NewsItemDB(Base):
    """Modelo ORM para la tabla news (no confundir con el Pydantic NewsItem en models.py)."""
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    link = Column(String(2000), nullable=False)
    date = Column(DateTime, nullable=True)
    source = Column(String(200), nullable=False)
    summary = Column(Text, default="")


def init_db():
    Base.metadata.create_all(bind=engine)


# --- CRUD ---
def create_news_item(db: Session, *,
                    title: str, link: str, source: str, 
                    summary: str = "", date: datetime | None = None) -> NewsItemDB:
    
    """Crea una noticia y la guarda en la base de datos."""
    item = NewsItemDB(
        title=title,
        link=link,
        source=source,
        summary=summary,
        date=date,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_news_item(db: Session, item_id: int) -> NewsItemDB | None:
    """Obtiene una noticia por id."""
    return db.query(NewsItemDB).filter(NewsItemDB.id == item_id).first()


def get_news_items(db: Session, *, limit: int = 100, source: str | None = None) -> list[NewsItemDB]:
    """Lista las N noticias más recientes (por fecha), con filtro opcional por source."""
    query = (
        db.query(NewsItemDB)
        .order_by(
            NewsItemDB.date.desc().nulls_last(),
            NewsItemDB.id.desc(),
        )
    )
    if source is not None:
        query = query.filter(NewsItemDB.source == source)
    return query.limit(limit).all()


def update_news_item(db: Session, item_id: int, *,
        title: str | None = None, link: str | None = None,
        source: str | None = None, summary: str | None = None,
        date: datetime | None = None) -> NewsItemDB | None:
    
    """Actualiza una noticia por id. Solo se actualizan los campos no None."""
    item = get_news_item(db, item_id)
    if item is None:
        return None
    if title is not None:
        item.title = title
    if link is not None:
        item.link = link
    if source is not None:
        item.source = source
    if summary is not None:
        item.summary = summary
    if date is not None:
        item.date = date
    db.commit()
    db.refresh(item)
    return item


def delete_news_item(db: Session, item_id: int) -> bool:
    """Elimina una noticia por id. Devuelve True si existía y se eliminó."""
    item = get_news_item(db, item_id)
    if item is None:
        return False
    db.delete(item)
    db.commit()
    return True
