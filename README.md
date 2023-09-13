# odmantic-fastapi

## 内容
元々、odmanticの実験をする場だったのですが
ついでにElasticsearchとの比較、問題となる非同期処理のブロッキングについて一通り調査したものです

またapp内にあるlocustfile.pyで負荷試験とスピードテストを行っています


## ベース
FastAPIのDocumentや周辺レポジトリを参考に、レポジトリ構造やPydanticによるschmea/Model定義を行っています。
大きいアプリの場合にはルーティングが必須で、そういった構造の分け方についても公式やその辺りに準拠しています。


## API
メインはAPIディレクトリ(app/api/v1)です

odmanic, elasticsearch-dsl, elasticsearch-pyの3つのライブラリを使って
DB操作の比較を行っています

[endpoints]
- es: elasticsearch-dsl
- async-lock-es: elasticsearch-dsl + async-lock
- mongo: odmantic
- es-py: elasticsearch-py

- GET("/es"): Elasticsearchから1000件取得
- GET("/es/{item_id}"): Elasticsearchから1件取得
- POST("/es"): Elasticsearchに1件保存
それぞれ４×3=12のエンドポイントを用意しています

"async-lock-es"はパスオペレーション関数をasyncで定義しているにも関わらず
内部（DB操作）は同期処理になっているので、lockがかかっている状態です