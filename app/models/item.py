from odmantic import Field, Model
from datetime import datetime
from typing import Optional

## ODMantic style model
class Item(Model):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    price: float = Field(..., gt=0)
    tax: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


## Elasticsearch-dsl style model
from elasticsearch_dsl import Document, Date, Float, Keyword, Text

class ItemDocument(Document):
    name = Text(analyzer='standard', fields={'raw': Keyword()})
    price = Float()
    description = Text(analyzer='standard')
    tax = Float()
    created_at = Date()
    updated_at = Date()

    class Index:
        name = 'items'
        settings = {
            "number_of_shards": 2,
        }

    def save(self, **kwargs):
        self.updated_at = datetime.now()
        return super(ItemDocument, self).save(**kwargs)


## Elasticsearch-py style mapping
from elasticsearch import AsyncElasticsearch

es = AsyncElasticsearch(hosts=['https://localhost:9200'], 
                              verify_certs=False, 
                              http_auth=('elastic', 's3+yOAkxJC4tfPSU6+JP'))

mapping = {
    "mappings": {
        "properties": {
            "name": {
                "type": "text",
                "analyzer": "standard",
                "fields": {
                    "raw": {"type": "keyword"} # name.rawで完全一致検索
                }
            },
            "price": {"type": "float"},
            "description": {"type": "text", "analyzer": "standard"},
            "tax": {"type": "float"},
            "created_at": {"type": "date"},
            "updated_at": {"type": "date"}
        }
    }
}

async def init_item_index():
    if not await es.indices.exists(index="item"):
        await es.indices.create(index="item", body=mapping)

