# Endpoint list

## Auth
| Explanation | Path | Method | Request | Response | Request_sample |
| ---- | ---- | ---- | ---- | ---- | ---- |
|ユーザーの基本情報の登録| /register | POST | email: string <br> password: string | user_id: string | curl --location 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/auth' <br>--form 'email="example@email.com"' <br>--form 'password="123456"' |
|登録ユーザーの基本情報の更新| /register?user_id=<user_id> | PUT | email: string (optional) <br> password: string (optional) | None | curl --location --request PUT 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/auth?user_id=mN2PWNGjHj5z2ED334Bv' <br>--form 'email="example@email.com"' <br>--form 'password="1234"' |


## Login
| Explanation | Path | Method | Request | Response | Request_sample |
| ---- | ---- | ---- | ---- | ---- | ---- |
|ログイン| /login?user_id=<user_id> | GET | None | result: bool | curl --location --request GET 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/login?user_id=YHMi6IE5Bnu8gcItzbld' <br> --form 'email="example@email.com"' <br> --form 'password="123456"' |

## User
| Explanation | Path | Method | Request | Response | Request_sample |
| ---- | ---- | ---- | ---- | ---- | ---- |
|ユーザー情報の登録| /user?user_id=<user_id> | POST | account_name: string <br>sex: string <br>birthday: Date  | user_id: string | curl --location 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/user?user_id=YHMi6IE5Bnu8gcItzbld' <br>--form 'account_name="あやぴ"' <br>--form 'sex="女性"' <br>--form 'birthday="2000-11-01"' |
|ユーザー情報の閲覧| /user?user_id=<user_id> | GET | None | account_name: string <br>sex: string <br>birthday: string | curl --location 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/user?user_id=YHMi6IE5Bnu8gcItzbld&hoge=null' |
|ユーザー情報の更新| /user?user_id=<user_id> | PUT | TD | ccount_name: string <br>sex: string <br>birthday: Date | curl --location --request PUT 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/user?user_id=YHMi6IE5Bnu8gcItzbld' <br>--form 'account_name="たろう"' <br>--form 'sex="男性"' <br>--form 'birthday="2020-05-20"' |
|ユーザーの基本情報と情報の削除| /user?user_id=<user_id> | DELETE | None | None | curl --location --request DELETE 'http://127.0.0.1:5001/hikarinabe-741d2/asia-northeast1/user?user_id=YHMi6IE5Bnu8gcItzbld' |