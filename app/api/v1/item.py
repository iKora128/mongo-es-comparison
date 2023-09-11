## api_item.py

from fastapi import APIRouter, HTTPException, Depends
from app.schemas import item as Item_schemas
from app.models import item as Item_models
from app.models.item import ItemDocument
from app.db.database import get_engine
from odmantic import AIOEngine


router = APIRouter()

@router.get("/")
async def read_items():
    return [{"name": "Foo"}, {"name": "Bar"}]


@router.get("/es")
def get_all_item():
    items = ItemDocument.search().extra(size=1000).execute()
    return items.to_dict()


@router.get("/mongo", response_model=list[Item_schemas.Item]) 
async def get_all_item(engine: AIOEngine = Depends(get_engine)):
    items = await engine.find(Item_models.Item, limit=1000)
    return items


@router.get("/{item_id}", response_model=Item_schemas.Item)  
async def read_item(item_id: int):
    return {"name": "Fake Specific Item", "item_id": item_id}


@router.post("/mongo", response_model=Item_schemas.Item)
async def create_item(item: Item_schemas.ItemCreate, engine: AIOEngine = Depends(get_engine)):
    item = Item_models.Item(**item.dict())
    await engine.save(item)
    
    if not item:
        raise HTTPException(status_code=400, detail="Item not saved")

    return item


@router.post("/es", response_model=Item_schemas.Item)
def create_item(item: Item_schemas.ItemCreate):
    item_doc = ItemDocument(**item.dict())
    item_doc.save()  # Elasticsearchに保存

    if not item_doc:
        raise HTTPException(status_code=400, detail="Item not saved")

    return item_doc.to_dict()