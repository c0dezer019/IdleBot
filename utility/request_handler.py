import requests

api_base_url_dev = 'http://127.0.0.1:5000/'
api_base_url_prod = 'https://combot.bblankenship.me/v1/'


def add_server(guild):
    api_add_server = '{0}bot/servers/add'.format(api_base_url_dev)
    api_get_server = '{0}bot/servers/{1}'.format(api_base_url_dev, guild.id)
    server = requests.get(api_get_server)

    if server.status_code == 500:
        packet = { 'server_id': guild.id, 'name': guild.name }
        response = requests.post(api_add_server, packet)

        return response
    else:
        return 200


def add_users(db_users, server_users, guild_id):
    api_add_user = '{0}bot/users/add'.format(api_base_url_dev)
    db_user_ids = []
    errors = []
    response = {}

    for i, v in enumerate(db_users):
        db_user_ids.insert(len(db_user_ids), v.user_id)

    for i, v in enumerate(server_users):
        if v.id not in db_user_ids:
            packet = [{ 'user_id': v.id, 'username': v }, { 'server_id': guild_id }]
            res = requests.post(api_add_user, packet)

            if res.status_code == 200:
                pass
            else:
                return 400

    return response


def handle_users(guild):
    api_get_user = '{0}bot/users'.format(api_base_url_dev)
    res = requests.get(api_get_user)

    if res.status_code == 200:
        users = res.json()
        response = add_users(guild.users, users, guild.server_id)

        return response
    else:
        return res.status_code
