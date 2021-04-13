import requests

api_base_url_dev = 'http://127.0.0.1:5000/'
api_base_url_prod = 'https://combot.bblankenship.me/v1/'


def add_guild(guild):
    api_get_guild = '{0}bot/guilds/{1}'.format(api_base_url_dev, guild['guild_id'])
    api_add_guild = '{0}bot/guilds/add'.format(api_base_url_dev)
    guild = requests.get(api_get_guild)

    if guild.status_code == 400:
        packet = { 'guild_id': guild['guild_id'], 'name': guild['name'] }
        response = requests.post(api_add_guild, json = packet)

        return response
    else:
        return 200


def add_members(guild_members, db_members, guild_id):
    api_add_member = '{0}bot/members/add'.format(api_base_url_dev)
    db_member_ids = []
    errors = []
    response = {}

    for i, v in enumerate(db_members):
        db_member_ids.insert(len(db_member_ids), v)

    for i, v in enumerate(guild_members):
        if v.id not in db_member_ids:
            packet = { 'member_id': v.id, 'membername': f'{v.name}#{v.discriminator}', 'guild_id': guild_id }
            res = requests.post(api_add_member, json = packet)

            if res.status_code == 200:
                response = res
            else:
                errors.insert(len(errors), { 'res_code': res.status_code, 'member': { 'id': v.id, 'membername': v } })

    if len(errors) > 0:
        return response, errors

    return response


def get_guild(guild_id):
    api_get_guild = '{0}bot/guilds/{1}'.format(api_base_url_dev, guild_id)


def handle_members(guild):
    api_get_members = '{0}bot/members'.format(api_base_url_dev)
    res = requests.get(api_get_members)

    if res.status_code == 200:
        members = res.json()
        response = add_members(guild['members'], members, guild['guild_id'])

        return response


def update_guild(guild_id, **data):
    api_get_guild = '{0}bot/guilds/{1}'.format(api_base_url_dev, guild_id)
    data_packet = {}

    for k, v in data.items():
        data_packet[k] = v

    guild = requests.patch(api_get_guild, json = data_packet)

    if guild.status_code != 200:
        return guild.status_code

    return 200


def update_member(member_id, **data):
    api_get_member = '{0}bot/members/{1}'.format(api_base_url_dev, member_id)
    data_packet = {}

    for k, v in data.items():
        data_packet[k] = v

    member = requests.patch(api_get_member, json = data_packet)

    if member.status_code != 200:
        return member.status_code

    return 200
