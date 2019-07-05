import mysql.connector
import time
from settings import config


config = config["postgres"]


def index(limit):
    cnn = None
    data = None
    try:
        cnn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))

    cursor = cnn.cursor()
    try:
        sql_query = 'SELECT * FROM wxapp.activities order by id desc limit 0,{};'.format(
            limit)
        cursor.execute(sql_query)
        data = cursor
    except mysql.connector.Error as e:
        print('get index error!{}'.format(e))
    finally:
        json_data = []
        for row in data:
            result = dict()
            result['id'] = row[0]
            result['title'] = row[1]
            result['start_time'] = row[2]
            result['duration'] = row[3]
            result['location'] = row[4]
            result['current_people_num'] = row[5]
            result['max_people_num'] = row[6]
            result['submission_date'] = row[7]
            result['author_nickname'] = row[8]
            result['participant'] = row[10]
            json_data.append(result)
        cursor.close()
        cnn.close()
        return json_data


def login(openid):
    cnn = None
    data = None
    try:
        cnn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))

    cursor = cnn.cursor()
    try:
        sql_query = 'SELECT id, liked_activities_id, joined_activities_id FROM users WHERE openid=\'{}\';'.format(
            openid)
        cursor.execute(sql_query)
        data = cursor
    except mysql.connector.Error as e:
        print('login error!{}'.format(e))
    finally:
        json_data = []
        user_id = ""
        liked_activities_id = ""
        joined_activities_id = ""
        for row in data:
            user_id = row[0]
            liked_activities_id = row[1]
            joined_activities_id = row[2]
        # print("{}, {}".format(username, correct_password))
        if liked_activities_id:
            liked_activities_id = liked_activities_id.split("&")
        if joined_activities_id:
            joined_activities_id = joined_activities_id.split("&")
        json_data.append(
            {"status": "success" if user_id else "fail",
             "liked_activities_id": liked_activities_id,
             "joined_activities_id": joined_activities_id
             })

        cursor.close()
        cnn.close()
        return json_data


def signin(openid, nickname):
    cnn = None
    data = None
    try:
        cnn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))

    cursor = cnn.cursor()
    try:
        sql_query = 'SELECT id FROM users WHERE openid=\'{}\';'.format(openid)
        cursor.execute(sql_query)
        data = cursor
    except mysql.connector.Error as e:
        print('signin error!{}'.format(e))
    finally:
        json_data = []
        user_id = None
        for row in data:
            user_id = row[0]
        # print("{}, {}".format(username, correct_password))
        if not user_id:
            try:
                sql_query = 'insert into users (`openid`, `nickname`) values  (\'{}\', \'{}\');'.format(
                    openid, nickname)
                cursor = cnn.cursor()
                cursor.execute(sql_query)
                cnn.commit()
            except mysql.connector.Error as e:
                print('create_user error!{}'.format(e))
            json_data.append({"status": "success"})
        else:
            json_data.append({"status": "fail"})
        cursor.close()
        cnn.close()
        return json_data


def get_specific_activities(activities_index):
    cnn = None
    data = None
    try:
        cnn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))

    cursor = cnn.cursor()

    try:
        sql_query = 'SELECT * FROM activities WHERE id in ({});'.format(",".join(activities_index))
        cursor.execute(sql_query)
        data = cursor
    except mysql.connector.Error as e:
        print('get_specific_activities error!{}'.format(e))
    finally:
        json_data = []
        for row in data:
            result = dict()
            result['id'] = row[0]
            result['title'] = row[1]
            result['start_time'] = row[2]
            result['duration'] = row[3]
            result['location'] = row[4]
            result['current_people_num'] = row[5]
            result['max_people_num'] = row[6]
            result['submission_date'] = row[7]
            result['author_nickname'] = row[8]
            result['participant'] = row[10]
            json_data.append(result)
        cursor.close()
        cnn.close()
        return json_data


