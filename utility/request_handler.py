from main import logger
from typing import Dict, Optional, TypedDict
from requests import Response
from time import perf_counter
import discord
import requests

api_url_dev = 'http://127.0.0.1:5000/bot/graphql'
api_base_url_prod = 'https://combot.bblankenship.me/v1/'


class Query(TypedDict):
    query: str
    variables: Dict


def get_guild(guild_id: Optional[int] = None):
    payload: Query = {
        'query': '''
            query guild ($guild_id: BigInt!) {
                 guild (guild_id: $guild_id) {
                     code
                     success_msg
                     errors
                     guild {
                         id
                         guild_id
                         name
                         last_activity
                         last_activity_loc
                         last_activity_ts
                         status
                         settings
                         members {
                            id
                            member_id
                            username
                            nickname
                            last_activity
                            last_activity_loc
                            last_activity_ts
                            avg_idle_time
                            idle_time_avgs
                            status
                            date_added
                        }
                         date_added
                     }
                 }
            }
        ''',
        'variables': { 'guild_id': guild_id }

    } if guild_id is not None else {
        'query': '''
            query guilds {
                guilds {
                    code
                    errors
                    guilds {
                        id
                        guild_id
                        name
                        last_activity
                        last_activity_loc
                        last_activity_ts
                        status
                        settings
                        members {
                            member_id
                            username
                            nickname
                            last_activity
                            last_activity_loc
                            last_activity_ts
                            avg_idle_time
                            idle_time_avgs
                            status
                            date_added
                        }
                        date_added
                    }
                }
            }
        '''
    }
    logger.info('Initiating guild query...')

    response: Response = requests.get(api_url_dev, json = payload)

    logger.info('Guild query complete.')

    return response


def add_guild(guild_info: Dict):
    logger.info('Attempting to add a guild...')
    func_start: float = perf_counter()

    logger.info('Searching for pre-existing guild...')

    guild = get_guild(guild_info['guild_id'])

    if guild.status_code == 404:
        logger.info('Guild not found.')
        payload: Query = {
            'query': '''
                    mutation createGuild ($guild_id: BigInt!, $name: String!) {
                        createGuild (guild_id: $guild_id, name: $name) {
                            code
                            success_msg
                            errors
                            guild {
                                id
                                guild_id
                                name
                                last_activity
                                last_activity_loc
                                last_activity_ts
                                avg_idle_time
                                idle_time_avgs
                                status
                                settings
                                date_added
                            }
                        }
                    }
                ''',
            'variables': { k: v for k, v in guild_info.items() }
        }

        logger.info('Adding guild to database...')
        response: Response = requests.post(api_url_dev, json = payload)

        func_end: float = perf_counter()
        time_to_complete: float = func_end - func_start
        logger.info(f'Guild added.\nOperation finished in {time_to_complete} seconds.\nAdded {response.json()}')

        return response

    elif guild.status_code == 200:
        func_end: float = perf_counter()
        time_to_complete: float = func_end - func_start
        logger.info(f'Guild already exists.\nExisting guild:'
                    f'\n\n{guild.json()}')
        logger.info(f'Operation finished in {time_to_complete} seconds.')

        return guild


def add_member(guild_id: int, member: discord.Member):
    payload: Query = {
        'query': '''
            query member ($member_id: BigInt!) {
                member (member_id: $member_id) {
                    code
                    success_msg
                    errors
                    member {
                        id
                        member_id
                        username
                        nickname
                        last_activity
                        last_activity_loc
                        last_activity_ts
                        avg_idle_time
                        idle_time_avgs
                        status
                        date_added
                    }
                }
            }
        ''',
        'variables': { 'member_id': member.id }
    }

    db_member: Response = requests.get(api_url_dev, json = payload)

    if db_member.status_code == 404:
        payload: Query = {
            'query': '''
                    mutation createMember ($guild_id: BigInt!, $member_id: BigInt!, $username: String!, $nickname: String) {
                        createMember (guild_id: $guild_id, member_id: $member_id, username: $username, nickname: $nickname) {
                            code
                            success_msg
                            errors
                            member {
                                id
                                member_id
                                username
                                nickname
                                last_activity
                                last_activity_loc
                                last_activity_ts
                                avg_idle_time
                                idle_time_avgs
                                status
                                date_added
                            }
                        }
                    }
                ''',
            'variables': {
                'guild_id': guild_id,
                'member_id': member.id,
                'username': str(member),
                'nickname': member.nick if member.nick else None,
            }
        }

        response: Response = requests.post(api_url_dev, json = payload)

        if response.status_code == 200:
            pass
        else:
            raise Exception(f'Was unable to add user id {member.id}, username {member.name}#{member.discriminator}')

    else:
        pass

    return 200


