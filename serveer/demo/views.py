# views.py
from aiohttp import web
import urllib3
import mysqlTest
from settings import config
import json


config = config["wxapp"]


async def test(request):
    print("test successfully")
    return web.Response(text='Hello Aiohttp!{}'.format(
        request.match_info['name']))


async def test_post(request):
    print(request.method)
    data = await request.json()
    print(data)
    return web.json_response({"status": "success"})


async def index(request):
    limit = request.match_info['limit']
    return web.json_response(mysqlTest.index(limit=limit))


def get_specific_activities(request):
    activities_index = request.match_info['activities_index']
    activities_index = activities_index.split(",")
    return web.json_response(mysqlTest.get_specific_activities(
        activities_index=activities_index))


def get_submitted_activities(request):
    openid = request.match_info['openid']
    return web.json_response(mysqlTest.get_submitted_activities(
        openid=openid))


async def do_login(request):
    code = request.match_info['code']
    nickname = request.match_info['nickname']
    appid = config['appid']
    secret = config['secret']
    url = "https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code"\
        .format(appid, secret, code)
    response = urllib3.PoolManager().request("GET", url)

    user_data = json.loads(response.data)
    response_data = mysqlTest.login(openid=user_data["openid"])
    if response_data[0]["status"] != "success":
        mysqlTest.signin(openid=user_data["openid"], nickname=nickname)
        response_data = mysqlTest.login(openid=user_data["openid"])
    response_data = [{"openid": user_data["openid"]}] + response_data
    return web.json_response(response_data)


async def modify_user_activities(request):
    openid = request.match_info['openid']
    activities_index = request.match_info['activities_index'].split(",")
    if activities_index[0] == '0':
        activities_index = []
    return web.json_response(mysqlTest.modify_user_activities(openid=openid,
                                                              activities_index=activities_index))


async def submit_activity(request):
    if request.method != "POST":
        return web.json_response({"status": "fail", "reason": "get POST only"})
    nickname = request.match_info['nickname']
    openid = request.match_info['openid']

    data = await request.json()
    data = dict(data)
    return web.json_response(mysqlTest.submit_activity(data_dict=data, nickname=nickname, openid=openid))


async def delete_activity(request):
    activity_id = request.match_info['activity_id']
    openid = request.match_info['openid']
    return web.json_response(mysqlTest.delete_activity(activity_id=activity_id, openid=openid))


async def join_activity(request):
    activity_id = request.match_info['activity_id']
    openid = request.match_info['openid']
    return web.json_response(mysqlTest.join_activity(activity_id=activity_id, openid=openid, reverse=False))


async def leave_activity(request):
    activity_id = request.match_info['activity_id']
    openid = request.match_info['openid']
    return web.json_response(mysqlTest.join_activity(activity_id=activity_id, openid=openid, reverse=True))
