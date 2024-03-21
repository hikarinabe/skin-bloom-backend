import json
from datetime import datetime
from zoneinfo import ZoneInfo

from firebase_admin import firestore
from firebase_functions import https_fn
from google.api_core.datetime_helpers import DatetimeWithNanoseconds


def set_str_day(time_item: DatetimeWithNanoseconds):
        date_time = datetime(time_item.year, time_item.month, time_item.day,
              time_item.hour, time_item.minute, time_item.second,
              time_item.nanosecond // 1000)
        if type(date_time) == datetime:
            timestamp_str = datetime.fromtimestamp(time_item.timestamp(), ZoneInfo("Asia/Tokyo"))
            return timestamp_str.strftime('%Y-%m-%dT%H:%M:%S')
        return time_item

def format_response(status, response: str):
    return https_fn.Response(status=status, response=json.dumps({'message': response}), content_type='application/json')


def get_mypage(req: https_fn.Request):
    user_id = req.args.to_dict().get('user_id')

    # ユーザーが最近追加したアイテム
    db = firestore.client()
    log_docs = db.collection(u'user').document(user_id).collection(u'cosmetic_logs').order_by('create_time', direction="descending").limit(3).get()

    logs = []
    for d in log_docs:
        log_dict = d.to_dict()
        one_log = {
            'id': d.id,
            'item_name': log_dict['item_name'],
            'rate': log_dict['rate'],
            'category': log_dict['category'],
            'good_tag': log_dict['good_tag'], 
            'bad_tag': log_dict['bad_tag'],
            'comment': log_dict['comment'],
            'date': set_str_day(log_dict['update_time'])
        } 
    logs.append(one_log)
    

    ###### レコメンド関連
    ## あとでAPI呼ぶ
    # レコメンドのおすすめ商品
    recommend_items = [
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
        }, 
    ]

    # レコメンドの合う成分
    good_ingredient = [
        "ナイアシンアミド",
        "ツボクサエキス" ,
        "ヒアルロン酸Ｎａ",
   ]

    # レコメンドの合わない成分
    bad_ingredient = [
        "カルボキシビニルポリマー",
        "トコフェロール (天然ビタミンE)",
        "ヤシ油脂肪酸",
    ]
    
    return https_fn.Response(status=200, response=json.dumps({
        'list_cosmetics': logs,
        'recommend_items': recommend_items,
        'good_ingredient': good_ingredient,
        'bad_ingredient': bad_ingredient
    }), content_type='application/json')
