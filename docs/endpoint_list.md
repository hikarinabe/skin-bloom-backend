# Endpoint list

## Auth

### ユーザーの基本情報の登録 /register | POST

request:
```
curl --location 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/auth' \
--header 'Authorization: API_KEY' \
--form 'email="example@email.com"' \
--form 'password="123456"'
```

response:
```
aTzO4X1KHIkmcV6PZVne (user_id)
```

### パスワードの更新 /register | PUT
request:
```
curl --location --request PUT 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/auth' \
--header 'Content-Type: application/json' \
--header 'Authorization: API_KEY' \
--data '{
    "user_id": "aTzO4X1KHIkmcV6PZVne",
    "current_password": "123456",
    "new_password": "1234"
}'
```

response:
```
{
    "message": "password updated"
}
```


## Login
### ログイン /login | POST

request:
```
curl --location 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/login' \
--header 'Content-Type: application/json' \
--header 'Authorization: API_KEY' \
--data-raw '{
    "email": "example@email.com",
    "password": "1234"
}'

```

response:
```
{
    "user_id": "aTzO4X1KHIkmcV6PZVne"
}
```

## User

### ユーザー情報の登録 /user | POST 

request:
```
curl --location 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/user' \
--header 'Content-Type: application/json' \
--header 'Authorization: API_KEY' \
--data '{
    "user_id": "aTzO4X1KHIkmcV6PZVne", 
    "account_name": "hoge",
    "sex": "男",
    "birthday": "1900-01-01 00:00:00",
    "nayami": [1,2,3]
}
'
```

response:
```
{
    "message": "Success to create user"
}
```

### ユーザー情報の閲覧 /user?user_id=<user_id> | GET

request:
```
curl --location 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/user?user_id=6KAop6PwbzUydmYsPBDv' \
--header 'Authorization: API_KEY'
```

response:
```
{
    "account_name": "hoge",
    "sex": "男",
    "birthday": "1900-01-01-09:00:00",
    "email": "example@email.com"
    "nayami": [
        1,
        2,
        3
    ],
}
```

### ユーザー情報の更新 /user | PUT

request:
```
curl --location --request PUT 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/user?user_id=6KAop6PwbzUydmYsPBDv' \
--header 'Content-Type: application/json' \
--header 'Authorization: API_KEY' \
--data-raw '{
    "user_id": "6KAop6PwbzUydmYsPBDv",
    "sex": "女",
    "email": "hoge@email.com"
}'
```

response:
```
{
    "message": "User updated"
}
```

### ユーザーの基本情報と情報の削除 /user?user_id=<user_id> | DELETE 

request:
```
curl --location --request DELETE 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/user?user_id=6KAop6PwbzUydmYsPBDv' \
--header 'Authorization: API_KEY'
```

response:
```
{
    "message": "User deleted"
}
```

## CosmeticLog
### Create

request:
```
curl --location 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/cosmetic_log' \
--header 'Content-Type: application/json' \
--header 'Authorization: API_KEY' \
--data '{
    "user_id": "7XFletCT3QvQqzWWt8sb",
    "cosmetic_id": "YYYY",
    "rate": 3.4,
    "category": 2,
    "good_tag": [2, 4],
    "bad_tag": [1, 3], 
    "comment": "test"
}'
```

response:
```
{
    "message": "Success to create log"
}
```

### Get
request:
```
curl --location 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/cosmetic_log?user_id=7XFletCT3QvQqzWWt8sb&cosmetic_id=YYYY' \
--header 'Authorization: API_KEY'
```

response:
```
{
    "id": "YYYY",
    "rate": 3.4,
    "category": 2,
    "good_tag": [
        2,
        4
    ],
    "bad_tag": [
        1,
        3
    ],
    "comment": "test"
}
```

### List
request:
```
curl --location 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/cosmetic_log/list?user_id=7XFletCT3QvQqzWWt8sb' \
--header 'Authorization: API_KEY'
```

