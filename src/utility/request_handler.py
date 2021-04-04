import requests

api_base_url_dev = 'http://127.0.0.1:5000/'
api_base_url_prod = 'https://combot.bblankenship.me/v1/'


def add_server(guild):
    api_add_server = '{0}bot/servers/add'.format(api_base_url_dev)
    api_get_server = '{0}bot/servers/{1}'.format(api_base_url_dev, guild['server_id'])
    server = requests.get(api_get_server)

    if server.status_code == 404:
        packet = { 'server_id': guild['server_id'], 'name': guild['name'] }
        response = requests.post(api_add_server, json = packet)

        return response
    else:
        return 200


def add_users(server_users, db_users, guild_id):
    api_add_user = '{0}bot/users/add'.format(api_base_url_dev)
    db_user_ids = []
    errors = []
    response = { }

    for i, v in enumerate(db_users):
        db_user_ids.insert(len(db_user_ids), v.id)

    for i, v in enumerate(server_users):
        if v.id not in db_user_ids:
            packet = { 'user_id': v.id, 'username': f'{v.name}#{v.discriminator}', 'server_id': guild_id }
            res = requests.post(api_add_user, json = packet)

            if res.status_code == 200:
                response = res
            else:
                errors.insert(len(errors), { 'res_code': res.status_code, 'user': { 'id': v.id, 'username': v } })

    if len(errors) > 0:
        return response, errors

    return response


def handle_users(guild):
    api_get_user = '{0}bot/users'.format(api_base_url_dev)
    res = requests.get(api_get_user)

    if res.status_code == 200:
        users = res.json()
        response = add_users(guild['users'], users, guild['server_id'])

        return response
