# ML model on AlibabaCloud Function Compute (template)
## Fun?
- [Funcraft](https://github.com/alibaba/funcraft)
- [VSCode Extention](https://github.com/alibaba/serverless-vscode)

## How to use
### Install docker & nodejs
### Install [Fun](https://github.com/alibaba/funcraft)
- https://www.alibabacloud.com/help/doc-detail/161136.htm

### Configuration Fun
- https://www.alibabacloud.com/help/doc-detail/146702.htm

### clone this repo.
```bash
git clone https://github.com/marufeuille/fc-ml-template
```

### 外部リソースの用意
- 実際のところ、ディレクトリ名は何でも良いが、このドキュメントではmodelsとして扱う
- 外部リソースは例えば、学習済みのモデルやスケーラーなどを指す

```bash
mkdir models
cp ORIGINAL_RESOURCE_DIR/ORIGINAL_RESOURCE ./models/
```

### write code
- 基本的に配下のようにコードは作る
- メインファイル(ここではindex.pyとする)
    - 初期化関数(ここではinitializerとする)及びハンドラ関数を定義する
```python
import XXXX

def initializer(context):
    # initializeしたい中身
    # 1度したら使い回せる処理、例えばDBとの接続、モデルのロード等

def handler(event, context):
    # 処理の中身(モデルを使った予測等)
```

- ヘルパ関数
    - その他使う関数は別ファイルにしてimportして利用する

### template.ymlの作成
- ROS(Resource Orchestration Service)のtemplateファイル。
- イチから作るのは難しいので、以下参考を見ながら作ると良い
    - [template.yml example](https://github.com/alibaba/funcraft/tree/master/examples)
- handlerを指定するときは、例えばindex.py内のmy_handlerを指定したければ、index.my_handlerのようにする。initializerも同じ。
- このディレクトリに付属のtemplate.yml内のService(ml-template) > Properties > NAS: Autoは、コード以外のリソースを利用する場合は基本的にOnにしておいたほうが捗る。
- CodeUriは./としてあるが、こうするとカレントディレクトリ内にあるすべてのファイルをアップロードしてしまう。これを避けるために後半で.funignoreを作成する

### Funfileの作成
- index.py, ヘルパ関数内で使う依存関係やOSのパッケージ(apt), モデルや必要なリソースのコピーを記載する
- Dockerfileによく似た書き方(実際にこれをもとにDockerfileが自動生成されている)
- Funfileはtemplate.yml内に指定したCodeUriに置く

- 例
```
RUNTIME python3
RUN fun-install pip install scikit-learn==0.22.0 -t /mnt/auto
RUN fun-install pip install numpy -t /mnt/auto
RUN fun-install pip install pandas -t /mnt/auto
RUN fun-install pip install h5py -t /mnt/auto
RUN fun-install pip install tensorflow -t /mnt/auto
COPY ./models /mnt/auto/models
```

### .funignore
- codeをdeployするときに、何も書かないと同じディレクトリ内のもの全てがアップロードされてしまう
- 邪魔なので、必要最小限のコードだけアップロードされるようにする

- コード以外のリソースは基本的にNASに置く想定とする

### Let's build

- NAS領域の用意
```bash
fun nas init
```

- 必要パッケージ等の導入
```bash
fun install
```

- NAS領域のSYNC
```bash
fun nas sync
```

- デプロイ
```bash
fun deploy
```
- 以降コードを変更したときはこれを実行する

## Sample
- あとでつくる

## Others
### PAYG vs Subscription
- FunctionComputeは基本的にはPAYGサービスであり、提供されるコンテナがいつ消えるかは指定できない。
- Subscriptionタイプのリソースを契約することで、契約中はコンテナが永続化(少なくとも1日以上は残っていた)
- モデルが大きくロードをいちいちやると辛いケースでは、その利用も検討すること。