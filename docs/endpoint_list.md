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