def get_submitted_activities(openid):
    cnn = None
    data = None
    try:
        cnn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))

    cursor = cnn.cursor()

    try:
        sql_query = 'SELECT * FROM wxapp.activities WHERE author_openid=\'{}\';'.format(openid)
        cursor.execute(sql_query)
        data = cursor
    except mysql.connector.Error as e:
        print('get_specific_activities error!{}'.format(e))
    finally:
        json_data = []
        for row in data:
            result = dict()
            result['id'] = row[0]
            result['title'] = row[1]
            result['start_time'] = row[2]
            result['duration'] = row[3]
            result['location'] = row[4]
            result['current_people_num'] = row[5]
            result['max_people_num'] = row[6]
            result['submission_date'] = row[7]
            result['author_nickname'] = row[8]
            json_data.append(result)
        cursor.close()
        cnn.close()
        return json_data


def modify_user_activities(openid, activities_index):
    cnn = None
    try:
        cnn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))

    cursor = cnn.cursor()

    json_data = []
    try:
        activities_index = sorted(set(activities_index), key=activities_index.index)  # 去除重复元素
        activities = '&'.join(activities_index)
        sql_query = 'UPDATE users SET `liked_activities_id` = \'{}\' WHERE (`openid` = \'{}\');'.format(
            activities, openid)
        print(sql_query)
        cursor = cnn.cursor()
        cursor.execute(sql_query)
        cnn.commit()
        json_data.append({"status": "success"})
        json_data.append({"liked_activities_id": activities_index})
    except mysql.connector.Error as e:
        json_data.append({"status": "fail"})
        print('keep_an_eye_on(modify data) error!{}'.format(e))

    cursor.close()
    cnn.close()
    return json_data


def submit_activity(data_dict, nickname, openid):
    cnn = None
    data = None
    try:
        cnn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))

    cursor = cnn.cursor()
    try:
        localtime = time.asctime(time.localtime(time.time()))
        sql_query = 'INSERT INTO activities \
        (`title`, `start_time`, `duration`, `location`, `current_people_num`, `max_people_num`, `submission_date`, `author_nickname`, `author_openid`) \
        VALUES \
        (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');'\
            .format(data_dict["title"], data_dict["start_time"], data_dict["duration"], data_dict["location"], 0, data_dict["max_people_num"], localtime, nickname, openid)
        cursor.execute(sql_query)
        cnn.commit()
        data = True
    except mysql.connector.Error as e:
        print('submit_activity error!{}'.format(e))
    finally:
        json_data = [{"status": "success" if data else "fail"}]

        cursor.close()
        cnn.close()
        return json_data


def delete_activity(activity_id, openid):
    cnn = None
    data = None
    try:
        cnn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))

    cursor = cnn.cursor()
    try:
        sql_query = 'SELECT author_openid FROM activities WHERE id=\'{}\';'.format(activity_id)
        cursor.execute(sql_query)
        data = cursor
    except mysql.connector.Error as e:
        print('delete_activity error!{}'.format(e))
    finally:
        json_data = []
        that_author_openid = None
        for row in data:
            that_author_openid = row[0]
        # print("{}, {}".format(username, correct_password))
        if that_author_openid == openid:
            try:
                sql_query = 'DELETE FROM activities WHERE (`id` = \'{}\');'.format(activity_id)
                print(sql_query)
                cursor = cnn.cursor()
                cursor.execute(sql_query)
                cnn.commit()
                json_data.append({"status": "success"})
            except mysql.connector.Error as e:
                json_data.append({"status": "fail"})
                print('delete_activity(modify data) error!{}'.format(e))
        else:
            json_data.append({"status": "fail", "reason": "not correct openid"})
        cursor.close()
        cnn.close()
        return json_data


