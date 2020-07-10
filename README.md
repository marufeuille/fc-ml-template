# AlibabaCloud FC with ML model template
## Fun?
- [Funcraft](https://github.com/alibaba/funcraft)
- [VSCode Extention](https://github.com/alibaba/serverless-vscode)

## Files/Dirs
### code/
- 名前は何でも良い。
- 中身はこれまた名前は何でも良いが、index.py（initializer, handlerが含まれるもの）とそれ以外のヘルパーでは分けたほうが良いと思っている。

### models/
- これまた名前は何でも良いが、モデルや外部リソースは別ディレクトリに格納し、後述するFunfile内でCopyするほうが良さげ

### template.yml
- ROS(Resource Orchestration Service)のtemplateファイル。
- イチから作るのは難しいので、以下参考を見ながら作ると良い
    - [template.yml example](https://github.com/alibaba/funcraft/tree/master/examples)
- handlerを指定するときは、例えばindex.py内のmy_handlerを指定したければ、index.my_handlerのようにする。initializerも同じ。
- Service(ml-template) > Properties > NAS: Autoは、後述するとおりおすすめ設定として記述している

### Funfile
- Functionで動作する環境を定義する。
- ローカルビルド時にはここに書いた指定に従ってコンテナがダウンロードされ、その上で必要パッケージのインストールやローカルリソースがコピーされる。
- 完了後、パッケージやコピーしたリソースはローカルに書き戻される
- これを関数とまとめてアップロードするか,NASにアップロードするかして、FCから見えるようにする。
- 追加となるものの容量が小さければ関数にまとめても良いと思うが、ML系は基本的にまとまった容量があるためNASをおすすめする。
- 関数とまとめてアップロードすると、関数で1行直しただけでも再度アップロードされることになり重たい。(おそらく、FCの起動にも影響する)


- サンプルの場合、Python3系コンテナ内で必要pipパッケージをインストール後、modelsディレクトリの中身を/mnt/auto/modelsにコピーしている(通常、NASがマウントされるのは/mnt/auto)

## Others
### Sync NAS
- Functionをデプロイしただけではだめで、NASとのSyncは別途コマンドを叩く必要あり。

### PAYG vs Subscription
- FunctionComputeは基本的にはPAYGサービスであり、提供されるコンテナがいつ消えるかは指定できない。
- Subscriptionタイプのリソースを契約することで、契約中はコンテナが永続化(少なくとも1日以上は残っていた)
- モデルが大きくロードをいちいちやると辛いケースでは、その利用も検討すること。