response:
```
{
    "list_cosmetics": [
        {
            "id": "XXXX",
            "rate": 4.0,
            "category": 2,
            "good_tag": [
                2,
                4
            ],
            "bad_tag": [
                1,
                3
            ],
            "comment": "test"
        },
        {
            "id": "YYYY",
            "rate": 3.4,
            "category": 2,
            "good_tag": [
                2,
                4
            ],
            "bad_tag": [
                1,
                3
            ],
            "comment": "test"
        }
    ]
}
```

### Update
request:
```
curl --location --request PUT 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/cosmetic_log' \
--header 'Content-Type: application/json' \
--header 'Authorization: API_KEY' \
--data '{
    "user_id": "7XFletCT3QvQqzWWt8sb",
    "cosmetic_id": "YYYY",
    "rate": 4.0
}'

```

response:
```
{
    "message": "Success to update log"
}
```

check update to use GET:
```
{
    "id": "YYYY",
    "rate": 4.0,
    "category": 2,
    "good_tag": [
        2,
        4
    ],
    "bad_tag": [
        1,
        3
    ],
    "comment": "test"
}
```

### Delete
request:
```
curl --location --request DELETE 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/cosmetic_log?user_id=7XFletCT3QvQqzWWt8sb&cosmetic_id=YYYY' \
--header 'Authorization: API_KEY'
```

response:
```
{
    "message": "CosmeticLog is deleted"
}
```

## Cosmetic_info
### Get

request:
```
curl --location 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/cosmetic_info?cosmetic_id=7MLO8LrBYv5prBblQEMR' \
--header 'Authorization: API_KEY'
```

response:
```
{
    "id": "7MLO8LrBYv5prBblQEMR",
    "ingredients": [
        "ミネラルオイル",
        "イソステアリン酸ＰＥＧ－８グリセリル",
        "トリ（カプリル酸／カプリン酸）グリセリル",
        "保湿成分",
        "グリセリン",
        "防腐剤",
        "フェノキシエタノール",
        "メチルパラベン",
        "成分の酸化防止剤",
        "トコフェロール",
        "基剤",
        "水"
    ],
    "name": 5,
    "price": 880,
    "company": 120,
    "category": 5
}
```

### Search

request:
Dataが空の時は全件が返ってくる

```
curl --location 'http://127.0.0.1:8080/hikarinabe-741d2/asia-northeast1/cosmetic_info' \
--header 'Content-Type: application/json' \
--header 'Authorization: API_KEY' \
--data '{
    "category": [6],
    "company": [120]
}'


# 全件
curl --location 'http://127.0.0.1:8080/hikarinabe-741d2/asia-northeast1/cosmetic_info' \
--header 'Content-Type: application/json' \
--header 'Authorization: API_KEY' \
--data '{}'

curl --location 'http://127.0.0.1:8080/hikarinabe-741d2/asia-northeast1/cosmetic_info' \
--header 'Content-Type: application/json' \
--header 'Authorization: API_KEY' \
--data '{
    "category": [],
    "company": []
}'
   
```

