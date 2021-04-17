import requests
import json

api_base_url_dev = 'http://127.0.0.1:5000/'
api_base_url_prod = 'https://combot.bblankenship.me/v1/'


def add_guild(guild_info):
    api_get_guild = f'{api_base_url_dev}bot/guilds/{guild_info["guild_id"]}'
    api_add_guild = f'{api_base_url_dev}bot/guilds/add'
    guild = requests.get(api_get_guild)

    if guild.status_code == 404:
        response = requests.post(api_add_guild, json = guild_info)

        return response
    else:
        return guild


def add_members(guild_members, db_members, guild_id):
    api_add_member = f'{api_base_url_dev}bot/members/add'
    db_member_ids = []
    errors = []
    response = {}

    for i, v in enumerate(db_members):
        db_member_ids.insert(len(db_member_ids), v['member_id'])

    for i, v in enumerate(guild_members):
        if v.id not in db_member_ids:
            packet = { 'member_id': v.id, 'username': f'{v.name}#{v.discriminator}', 'guild_id': guild_id }
            response = requests.post(api_add_member, json = packet)

            if response.status_code == 200:
                response = response.status_code
            else:
                errors.insert(len(errors), {
                    'res_code': response.status_code,
                    'member': { 'id': v.id, 'username': v }
                })

    if len(errors) > 0:
        return response, errors

    return response


def get_guild(guild_id):
    api_get_guild = f'{api_base_url_dev}bot/guilds/{guild_id}'
    response = requests.get(api_get_guild)

    return response.json()


def get_member(member_id):
    api_get_member = f'{api_base_url_dev}bot/guilds/{member_id}'
    response = requests.get(api_get_member)

    return response


def handle_members(guild):
    api_get_members = f'{api_base_url_dev}bot/members'
    res = requests.get(api_get_members)

    if res.status_code == 200:
        members = res.json()
        response = add_members(guild['members'], members, guild['guild_id'])

        return response


def update_guild(guild_id, **data):
    api_get_guild = f'{api_base_url_dev}bot/guilds/{guild_id}'
    data_packet = {}

    for k, v in data.items():
        data_packet[k] = v

    guild = requests.patch(api_get_guild, json = data_packet)

    if guild.status_code != 200:
        return guild.status_code

    return 200


def update_member(member_id, **data):
    api_get_member = f'{api_base_url_dev}bot/members/{member_id}'
    data_packet = {}

    for k, v in data.items():
        data_packet[k] = v

    member = requests.patch(api_get_member, json = data_packet)

    if member.status_code != 200:
        return member.status_code

    return 200
