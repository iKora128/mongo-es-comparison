# odmantic-fastapi

## 内容
元々、odmanticの実験をする場だったのですが
ついでにElasticsearchとの比較、問題となる非同期処理のブロッキングについて一通り調査したものです

またapp内にあるlocustfile.pyで負荷試験とスピードテストを行っています


## ベース
FastAPIのDocumentや周辺レポジトリを参考に、レポジトリ構造やPydanticによるschmea/Model定義を行っています。
大きいアプリの場合にはルーティングが必須で、そういった構造の分け方についても公式やその辺りに準拠しています。

またpythonのversionやライブラリRyeを使っています
個人の環境ではLinterとしてruffを使っています

## API
メインはAPIディレクトリ(app/api/v1)です

odmanic, elasticsearch-dsl, elasticsearch-pyの3つのライブラリを使って
DB操作の比較を行っています


### endpoints
[endpoints]
- es: elasticsearch-dsl
- async-lock-es: elasticsearch-dsl + async-lock
- mongo: odmantic
- es-py: elasticsearch-py

[method]
- GET("/es"): Elasticsearchから1000件取得
- GET("/es/{item_id}"): Elasticsearchから1件取得
- POST("/es"): Elasticsearchに1件保存
それぞれ４×3=12のエンドポイントを用意しています

"async-lock-es"はパスオペレーション関数をasyncで定義しているにも関わらず
内部（DB操作）は同期処理になっているので、lockがかかっている状態です

### 比較内容
mongoとelasticsearch-pyは非同期処理に対応しており、DBの素性をみてる
esはdefでパスオペレーション関数を定義して、async-lock-esはasyncでパスオペレーション関数を定義
すなわち、Async対応していないライブラリなのにAsyncを使うとlockがかかるのでは？ということ

esとes-pyは単純にFastAPIの外部スレッドプールで実行しているか非同期処理なのかの比較

## 結果
DBの速度については
MongoDB > Elasticsearchだが大きくは違わない
(Writeで５倍程度、Readはシャーディングなどの最適化に依存)

上記endpoints/ドライバの結果については
elasticsearch-py ≒ mongo >> es >>>>>> async-lock-es

GETの秒間リクエストについては

(測定環境：MacStduio M1 Max 8コアCPU)
