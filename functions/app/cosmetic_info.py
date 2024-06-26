import json

from firebase_admin import firestore
from firebase_functions import https_fn
from google.cloud.firestore_v1.base_query import FieldFilter, Or

DEFAULT_PAGE_SIZE=12

def format_response(status, response: str):
    return https_fn.Response(status=status, response=json.dumps({'message': response}), content_type='application/json')

def split_ingredient(ingredient: str):
    sort_split = [] # [[num, [list]], [num, [list]], ...]

    split_a  = ingredient.split('、')
    sort_split.append([len(split_a), split_a])
    
    split_b  = ingredient.split('・')
    sort_split.append([len(split_b), split_b])
    
    split_c  = ingredient.split(',')
    sort_split.append([len(split_c), split_c])
    
    split_d  = ingredient.split('，')
    sort_split.append([len(split_d), split_d])

    sort_split = sorted(sort_split, reverse=True)

    return sort_split[0][1]

def shorten_list(string_list, length=7, ellipsis="..."):
    shortened_list = []
    for string in string_list:
        if len(string) > length:
            shorted_string = string[:length] + ellipsis
        else:
            shorted_string = string
        shortened_list.append(shorted_string)
    return shortened_list

def get_cosmetic_info(req: https_fn.Request):
    cosmetic_id = req.args.to_dict().get('cosmetic_id')
    if cosmetic_id == None:
        return format_response(status=400, response="please specify cosmetic_id")
    
    db = firestore.client()
    doc = db.collection(u'cosmetic_data').document(cosmetic_id).get()    
    if doc.exists == False:
        return format_response(status=404, response="cosmetic not found")
        
    info_dict = doc.to_dict()
    ingredients = split_ingredient(info_dict['raw_ingredients'])

    resp = {
        'id': cosmetic_id,
        'ingredients': ingredients,
        'name': info_dict['name'],
        'price': info_dict['price'], 
        'company': info_dict['company'],
        'category': info_dict['category'],
    } 
    
    return https_fn.Response(status=200, response=json.dumps(resp), content_type='application/json')
    
def search_cosmetic_info(req: https_fn.Request):
    req_data = json.loads(req.data.decode("utf-8"))    
    db = firestore.client()
    doc_ref = db.collection(u'cosmetic_data')

    company = req_data['company'] if 'company' in req_data else None
    if (company != None) and (type(company) == list):
        if len(company) == 1:
            doc_ref = doc_ref.where('company', '==', company[0])
        elif len(company) > 1:
            filter_lst = []
            for c in company:
                filter_lst.append(FieldFilter('company', '==', c))
            doc_ref = doc_ref.where(filter=Or(filter_lst))

    category = req_data['category'] if 'category' in req_data else None
    if (category != None) and (type(category) == list):
        if len(category) == 1:
            doc_ref = doc_ref.where('category', '==', category[0])
        elif len(category) > 1:
            filter_lst = []
            for c in category:
                filter_lst.append(FieldFilter('category', '==', c))
            doc_ref = doc_ref.where(filter=Or(filter_lst))
    
    keyword = req_data['keyword'] if 'keyword' in req_data else None
    if (keyword != None):
        doc_ref = doc_ref.order_by("name",direction="ASCENDING").start_at({"name": keyword})
    
    page_size = req_data['page_size'] if 'page_size' in req_data else DEFAULT_PAGE_SIZE
    doc = doc_ref.limit(page_size).get()
    resp = []
    for d in doc:
        info_dict = d.to_dict()
        ingredients = split_ingredient(info_dict['raw_ingredients'])
        resp.append({
            'id': d.id,
            'ingredients': shorten_list(ingredients),
            'name': info_dict['name'],
            'price': info_dict['price'], 
            'company': info_dict['company'],
            'category': info_dict['category'],
        })

    return https_fn.Response(status=200, response=json.dumps(resp), content_type='application/json')
