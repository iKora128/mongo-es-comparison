from odmantic import Field, Model
from datetime import datetime

from typing import Optional

class Item(Model):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    price: float = Field(..., gt=0)
    tax: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)



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