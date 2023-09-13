## api_item.py
"""
odmanic, elasticsearch-dsl, elasticsearch-pyの3つのライブラリを使って
DB操作の比較を行っています

[endpoints]
- mongo: odmantic
- es: elasticsearch-dsl
- es-py: elasticsearch-py
"""

from fastapi import APIRouter, HTTPException, Depends
from app.schemas import item as Item_schemas
from app.models import item as Item_models
from app.models.item import ItemDocument
from app.db.database import get_engine
from odmantic import AIOEngine
from elasticsearch import AsyncElasticsearch
from odmantic import ObjectId
import asyncio
from time import sleep


router = APIRouter()

sleep_time = 0.3

es = AsyncElasticsearch(hosts=['https://localhost:9200'], 
                              verify_certs=False, 
                              http_auth=('elastic', 'y1X5ohccHph+6XpdRsaB'))

@router.get("/")
async def read_items():
    return [{"name": "Foo"}, {"name": "Bar"}]


@router.get("/es")
def get_items():
    items = ItemDocument.search().extra(size=1000).execute()
    return items.to_dict()

@router.get("/es/{item_id}")
def get_single_item(item_id: str):
    sleep(sleep_time)
    item = ItemDocument.get(id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return item.to_dict()


@router.get("/mongo") # response_model=list[Item_schemas.Item] 
async def get_items(engine: AIOEngine = Depends(get_engine)):
    await asyncio.sleep(sleep_time)
    items = await engine.find(Item_models.Item, limit=1000)
    return items

@router.get("/mongo/{item_id}", response_model=Item_schemas.Item)
async def get_single_item(item_id: ObjectId, engine: AIOEngine = Depends(get_engine)):
    await asyncio.sleep(0.3)
    item = await engine.find_one(Item_models.Item, Item_models.Item.id == item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return item


@router.get("/es-py")
async def get_items():
    await asyncio.sleep(sleep_time)
    items = await es.search(index="item", size=1000)
    return items['hits']['hits']

@router.get("/es-py/{item_id}")
async def get_single_item(item_id: str):
    await asyncio.sleep(sleep_time)
    item = await es.get(index="item", id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return item['_source']


# 以下, post系のエンドポイント
@router.post("/mongo", response_model=Item_schemas.Item)
async def create_item(item: Item_schemas.ItemCreate, engine: AIOEngine = Depends(get_engine)):
    await asyncio.sleep(sleep_time)
    item = Item_models.Item(**item.dict())
    await engine.save(item)
    
    if not item:
        raise HTTPException(status_code=400, detail="Item not saved")

    return item


@router.post("/es", response_model=Item_schemas.Item)
def create_item(item: Item_schemas.ItemCreate):
    sleep(sleep_time)
    item_doc = ItemDocument(**item.dict())
    item_doc.save()  # Elasticsearchに保存

    if not item_doc:
        raise HTTPException(status_code=400, detail="Item not saved")

    return item_doc.to_dict()


@router.post("/es-py", response_model=Item_schemas.Item)
async def create_item(item: Item_schemas.ItemCreate):
    await asyncio.sleep(sleep_time)
    item_doc = item.dict()
    await es.index(index="item", document=item_doc)

    if not item_doc:
        raise HTTPException(status_code=400, detail="Item not saved")

    return Item_schemas.Item(**item_doc)
