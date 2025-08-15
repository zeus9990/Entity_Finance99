import pymongo

database = pymongo.MongoClient("MONGO URI")
db = database["Entity"]
col = db["lb"]

def get_user(userid):
    export_data = {}
    data = col.find_one({'userid': userid})
    if data:
        sorted_data = list(col.find().sort('points', -1))
        for ind, i in enumerate(sorted_data, start=1):
            if i['userid'] == data['userid']:
                data.pop('_id')
                data['rank'] = ind
                break
        export_data['user_data'] = data
        return export_data
    else:
        export_data['user_data'] = None
        return export_data

def lb(rank):
    export_data = {}
    sorted_data = list(col.find().sort('points', -1))
    total_data = len(sorted_data)
    if total_data >= rank:
        data = []
        for ind, i in enumerate(sorted_data[:rank], start=1):
            i.pop('_id')
            i['rank'] = ind
            data.append(i)
        export_data['user_count'] = total_data
        export_data['user_data'] = data
        return export_data
    else:
        export_data['user_count'] = total_data
        export_data['user_data'] = []
        return export_data


print(get_user(38544609826701312))
