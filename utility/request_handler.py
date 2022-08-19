from typing import Dict, Optional, TypedDict
from requests import Response
from time import perf_counter, perf_counter_ns
from typing import List
import discord
import logging
import requests

api_url_dev = 'http://127.0.0.1:5000/bot/graphql'
api_base_url_prod = 'https://combot.bblankenship.me/v1/'


class Query(TypedDict):
    query: str
    variables: Dict


# Will get a specified guild or all guilds if no id is specified.
def get_guilds(guild_id: Optional[int] = None):
    func_start = perf_counter()
    payload: Query = {
        'query': '''
            query guild ($guild_id: BigInt!) {
                code
                success
                message
                errors
                guild {
                    id
                    guild_id
                    name
                    last_activity
                    last_activity_loc
                    last_activity_ts
                    idle_times
                    idle_time_avgs
                    idle_time_avg
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
                       idle_times
                       idle_time_avg
                       idle_time_avgs
                       status
                       date_added
                   }
                   date_added
                }
            }
        ''',
        'variables': { 'guild_id': guild_id }

    } if guild_id is not None else {
        'query': '''
            query guilds {
                code
                success
                message
                errors
                guilds {
                    id
                    guild_id
                    name
                    last_activity
                    last_activity_loc
                    last_activity_ts
                    idle_times
                    idle_time_avgs
                    idle_time_avg
                    status
                    settings
                    members {
                        member_id
                        username
                        nickname
                        last_activity
                        last_activity_loc
                        last_activity_ts
                        idle_times
                        idle_time_avg
                        idle_time_avgs
                        status
                        date_added
                    }
                    date_added
                }
            }
        '''
    }
    logging.info('Initiating guild query...')

    response: Response = requests.get(api_url_dev, json = payload)
    func_end = perf_counter()
    time_to_complete = func_end - func_start

    logging.info('Guild query complete.')
    logging.info(f'Operation finished in {time_to_complete} seconds.\n-------------------------')

    return response


def get_truncated_guild(guild_id: Optional[int] = None):
    func_start = perf_counter()
    payload: Query = {
        'query': '''
            query Guild ($guild_id: BigInt!) {
                code
                success
                message
                errors
                guild (guild_id: $guild_id) {
                    id
                    guild_id
                    settings
                    members {
                        id
                        member_id
                        status
                    }
                }
            }
        ''',
        'variables': {'guild_id': guild_id}
    } if guild_id is not None else {
        'query': '''
            query Guild {
                code
                success
                message
                errors
                guilds {
                    id
                    guild_id
                    members {
                        id
                        member_id
                        status
                    }
                }
            }
        '''
    }

    logging.info('Initiating guild query')

    response: Response = requests.get(api_url_dev, json = payload)
    func_end = perf_counter()
    time_to_complete = func_end - func_start

    logging.info('Guild query complete.')
    logging.info(f'Operation completed in {time_to_complete} seconds.\n')

    return response


def add_guild(guild_info: Dict):
    logging.info('Attempting to add a guild...')
    func_start: float = perf_counter()

    logging.info('Searching for pre-existing guild...')

    guild: Response = get_guilds(guild_info['guild_id'])
    print(guild)

    if guild.status_code == 404:
        logging.info('Guild not found.')
        payload: Query = {
            'query': '''
                    mutation createGuild ($guild_id: BigInt!, $name: String!) {
                        createGuild (guild_id: $guild_id, name: $name) {
                            id
                            guild_id
                            name
                            last_activity
                            last_activity_loc
                            last_activity_ts
                            idle_times
                            idle_time_avg
                            idle_time_avgs
                            status
                            settings
                            date_added
                        }
                    }
                ''',
            'variables': { k: v for k, v in guild_info.items() }
        }

        logging.info('Adding guild to database...')
        response: Response = requests.post(api_url_dev, json = payload)

        func_end: float = perf_counter()
        time_to_complete: float = func_end - func_start
        logging.info(f'Guild added successfully.')
        logging.info(f'Newest Guild:\n\n{response.json()}\n')
        logging.info(f'Operation finished in {time_to_complete} seconds.\n-------------------------')

        return response

    elif guild.status_code == 200:
        func_end: float = perf_counter()
        time_to_complete: float = func_end - func_start
        logging.info(f'Guild already exists.\nExisting guild:'
                     f'\n\n{guild.json()}\n')
        logging.info(f'Operation finished in {time_to_complete} seconds.\n-------------------------')

        return guild


