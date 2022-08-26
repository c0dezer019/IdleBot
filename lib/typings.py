# Standard packages
# Standard modules
from datetime import datetime
from typing import Dict, List, TypedDict


class Activity(TypedDict):
    type: str
    location: int
    timestamp: datetime


class IdleStats(TypedDict):
    times_idle: List[int]
    avg_idle_time: int
    previous_avgs: List[int]


class Member(TypedDict):
    id: int
    member_id: int
    username: str
    nickname: str
    last_activity: Activity
    idle_stats: IdleStats
    status: str
    date_added: datetime


class Settings(TypedDict):
    kick_inactive_members: bool
    time_before_inactive: List[int]


class DiscordGuild(TypedDict):
    id: int
    guild_id: int
    name: str
    last_activity: Activity
    idle_stats: IdleStats
    status: str
    settings: Settings
    members: List[Member]


class PurgeList(TypedDict):
    guild_id: int
    member_id: int


class Query(TypedDict):
    query: str
    variables: Dict[str, str]
