import motor.motor_asyncio
from config import DB_URL
database = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
db = database["Entity"]
lb = db["lb"]

#{userid: 857767698795879, username: xyz, display_name: jhfhh, points: 866}
async def get_user(userid):
    data = await lb.find_one({'userid': userid})
    if data:
        sorted_data = await lb.find().sort('points', -1).to_list(None)
        userid_to_data = {item['userid']: {'rank': index, 'username': item['username'], 'display_name': item['display_name'], 'points': item['points']} for index, item in enumerate(sorted_data, start=1)}
        rank = str(userid_to_data[userid]['rank']).zfill(2)
        data['rank'] = rank
    return data

async def give_points(userid, username, display_name, points):
    data = await lb.find_one_and_update({'userid':userid}, {'$inc': {'points': points}})
    if not data:
        await lb.insert_one({'userid': userid, 'username': username, 'display_name': display_name, 'points': points})

async def remove_points(userid, username, display_name, points):
    points = points*-1
    data = await lb.find_one_and_update({'userid':userid}, {'$inc': {'points': points}})
    if not data:
        await lb.insert_one({'userid': userid, 'username': username, 'display_name': display_name, 'points': points})

async def get_lb(interactor_id):
    top_10_string = ""
    sorted_data = await lb.find().sort('points', -1).to_list(None)
    userid_to_data = {item['userid']: {'rank': index, 'username': item['username'], 'display_name': item['display_name'], 'points': item['points']} for index, item in enumerate(sorted_data, start=1)}
    for k, v in userid_to_data.items():
        top_10_string += f"**{str(v['rank']).zfill(2)} • {v['username']} • {v['points']} Points**\n"
        if v['rank'] == 10:
            break
    
    interactor_user = userid_to_data.get(interactor_id)
    if interactor_user:
        if interactor_user['username'] not in top_10_string:
            top_10_string += f"\n**{str(interactor_user['rank']).zfill(2)} • {interactor_user['username']} • {interactor_user['points']} Points**"
    
        return top_10_string

    else:
        return "You're No Ranked In The Leadearboard Try Interacting And Check Back Later!!"

async def admin_lb(rank):
    top_10_string = ""
    sorted_data = await lb.find().sort('points', -1).to_list(None)
    total_data = len(sorted_data)
    if total_data > rank:
        after_rank = sorted_data[rank:]
        docs = after_rank[:10]
        userid_to_data = {item['userid']: {'rank': index, 'username': item['username'], 'display_name': item['display_name'], 'points': item['points']} for index, item in enumerate(docs, start=rank+1)}

        for k, v in userid_to_data.items():
            top_10_string += f"**{str(v['rank']).zfill(2)} • {v['username']} • {v['points']} Points**\n"
        return True, top_10_string
    else:
        return False, f"Only {total_data} users exist in database kindly choose the rank accordingly !!"