def join_activity(activity_id, openid, reverse=False):
    cnn = None
    data = None
    json_data = []
    try:
        cnn = mysql.connector.connect(**config)
    except mysql.connector.Error as e:
        print('connect fails!{}'.format(e))

    cursor = cnn.cursor()
    try:
        sql_query = 'SELECT current_people_num, max_people_num, participant FROM activities WHERE id=\'{}\';'.format(activity_id)
        cursor.execute(sql_query)
        data = cursor
    except mysql.connector.Error as e:
        print('join_activity(get current participant) error!{}'.format(e))
    current_people_num = None
    max_people_num = None
    participant = None
    for row in data:
        current_people_num = row[0]
        max_people_num = row[1]
        participant = row[2]
    check = (current_people_num is not None) and (max_people_num is not None)
    if check:
        check = reverse or current_people_num < max_people_num
    if not check:
        json_data.append({"status": "fail", "reason": "about activity"})
        cursor.close()
        cnn.close()
        return json_data

    try:
        sql_query = 'SELECT nickname, joined_activities_id FROM users WHERE openid=\'{}\';'.format(openid)
        cursor.execute(sql_query)
        data = cursor
    except mysql.connector.Error as e:
        print('join_activity(get nickname) error!{}'.format(e))
    nickname = None
    joined_activities_id = None
    for row in data:
        nickname = row[0]
        joined_activities_id = row[1]
    if nickname is None:
        json_data.append({"status": "fail", "reason": "about user"})
        cursor.close()
        cnn.close()
        return json_data

    if not reverse:
        current_people_num = int(current_people_num)
        current_people_num += 1
        current_people_num = current_people_num.__str__()

        if not participant:
            participant = "[{}]".format(nickname)
        else:
            participant += "&" + "[{}]".format(nickname)

        if not joined_activities_id:
            joined_activities_id = activity_id.__str__()
        else:
            joined_activities_id += "&" + activity_id.__str__()

    else:
        participant = participant.__str__() if participant else ""
        participant = participant.split("&")
        target_nickname = "[" + nickname.__str__() + "]"
        if target_nickname.__str__() in participant:
            participant.pop(participant.index(target_nickname))
            current_people_num = int(current_people_num)
            current_people_num -= 1
            current_people_num = current_people_num.__str__()
        participant = "&".join(participant)

        joined_activities_id = joined_activities_id.__str__()
        joined_activities_id = joined_activities_id.split("&")
        if activity_id.__str__() in joined_activities_id:
            joined_activities_id.pop(joined_activities_id.index(activity_id.__str__()))
        joined_activities_id = "&".join(joined_activities_id)

    try:
        sql_query = 'UPDATE activities SET `current_people_num` = \'{}\', `participant` = \'{}\' WHERE (`id` = \'{}\');'\
            .format(current_people_num, participant, activity_id)
        print(sql_query)
        cursor = cnn.cursor()
        cursor.execute(sql_query)
        cnn.commit()

    except mysql.connector.Error as e:
        json_data.append({"status": "fail"})
        print('join_activity(modify data) error!{}'.format(e))

    try:
        sql_query = 'UPDATE users SET `joined_activities_id` = \'{}\' WHERE (`openid` = \'{}\');'.format(
            joined_activities_id, openid)
        print(sql_query)
        cursor = cnn.cursor()
        cursor.execute(sql_query)
        cnn.commit()
        json_data.append({"status": "success"})
        json_data.append({"joined_activities_id": joined_activities_id.split("&")})
    except mysql.connector.Error as e:
        json_data.append({"status": "fail"})
        print('keep_an_eye_on(modify data) error!{}'.format(e))

    cursor.close()
    cnn.close()
    return json_data

"""
cnn = None
try:
cnn = mysql.connector.connect(**config)
except mysql.connector.Error as e:
print('connect fails!{}'.format(e))
cursor = cnn.cursor()
try:
sql_query = 'select * from targets;'
cursor.execute(sql_query)
data = cursor
except mysql.connector.Error as e:
print('query error!{}'.format(e))
finally:
json_data = []
for row in data:
    result = dict()
    result['id'] = row[0]
    result['name'] = row[1]
    result['sex'] = row[2]
    result['salary'] = row[3]
    result['school'] = row[4]
    result['city'] = row[5]
    result['major'] = row[6]
    result['exp'] = row[7]
    json_data.append(result)

cursor.close()
cnn.close()
return json_data
"""
"""
INSERT INTO `wxapp`.`activities` (`title`, `start_time`, `duration`, `location`, `current_people_num`, `max_people_num`) VALUES ('围观舍友在deadline前的反应', '2108/12/16 18:00', '2小时', '6049', '1', '6');
"""