response:
```
[
    {
        "id": "7MLO8LrBYv5prBblQEMR",
        "ingredients": [
            "ミネラルオイル",
            "イソステアリン酸ＰＥＧ－８グリセリル",
            "トリ（カプリル酸／カプリン酸）グリセリル",
            "保湿成分",
            "グリセリン",
            "防腐剤",
            "フェノキシエタノール",
            "メチルパラベン",
            "成分の酸化防止剤",
            "トコフェロール",
            "基剤",
            "水"
        ],
        "name": 5,
        "price": 880,
        "company": 120,
        "category": 5
    },
    {
        "id": "FvqSiA54bzdDVyzcEdoN",
        "ingredients": [
            "合成ワックス",
            "ダイマージリノール酸ダイマージリノレイル",
            "ニオイテンジクアオイ油",
            "レモングラス葉油",
            "クレンジング成分",
            "トリイソステアリン酸ＰＥＧ－２０グリセリル",
            "トリイソステアリン酸ＰＥＧ－５グリセリル",
            "防腐剤",
            "フェノキシエタノール",
            "製品の酸化防止剤",
            "トコフェロール",
            "基剤",
            "パルミチン酸エチルヘキシル"
        ],
        "name": 5,
        "price": 1760,
        "company": 120,
        "category": 5
    },
    {
        "id": "R6sKXDiilTE3eUhZnJki",
        "ingredients": [
            "トリエチルヘキサノイン",
            "エチルヘキサン酸セチル",
            "パルミチン酸イソプロピル",
            "ミネラルオイル",
            "保湿成分",
            "グリセリン",
            "ソルビトール",
            "ＰＥＧ－４０",
            "乳化剤",
            "オクチルドデセス－２５",
            "防腐剤",
            "メチルパラベン",
            "プロピルパラベン",
            "成分の酸化防止剤",
            "ヒドロキシアニソール",
            "トコフェロール",
            "基剤",
            "水"
        ],
        "name": 5,
        "price": 660,
        "company": 120,
        "category": 5
    },
    {
        "id": "lTbPTlmMto4wu5NaaUS6",
        "ingredients": [
            "ミネラルオイル",
            "イソノナン酸イソトリデシル",
            "ダイズ油",
            "乳化剤",
            "ステアリン酸ポリグリセリル−10",
            "イソステアリン酸PEG-6",
            "ラウロイルメチルタウリンNa",
            "防腐剤",
            "プロピルパラベン",
            "エチルパラベン",
            "メチルパラベン",
            "製品の酸化防止剤",
            "トコフェロール",
            "基剤",
            "水"
        ],
        "name": 5,
        "price": 880,
        "company": 120,
        "category": 5
    },
    {
        "id": "mxE1wyRoCSceLQRY8N3O",
        "ingredients": [
            "ミネラルオイル",
            "エチルヘキサン酸セチル",
            "油性エモリエント成分",
            "ワセリン",
            "ステアリルアルコール",
            "ステアリン酸",
            "保湿成分",
            "ＰＧ",
            "乳化剤",
            "ポリソルベート６０",
            "ペンタオレイン酸ポリグリセリル－１０",
            "防腐剤",
            "メチルパラベン",
            "プロピルパラベン",
            "ｐＨ調整剤",
            "水酸化Ｋ",
            "製品の酸化防止剤",
            "トコフェロール",
            "成分の酸化防止剤",
            "ＢＨＴ",
            "基剤",
            "水"
        ],
        "name": 5,
        "price": 825,
        "company": 120,
        "category": 5
    },
    {
        "id": "nZrEBHn7ovzA2y4rccN9",
        "ingredients": [
            "ミネラルオイル",
            "エチルヘキサン酸セチル",
            "油性エモリエント成分",
            "ワセリン",
            "ステアリルアルコール",
            "ステアリン酸",
            "保湿成分",
            "ＰＧ",
            "乳化剤",
            "ポリソルベート６０",
            "ペンタオレイン酸ポリグリセリル－１０",
            "防腐剤",
            "メチルパラベン",
            "プロピルパラベン",
            "ｐＨ調整剤",
            "水酸化Ｋ",
            "製品の酸化防止剤",
            "トコフェロール",
            "成分の酸化防止剤",
            "ＢＨＴ",
            "基剤",
            "水"
        ],
        "name": 5,
        "price": 825,
        "company": 120,
        "category": 5
    },
    {
        "id": "xuk9Jhgval5LXOjlCsU3",
        "ingredients": [
            "ラウリルグルコシド",
            "保湿成分",
            "ＢＧ",
            "クレンジング成分",
            "ジイソステアリン酸ポリグリセリル－１０",
            "ＰＥＧ－１２ジメチコン",
            "安定化剤",
            "エタノール",
            "防腐剤",
            "メチルパラベン",
            "プロピルパラベン",
            "ｐＨ調整剤",
            "炭酸Ｎａ",
            "成分の酸化防止剤",
            "トコフェロール",
            "基剤",
            "水"
        ],
        "name": 5,
        "price": 880,
        "company": 120,
        "category": 5
    }
]
```

