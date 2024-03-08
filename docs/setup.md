# セットアップ

仮想環境の作成が必要。venvはgithubに上げないように。
```
cd functions
newenvname=venv
python3.12 -m venv $newenvname
source $newenvname/bin/activate
```

必要なライブラリのインストール
```
python3.12 -m pip install -r requirements.txt
```


## アプリケーションの起動
```
firebase emulators:start --debug
```

## デプロイ
ログインして自分のアカウントを選択
```
firebase login
```

デプロイ (python3.12が必要)
```
firebase deploy --only functions
```

