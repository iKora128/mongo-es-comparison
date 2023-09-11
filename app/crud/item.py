## crud_item.py

from app.db.database import engine
from app.schemas import item as Item_schemas


def save_item(item: Item_schemas.ItemCreate):
    engine.save(item)
    return item