## homeページの取得
### home GET

request:
```
curl --location 'https://asia-northeast1-hikarinabe-741d2.cloudfunctions.net//home?user_id=F5qsGFCI23UJP5JuK9XN' \
--header 'Authorization: API_key'
```
response:
```
{
    "list_cosmetics": [
        {
            "id": "2fCklSzErUKklOemOm62",
            "item_name": "メラノCC 薬用しみ対策 保湿クリーム",
            "rate": 4.0,
            "category": 2,
            "good_tag": [
                1,
                3
            ],
            "bad_tag": [
                2,
                4
            ],
            "comment": "すごい良かった！",
            "date": "2024-03-20T19:41:51"
        },
        {
            "id": "0rZ44IDAd3v0ca6SWeP3",
            "item_name": "エカクレイスティックパック",
            "rate": 2.0,
            "category": 1,
            "good_tag": [
                1,
                7
            ],
            "bad_tag": [
                8,
                4,
                5
            ],
            "comment": "eeeee",
            "date": "2024-03-20T19:41:12"
        }
    ],
    "recommend_items": [
        {
            "id": "01DKCIR93KatptXG3sno",
            "ingredients": [
                "ジメチコン",
                "グリセリン",
                "PG",
                "ミネラルオイル",
                "（ジメチコン／ビニルジメチコン）クロスポリマー",
                "（ラウリルジメチコン／ポリグリセリン-3）クロスポリマー",
                "水",
                "ハイドロキノン",
                "トコフェロール",
                "ツボクサエキス",
                "アスコルビン酸",
                "水添ポリイソブテン",
                "香料"
            ],
            "name": "エピステーム HQレーザークリア",
            "price": 7480,
            "company": 130,
            "category": 3
        },
        {
            "id": "NwCyFwB7IOkRh3cCjS8T",
            "ingredients": [
                "グリセリン",
                "ＤＰＧ",
                "ＢＧ",
                "ヒアルロン酸Ｎａ",
                "トレハロース",
                "油性エモリエント成分",
                "ラウロイルグルタミン酸ジ（フィトステリル／オクチルドデシル）",
                "トリエチルヘキサノイン",
                "乳化剤",
                "トリイソステアリン酸ＰＥＧ－５０水添ヒマシ油",
                "セテス－２０",
                "可溶化剤",
                "ＰＥＧ－６０水添ヒマシ油",
                "防腐剤",
                "メチルパラベン",
                "プロピルパラベン",
                "ｐＨ調整剤",
                "リンゴ酸Ｎａ",
                "リンゴ酸",
                "成分の酸化防止剤",
                "トコフェロール",
                "基剤",
                "水"
            ],
            "name": "保湿化粧水 とてもしっとりタイプ",
            "price": 770,
            "company": 120,
            "category": 1
        },
        {
            "id": "EBvc3Z5oyXTofirGsNdF",
            "ingredients": [
                "ナイアシンアミド",
                "グリチルリチン酸2K"
            ],
            "name": "肌ラボ 極潤 ハリパーフェクトゲル",
            "price": 1309,
            "company": 130,
            "category": 7
        }
    ],
    "good_ingredient": [
        "ナイアシンアミド",
        "ツボクサエキス",
        "ヒアルロン酸Ｎａ"
    ],
    "bad_ingredient": [
        "カルボキシビニルポリマー",
        "トコフェロール (天然ビタミンE)",
        "ヤシ油脂肪酸"
    ]
}
```
