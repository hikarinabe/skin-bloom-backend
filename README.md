# skin-bloom-backend

## Start app in local

仮想環境の作成
```
cd functions
newenvname=venv
python3.12 -m venv $newenvname
source $newenvname/bin/activate
```

start app
```
firebase emulators:start
```

## Documents
- [Setup](https://github.com/hikarinabe/skin-bloom-backend/blob/main/docs/setup.md)

## Deploy

```
firebase deploy --only functions
```
