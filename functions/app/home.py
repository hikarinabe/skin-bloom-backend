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
    log_docs = db.collection(u'user').document(user_id).collection(u'cosmetic_logs').order_by('create_time', direction="DESCENDING").limit(3).get()

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
    if len(logs) == 0:
        recommend_items = recommend_0["recommend_items"]
        good_ingredient = recommend_0["good_ingredient"]
        bad_ingredient = recommend_0["bad_ingredient"]
    elif len(logs) == 1:
        recommend_items = recommend_1["recommend_items"]
        good_ingredient = recommend_1["good_ingredient"]
        bad_ingredient = recommend_1["bad_ingredient"]
    else:
        recommend_items = recommend_2["recommend_items"]
        good_ingredient = recommend_2["good_ingredient"]
        bad_ingredient = recommend_2["bad_ingredient"]
 
      
    
    
    return https_fn.Response(status=200, response=json.dumps({
        'list_cosmetics': logs,
        'recommend_items': recommend_items,
        'good_ingredient': good_ingredient,
        'bad_ingredient': bad_ingredient
    }), content_type='application/json')



recommend_0 = {
     'recommend_items': [
        {
            "id": "01DKCIR93KatptXG3sno",
            "ingredients": [
                "ジメチコン",
                "グリセリン",
            ],
            "name": "エピステーム HQレーザークリア",
            "price": 7480,
            "company": 130,
            "category": 3,
            "match_rate": 70,
        }, 
        {
            "id": "NwCyFwB7IOkRh3cCjS8T",
            "ingredients": [
                "グリセリン",
                "ＤＰＧ",
                "ＢＧ",
            ],
            "name": "保湿化粧水 とてもしっとりタイプ",
            "price": 770,
            "company": 120,
            "category": 1,
            "match_rate": 68,
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
            "category": 7,
            "match_rate": 56
        }, 
    ],
    # レコメンドの合う成分
    'good_ingredient' : [
        "ナイアシンアミド",
        "ツボクサエキス" ,
        "ヒアルロン酸Ｎａ",
   ],
    # レコメンドの合わない成分
    'bad_ingredient' : [
        "カルボキシビニルポリマー",
        "トコフェロール (天然ビタミンE)",
        "ヤシ油脂肪酸",
    ]
}
     

recommend_1 = {
     'recommend_items': [
        {
            "id": "EBvc3Z5oyXTofirGsNdF",
            "ingredients": [
                "ナイアシンアミド",
                "グリチルリチン酸2K"
            ],
            "name": "肌ラボ 極潤 ハリパーフェクトゲル",
            "price": 1309,
            "company": 130,
            "category": 7,
            "match_rate": 78
        }, 
        {
            "id": "VvDaLpOoAzEZtX35hacY",
            "ingredients": [
                "カンゾウ根エキス",
                "サクラ葉エキス",
                "イチョウ葉エキス",
                "ワイルドタイムエキス",
                "オリーブ葉エキス",
                "ワレモコウエキス",
                "テンチャエキス",
                "ヒアルロン酸Ｎａ",
            ],
            "name": "3D　ビューティーリフティング　セラム",
            "price": 14300,
            "company": 110,
            "category": 3,
            "match_rate": 78
        }, 
       {
        "id": "BNUUzfw5bSAU4qrSXN4u",
        "ingredients": [
            "水",
            "グリセリン",
            "BG"
        ],
        "name": "エピステーム ステムサイエンスリフトクリームb",
        "price": None,
        "company": 130,
        "category": 6,
        "match_rate": 65,
    }
            
    ],
    # レコメンドの合う成分
    'good_ingredient' : [
        "ナイアシンアミド",
        "ヒアルロン酸Ｎａ",
        "カンゾウ根エキス",
   ],
    # レコメンドの合わない成分
    'bad_ingredient' : [
        "トコフェロール (天然ビタミンE)",
        "カルボキシビニルポリマー",
        "ヤシ油脂肪酸",
    ]     
}

recommend_2 = {
     'recommend_items': [
        {
            "id": "JBHItuSYUgFp9wT6xrhm",
            "ingredients": [
                "水",
                "グリセリン",
                "トリ（カプリル酸／カプリン酸）グリセリル",
                "DPG",
                "オレフィンオリゴマー",
                "ペンチレングリコール",
                "PPG-10メチルグルコース",
                "ヒアルロン酸Na",
                "加水分解ヒアルロン酸",
                "アセチルヒアルロン酸Na",
                "乳酸球菌／ヒアルロン酸発酵液",
                "BG",
                "イソステアリン酸PEG-20ソルビタン",
                "PEG-32",
                "PEG-6",
                "ステアリン酸グリセリル",
                "ジメチコン",
                "カルボマー",
                "プロパンジオール",
                "ラウロイルグルタミン酸ジ（フィトステリル／オクチルドデシル）",
                "カプリルヒドロキサム酸",
                "TEA",
                "EDTA-2Na",
                "ステアリルアルコール",
                "ベヘニルアルコール"
            ],
            "name": "肌ラボ 極潤 ヒアルロン乳液",
            "price": None,
            "company": 130,
            "category": 2,
            "match_rate": 85
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
            "category": 7,
            "match_rate": 80
        }, 
        {
            "id": "VvDaLpOoAzEZtX35hacY",
            "ingredients": [
                "カンゾウ根エキス",
                "サクラ葉エキス",
                "イチョウ葉エキス",
                "ワイルドタイムエキス",
                "オリーブ葉エキス",
                "ワレモコウエキス",
                "テンチャエキス",
                "ヒアルロン酸Ｎａ",
            ],
            "name": "3D　ビューティーリフティング　セラム",
            "price": 14300,
            "company": 110,
            "category": 3,
            "match_rate": 72
        },  
    ],
    # レコメンドの合う成分
    'good_ingredient' : [
        "ヒアルロン酸Ｎａ",
        "ナイアシンアミド",
        "カンゾウ根エキス",
   ],
    # レコメンドの合わない成分
    'bad_ingredient' : [
        "オリーブ果実油"
        "トコフェロール (天然ビタミンE)",
        "カルボキシビニルポリマー",
    ]     
     
}
