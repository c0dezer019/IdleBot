# Purge list queries
purge_list_query = """
    query PurgeList {
        code
        success
        message
        errors
        list {
            guildId
            members {
                memberId
            }
        }
    }
"""

delete_purge_entry = """
    mutation DeletePurgeListEntry($memberId: Snowflake!) {
        deletePurgeListEntry(memberId: $memberId) {
            code
            success
            errors
        }
    }
"""

add_to_purge_list = """
    mutation AddToPurgeList($memberId: Snowflake!, $guildId: Snowflake!) {
        addToPurgeList(memberId: $memberId, guildId: $guildId) {
            code
            success
            errors
        }
    }
"""

# Guild queries

create_guild = """
    mutation CreateGuild($input: GuildCreate!) {
        guild {
            createGuild(input: $input) {
                code
                success
                created
                errors
                guild {
                    guildId
                    name
                    status
                    dateAdded
                }
            }
        }
    }
"""

get_guild = """
    query Guild($guild_id: Snowflake!) {
        guild {
            guild(guild_id: $snowflake) {
                code
                success
                created
                errors
                guild {
                    guildId
                    lastAct {
                        ch
                        type
                        ts
                    }
                    idleStats {
                        timesIdle
                        prevAvgs
                    }
                    status
                    settings
                    members {
                       memberId
                       username
                       guildId
                       adminAccess
                       status
                       flags
                       lastAct {
                            ch
                            type
                            ts
                        }
                        idleStats {
                            timesIdle
                            prevAvgs
                        }
                       dateAdded
                    }
                    dateAdded
                }
            }
        }
    }
"""

get_guilds = """
    query Guilds {
        guild {
            guilds {
                code
                success
                errors
                guilds {
                    guildId
                    lastAct {
                        ch
                        type
                        ts
                    }
                    idleStats {
                        timesIdle
                        prevAvgs
                    }
                    status
                    settings
                    members {
                        memberId
                        username
                        guildId
                        adminAccess
                        status
                        flags
                        lastAct {
                            ch
                            type
                            ts
                        }
                        idleStats {
                            timesIdle
                            prevAvgs
                        }
                        dateAdded
                    }
                    dateAdded
                }
            }
        }
    }
"""

update_guild = """
    mutation UpdateGuild(
        $guildId: Snowflake!,
        $input: GuildUpdate!
    ) {
        guild {
            updateGuild(
                guildId: $guildId,
                input: $input
            ) {
                guild {
                    guildId
                    lastAct {
                        ch
                        type
                        ts
                    }
                    idleStats {
                        timesIdle
                        prevAvgs
                    }
                    status
                    settings
                    dateAdded
                }
            }
        }
    }
"""

delete_guild = """
    mutation DeleteGuild($guildId: Snowflake!) {
        deleteGuild(guildId: $guildId) {
            guild {
                code
                success
                errors
            }
        }
    }
"""

# Member queries
get_members = """
    query Members {
        member {
            member {
                code
                success
                errors
                members {
                    memberId
                    username
                    guildId
                    adminAccess
                    status
                    flags
                    lastAct {
                        ch
                        type
                        ts
                    }
                    idleStats {
                        timesIdle
                        prevAvgs
                    }
                    dateAdded
                }
            }
        }
    }
"""

get_member = """
    query GetMember($guildId: Snowflake!, $memberId: Snowflake!) {
        member {
            member(guildId: $guildId, memberId: $memberId) {
                code
                success
                created
                errors
                member {
                    memberId
                    username
                    guildId
                    adminAccess
                    status
                    flags
                    lastAct {
                        ch
                        type
                        ts
                    }
                    idleStats {
                        timesIdle
                        prevAvgs
                    }
                    dateAdded
                }
            }
        }
    }
"""

update_member = """
    mutation UpdateMember(
        $memberId: Snowflake!,
        $guildId: Snowflake!,
        $input: MemberUpdate
    ) {
        member {
            updateMember(
                memberId: $memberId,
                guildId: $guildId,
                input: $input
            ) {
                code
                success
                errors
                member {
                    memberId
                    username
                    guildId
                    adminAccess
                    status
                    flags
                    lastAct {
                        ch
                        type
                        ts
                    }
                    idleStats {
                        timesIdle
                        prevAvgs
                    }
                    dateAdded
                }
            }
        }
    }
"""

delete_member = """
    mutation DeleteMember($memberId: Snowflake!) {
        deleteMember(memberId: $memberId) {
            member {
                code
                success
                errors
            }
        }
    }
"""

add_member = """
  mutation CreateMember($guildId: Snowflake!, $input: MemberCreate!) {
      member {
          createMember(guildId: $guildId, input: $input) {
              code
              success
              created
              errors
              member {
                  memberId
                  username
                  guildId
                  adminAccess
                  dateAdded
                  flags
                  status
              }
          }
      }
  }
"""


# Query mapping for easy access
queries: dict[str, str] = {
    "purge_list": purge_list_query,
    "delete_purge_entry": delete_purge_entry,
    "add_to_purge_list": add_to_purge_list,
    "create_guild": create_guild,
    "get_guild": get_guild,
    "get_guilds": get_guilds,
    "update_guild": update_guild,
    "delete_guild": delete_guild,
    "add_member": add_member,
    "get_member": get_member,
    "get_members": get_members,
    "update_member": update_member,
    "delete_member": delete_member,
}