def get_member(member_id: Optional[int] = None):
    payload: Query = {
        'query': '''
            query member ($member_id: BigInt!) {
                member (member_id: $member_id) {
                    code
                    success_msg
                    errors
                    member {
                        id
                        member_id
                        username
                        nickname
                        last_activity
                        last_activity_loc
                        last_activity_ts
                        avg_idle_time
                        idle_time_avgs
                        status
                        date_added
                    }
                }
            }
            ''',
        'variables': { 'member_id': member_id }
    } if member_id is not None else {
        'query': '''
            query members {
                members {
                    code
                    errors
                    members{
                        id
                        member_id
                        username
                        nickname
                        last_activity
                        last_activity_loc
                        last_activity_ts
                        avg_idle_time
                        idle_time_avgs
                        status
                        date_added
                    }
                }
            }
        '''
    }

    response: Response = requests.get(api_url_dev, json = payload)

    return response


def update_guild(guild_id: int, **data):
    payload: Query = {
        'query': '''
            mutation updateGuild ($guild_id: BigInt!, $name: String, $last_activity: String, $last_activity_loc: String, $last_activity_ts: DateTime, $status: String) {
                updateGuild (guild_id: $guild_id, name: $name, last_activity: $last_activity, last_activity_loc: $last_activity_loc, last_activity_ts: $last_activity_ts, status: $status) {
                    code
                    success_msg
                    errors
                    guild {
                        id
                        guild_id
                        name
                        last_activity
                        last_activity_loc
                        last_activity_ts
                        avg_idle_time
                        idle_time_avgs
                        status
                        settings
                        date_added
                    }
                }
            }
        ''',
        'variables': {
            'guild_id': guild_id,
        }
    }

    for k, v in data.items():
        payload['variables'][k] = v

    guild: Response = requests.patch(api_url_dev, json = payload)

    if guild.status_code != 200:
        return guild.status_code

    return 200


def update_member(member_id: int, **data):
    payload: Query = {
        'query': '''
            mutation updateMember ($member_id: BigInt!, $nickname: String, $last_activity: String, 
                                   $last_activity_loc: String, $last_activity_ts: DateTime, $status: String) {
                updateMember (member_id: $member_id, nickname: $nickname, last_activity: $last_activity, 
                              last_activity_loc: $last_activity_loc, last_activity_ts: $last_activity_ts,
                              status: $status) {
                    code
                    success_msg
                    errors
                    member {
                        id
                        member_id
                        username
                        nickname
                        last_activity
                        last_activity_loc
                        last_activity_ts
                        avg_idle_time
                        idle_time_avgs
                        status
                        date_added
                    }
                }
            }
        ''',
        'variables': {
            'member_id': member_id,
        }
    }

    for k, v in data.items():
        payload['variables'][k] = v

    member: Response = requests.patch(api_url_dev, json = payload)

    if member.status_code != 200:
        return member.status_code

    return 200


def remove_guild(guild_id: int):
    payload: Query = {
        'query': '''
            mutation deleteGuild ($guild_id: BigInt!) {
                deleteGuild (guild_id: $guild_id) {
                    code
                    success_msg
                    errors
                }
            }
        ''',
        'variables': {
            'guild_id': guild_id
        }
    }

    guild: Response = requests.delete(api_url_dev, json = payload)

    if guild.status_code == 200:
        pass
    else:
        raise


def remove_member(member_id: int):
    payload: Query = {
        'query': '''
            mutation deleteMember ($member_id: BigInt!) {
                deleteMember (member_id: $member_id) {
                    code
                    success_msg
                    errors
                }
            }
        ''',
        'variables': {
            'member_id': member_id
        }
    }

    member: Response = requests.delete(api_url_dev, json = payload)

    if member.status_code == 200:
        pass
    else:
        raise
