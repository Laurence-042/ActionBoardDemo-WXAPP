# routes.py
from views import test, test_post, index, get_specific_activities, get_submitted_activities, \
    modify_user_activities, do_login, submit_activity, delete_activity, join_activity, leave_activity


def setup_routes(app):
    app.router.add_get('/wxapp/test/{name}', test)
    app.router.add_post('/wxapp/test_post', test_post)

    app.router.add_post('/wxapp/submit_activity/{nickname}/{openid}', submit_activity)

    app.router.add_get('/wxapp/do_login/{code}/{nickname}', do_login)
    app.router.add_get('/wxapp/index/{limit}', index)
    app.router.add_get('/wxapp/get_specific_activities/{activities_index}', get_specific_activities)
    app.router.add_get('/wxapp/get_submitted_activities/{openid}', get_submitted_activities)
    app.router.add_get('/wxapp/modify_user_activities/{openid}/{activities_index}', modify_user_activities)
    app.router.add_get('/wxapp/delete_activity/{activity_id}/{openid}', delete_activity)
    app.router.add_get('/wxapp/join_activity/{activity_id}/{openid}', join_activity)
    app.router.add_get('/wxapp/leave_activity/{activity_id}/{openid}', leave_activity)
