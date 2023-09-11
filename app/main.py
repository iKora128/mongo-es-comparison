## main.py


from fastapi import FastAPI
from app.api.v1 import user, item
from odmantic import AIOEngine, Model, Field

app = FastAPI()

engine = AIOEngine()


from datetime import datetime
from elasticsearch_dsl import Document, Date, Float, Keyword, Text, connections, Index

# Elasticsearchとのデフォルトの接続を定義
connections.create_connection(hosts=['https://localhost:9200'], 
                              verify_certs=False, 
                              http_auth=('elastic', 'y1X5ohccHph+6XpdRsaB'),
                              )

class ItemDocument(Document):
    name = Text(analyzer='standard', fields={'raw': Keyword()})
    description = Text(analyzer='standard')
    price = Float()
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

def create_index():
    # インデックスが既に存在しない場合のみ作成
    if not ItemDocument._index.exists():
        ItemDocument.init()

# アプリケーションの起動時に呼び出す
create_index()

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(user.router, prefix="/user", tags=["users"])
#app.include_router(api.timeline.router, prefix="/timeline", tags=["home"])
#app.include_router(api.story.router, prefix="/story", tags=["story"])
#app.include_router(api.post.router, prefix="/post", tags=["post"])
#app.include_router(api.effect.router, prefix="/effect", tags=["effect"])
app.include_router(item.router, prefix="/item", tags=["items"])