def get_members(member_id: Optional[int] = None):
    func_start: float = perf_counter()

    payload: Query = {
        'query': '''
            query member ($member_id: BigInt!) {
                code
                success
                message
                errors
                member {
                    id
                    member_id
                    username
                    nickname
                    last_activity
                    last_activity_loc
                    last_activity_ts
                    idle_times
                    idle_time_avg
                    idle_time_avgs
                    status
                    date_added
                }
            }
            ''',
        'variables': { 'member_id': member_id }
    } if member_id is not None else {
        'query': '''
            query members {
                code
                success
                message
                errors
                members{
                    id
                    member_id
                    username
                    nickname
                    last_activity
                    last_activity_loc
                    last_activity_ts
                    idle_times
                    idle_time_avg
                    idle_time_avgs
                    status
                    date_added
                }
            }
        '''
    }

    logging.info('Initiating member query...')

    response: Response = requests.get(api_url_dev, json = payload)
    func_end: float = perf_counter()
    time_to_complete: float = func_end - func_start

    logging.info('Query complete.')
    logging.info(f'Operation finished in {time_to_complete} seconds.\n-------------------------')

    return response


def add_member(guild_id: int, member: discord.Member):
    logging.info('Attempting to add a member...')
    logging.info('Checking to see if member exists...')

    func_start: float = perf_counter()
    db_member: Response = get_members(member.id)

    if db_member.status_code == 404:
        logging.info('Member does not exist. Adding member to database...')

        payload: Query = {
            'query': '''
                    mutation createMember ($guild_id: BigInt!, $member_id: BigInt!, $username: String!, $nickname: String) {
                        createMember (guild_id: $guild_id, member_id: $member_id, username: $username, nickname: $nickname) {
                            id
                            member_id
                            username
                            nickname
                            last_activity
                            last_activity_loc
                            last_activity_ts
                            idle_times
                            idle_time_avg
                            idle_time_avgs
                            status
                            date_added
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
        func_end: float = perf_counter()
        time_to_complete = func_end - func_start

        if response.status_code == 200:
            logging.info('Member added successfully.')
            logging.info(f'Newest member:\n\n{response.json()}\n')
            logging.info(f'Operation finished in {time_to_complete} seconds.\n-------------------------')
        else:
            logging.info(f'Was unable to add member. Here\'s the response:\n{response.json()}\n')
            logging.info(f'Operation finished in {time_to_complete} seconds.\n-------------------------')

            raise Exception(f'Was unable to add user id {member.id}, username {member.name}#{member.discriminator}')
    else:
        func_end: float = perf_counter()
        time_to_complete: float = func_end - func_start

        logging.info('Member already exists, doing nothing.')
        logging.info(f'Existing member: \n\n{db_member.json()}')
        logging.info(f'Operation finished in {time_to_complete} seconds\n-------------------------')

    return 200


def update_guild(guild_id: int, **data):
    logging.info('Updating guild...')
    func_start: float = perf_counter()

    payload: Query = {
        'query': '''
            mutation updateGuild ($guild_id: BigInt!, $name: String, $last_activity: String, $last_activity_loc: String, 
                                  $last_activity_ts: DateTime, $idle_times: List, $idle_time_avg: Int,
                                  $idle_time_avgs: List, $status: String) {
                updateGuild (guild_id: $guild_id, name: $name, last_activity: $last_activity, 
                             last_activity_loc: $last_activity_loc, last_activity_ts: $last_activity_ts, 
                             idle_times: $idle_times, idle_time_avg: $idle_time_avg, idle_time_avgs: $idle_time_avgs,
                             status: $status) {
                    id
                    guild_id
                    name
                    last_activity
                    last_activity_loc
                    last_activity_ts
                    idle_times
                    idle_time_avg
                    idle_time_avgs
                    status
                    settings
                    date_added
                }
            }
        ''',
        'variables': {
            'guild_id': guild_id,
        }
    }

    logging.info('Building payload...')

    item_list: List[str] = list(data.keys())
    loop_times: List[float] = []

    for k, v in data.items():
        loop_start: float = perf_counter_ns() / 1000
        payload['variables'][k] = v
        percentage_complete: int = int((item_list.index(k) + 1) / len(item_list) * 100)
        loop_end: float = perf_counter_ns() / 1000
        time_to_complete: float = loop_end - loop_start
        loop_times.append(time_to_complete)

        logging.info(f'Payload {percentage_complete}% complete. {time_to_complete} microseconds.')

        if percentage_complete == 100:
            logging.info('Payload complete.')
            logging.info(f'Items to be patched:\n{payload["variables"]}\n')
            logging.info(f'Operation finished in {sum(loop_times)} microseconds.')

    logging.info('Patching...')

    guild: Response = requests.patch(api_url_dev, json = payload)

    if guild.status_code != 200:
        func_end = perf_counter()
        time_to_complete = func_end - func_start
        logging.error('Patching guild failed.')
        logging.info(f'Operation finished in {time_to_complete} seconds.\n-------------------------')

        return guild.status_code

    func_end = perf_counter()
    time_to_complete = func_end - func_start

    logging.info(f'Operation finished in {time_to_complete} seconds.\n-------------------------')

    return guild


# data - Received as 'nickname', 'last_activity', etc
def update_member(member_id: int, **data):
    func_start: float = perf_counter()

    payload: Query = {
        'query': '''
            mutation updateMember ($member_id: BigInt!, $nickname: String, $last_activity: String, 
                                   $last_activity_loc: String, $last_activity_ts: DateTime, $idle_times: List,
                                   $idle_time_avg: Int, $idle_time_avgs: List, $status: String) {
                updateMember (member_id: $member_id, nickname: $nickname, last_activity: $last_activity, 
                              last_activity_loc: $last_activity_loc, last_activity_ts: $last_activity_ts,
                              idle_times: $idle_times, idle_time_avg: $idle_time_avg, idle_time_avgs: $idle_time_avgs, 
                              status: $status) {
                    id
                    member_id
                    username
                    nickname
                    last_activity
                    last_activity_loc
                    last_activity_ts
                    idle_times
                    idle_time_avg
                    idle_time_avgs
                    status
                    date_added
                }
            }
        ''',
        'variables': {
            'member_id': member_id,
        }
    }

    # Need to DRY this up some.
    item_list: List[str] = list(data.keys())
    loop_times: List[float] = []

    for k, v in data.items():
        loop_start: float = perf_counter_ns() / 1000

        payload['variables'][k] = v

        percentage_complete: int = int((item_list.index(k) + 1) / len(item_list) * 100)
        loop_end: float = perf_counter_ns() / 1000
        time_to_complete: float = loop_end - loop_start
        loop_times.append(time_to_complete)
        logging.info(f'Payload {percentage_complete}% complete. {time_to_complete} microseconds.')

        if percentage_complete == 100:
            logging.info('Payload complete.')
            logging.info(f'Items to be patched:\n{payload["variables"]}\n')
            logging.info(f'Operation finished in {sum(loop_times)} microseconds.')

    logging.info('Patching member...')

    member: Response = requests.patch(api_url_dev, json = payload)

    if member.status_code != 200:
        logging.info('Unable to patch member.')

        return member.status_code

    func_end: float = perf_counter()
    time_to_complete: float = func_end - func_start

    logging.info('Member successfully patched.')
    logging.info(f'Operation finished in {time_to_complete} seconds.\n-------------------------')

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
