from pymongo import MongoClient
from extract_single_page import *
import time

def get_collection():
    mongoC = MongoClient('mongodb://localhost:27017/')
    db = mongoC.opt_doc
    coll = db.first_opt
    return coll

def get_one_record(case_id):
    t = get_single_page(case_id)
    if t == None:
        raise Exception('HttpPostError')
    info = extract_info(t)
    status = extract_status(info)
    date = extract_date(info)
    form = extract_form(info)
    return (date, status, form)

def save_one_record(num, coll):
    case_id = 'YSC1890' + str(num)
    doc = coll.find_one({"case_id": case_id})
    try:
        res = get_one_record(num)
    except Exception as e:
        print(e)
    else:
        #date = str(res[0].year) +'-'+ str(res[0].month) +'-'+ str(res[0].day)
        date = str(res[0])
        if doc == None:
            doc = {'case_id': case_id,
                'form': res[2],
                'detail': [{
                    'date': date,
                    'status': res[1]
                }]}
            coll.insert_one(doc)
        else:
            ori_date_str = doc['detail'][0]['date']
            if date != ori_date_str:
                update_doc = {}
                if doc['form'] == None:
                    update_doc['form'] = res[2]
                doc['detail'].insert(0, {'date': date, 'statue': res[1]})
                update_doc['detail'] = doc['detail']
                print(update_doc)
                coll.update_one({"case_id": doc["case_id"]}, {'$set': update_doc})

if __name__ == '__main__':
    coll = get_collection()
    # start from 168000
    for i in range(168000, 170000):
        print(i)
        save_one_record(i, coll)
        time.sleep(0.5)