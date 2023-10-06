import os
from datetime import datetime
import psycopg2

db = psycopg2.connect(os.getenv('RETOOL_DB'))


def get_guild_data(guild_id):
    cursor = db.cursor()
    query = "SELECT * FROM guilds WHERE guild_id = %s"
    cursor.execute(query, (str(guild_id),))
    data = cursor.fetchone()
    cursor.close()
    return data


"""
Existance checks. Functions are to check for existance of data within the DB.

TODO: Add existance check for current guild.
"""


def is_member_in_db(member_id):
    cursor = db.cursor()
    query = """SELECT * from members where member_id = (%s)"""
    cursor.execute(query, (str(member_id),))
    data = cursor.fetchone()
    cursor.close()
    return data


def is_role_in_db(role_id):
    cursor = db.cursor()
    query = """SELECT * from roles where role_id = (%s)"""
    cursor.execute(query, (str(role_id),))
    data = cursor.fetchone()
    cursor.close()
    return data


def is_channel_in_db(channel_id):
    cursor = db.cursor()
    query = """SELECT * from channels where channel_id = (%s)"""
    cursor.execute(query, (str(channel_id),))
    data = cursor.fetchone()
    cursor.close()
    return data


"""
Add data. Functions add data that does NOT exist in the DB.

TODO: Add function to add guild when guild does not exist.
"""


def add_member_to_db(guild_id, member_id, name, avatar, created_at, nickname, display_name, joined_at):
    cursor = db.cursor()
    query = """INSERT 
                INTO members
                    (discord_guild_id, member_id, name, avatar, created_at, nickname, display_name, joined_at, points)
                VALUES((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))
                    """
    cursor.execute(query,
                   (str(guild_id), str(member_id), name, avatar, created_at, nickname, display_name, joined_at, 10))
    db.commit()
    cursor.close()


def add_role_to_db(id_guild, role_id, role_name, position, color, hoisted, mentionable, managed, permissions,
                   created_at, last_synced):
    cursor = db.cursor()
    query = """INSERT 
                INTO roles (
                    discord_guild_id
                    , role_id
                    , role_name
                    , position
                    , color
                    , hoisted
                    , mentionable
                    , managed
                    , permissions
                    , created_at
                    , last_synced
                    )
                VALUES((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))
                    """
    cursor.execute(
        query, (
            str(id_guild)
            , str(role_id)
            , role_name
            , position
            , color
            , hoisted
            , mentionable
            , managed
            , permissions
            , created_at
            , last_synced
        )
    )
    db.commit()
    cursor.close()


def add_channel_to_db(guild_id, channel_id, name, category, position, mention, jump_url, permissions_synced, overwrites,
                      created_at, last_synced):
    cursor = db.cursor()
    query = """INSERT 
                INTO channels (
                    discord_guild_id
                    , channel_id
                    , channel_name
                    , category
                    , position
                    , mention
                    , jump_url
                    , permissions_synced
                    , overwrites
                    , created_at
                    , last_synced
                    )
                VALUES((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))
                    """
    cursor.execute(
        query, (
            str(guild_id)
            , str(channel_id)
            , name
            , category
            , position
            , mention
            , jump_url
            , permissions_synced
            , overwrites
            , created_at
            , last_synced
        )
    )
    db.commit()
    cursor.close()


"""
Update data. Functions update data that already exists in the DB.

"""


def update_guild_info(g_name, g_logo, g_created_at, g_member_count, g_nsfw_level, g_language, dt_now, guild_id):
    cursor = db.cursor()
    query = """UPDATE
                    guilds
                SET
                    name = (%s)
                  , logo = (%s)
                  , created_at = (%s)
                  , member_count = (%s)
                  , nsfw_level = (%s)
                  , language = (%s)
                  , last_sync = (%s)
                WHERE
                    guild_id = (%s)"""
    cursor.execute(
        query
        , (g_name
           , g_logo
           , g_created_at
           , g_member_count
           , g_nsfw_level
           , g_language
           , dt_now
           , str(guild_id),)
    )

    db.commit()
    cursor.close()


def update_member_info(guild_id, member_id, name, avatar, created_at, nickname, display_name, joined_at):
    cursor = db.cursor()
    query = """UPDATE 
                    members
                SET
                    discord_guild_id = (%s)
                    , name = (%s)
                    , avatar = (%s)
                    , created_at = (%s)
                    , nickname = (%s)
                    , display_name = (%s)
                    , joined_at = (%s)
                WHERE member_id = (%s)
                """
    cursor.execute(query, (str(guild_id), name, avatar, created_at, nickname, display_name, joined_at, str(member_id)))
    db.commit()
    cursor.close()


def update_role_in_db(ID_guild, role_id, role_name, position, color, hoisted, mentionable, managed, permissions,
                      created_at, last_synced):
    cursor = db.cursor()
    query = """UPDATE 
                    roles
                SET
                    discord_guild_id = (%s)
                    , role_name = (%s)
                    , position = (%s)
                    , color = (%s)
                    , hoisted = (%s)
                    , mentionable = (%s)
                    , managed = (%s)
                    , permissions = (%s)
                    , created_at = (%s)
                    , last_synced = (%s)

                WHERE role_id = (%s)
                """
    cursor.execute(query, (
        str(ID_guild), role_name, position, color, hoisted, mentionable, managed, permissions, created_at, last_synced,
        str(role_id)))
    db.commit()
    cursor.close()


def update_channel_in_db(guild_id, channel_id, name, category, position, mention, jump_url, permissions_synced,
                         overwrites, created_at, last_synced):
    cursor = db.cursor()
    query = """UPDATE 
                    channels
                SET
                    discord_guild_id = (%s)
                    , channel_name = (%s)
                    , category = (%s)
                    , position = (%s)
                    , mention = (%s)
                    , jump_url = (%s)
                    , permissions_synced = (%s)
                    , overwrites = (%s)
                    , created_at = (%s)
                    , last_synced = (%s)
                WHERE channel_id = (%s)
                """
    cursor.execute(query, (
        str(guild_id), name, category, position, mention, jump_url, permissions_synced, overwrites, created_at,
        last_synced,
        str(channel_id)))
    db.commit()
    cursor.close()


"""
Sync function ties everything together. INSERT if not exists, UPDATE if exists.
"""


def sync(discord_client):
    def sync_guild_info():
        # TODO: Add handing for INSERT when not exists, and UPDATE for when exists.

        for guild in discord_client.guilds:
            print("- Syncing Guild...")
            update_guild_info(
                guild.name
                , str(guild.icon)
                , guild.created_at
                , guild.member_count
                , guild.nsfw_level[0]
                , guild.preferred_locale[1]
                , datetime.now()
                , guild.id
            )

    def sync_channel_info():
        for guild in discord_client.guilds:
            print("- Syncing Channels")
            for channel in guild.channels:
                if is_channel_in_db(channel.id) is None:
                    add_channel_to_db(
                        channel.guild.id
                        , channel.id
                        , channel.name
                        , 'Category' if channel.category is None else str(channel.category)
                        , channel.position
                        , channel.mention
                        , channel.jump_url
                        , channel.permissions_synced
                        , str(channel.overwrites)
                        , channel.created_at
                        , datetime.now()
                    )
                else:
                    update_channel_in_db(
                        channel.guild.id
                        , channel.id
                        , channel.name
                        , 'Category' if channel.category is None else str(channel.category)
                        , channel.position
                        , channel.mention
                        , channel.jump_url
                        , channel.permissions_synced
                        , str(channel.overwrites)
                        , channel.created_at
                        , datetime.now()
                    )

    def sync_role_info():
        for guild in discord_client.guilds:
            print("- Syncing roles")
            for role in guild.roles:
                if is_role_in_db(role.id) is None:
                    add_role_to_db(
                        str(role.guild.id)
                        , str(role.id)
                        , role.name
                        , role.position
                        , str(role.color)
                        , role.hoist
                        , role.mentionable
                        , role.managed
                        , str(role.permissions)
                        , role.created_at
                        , datetime.now()
                    )
                else:
                    update_role_in_db(
                        str(role.guild.id)
                        , str(role.id)
                        , role.name
                        , role.position
                        , str(role.color)
                        , role.hoist
                        , role.mentionable
                        , role.managed
                        , str(role.permissions)
                        , role.created_at
                        , datetime.now()
                    )

    def sync_member_info():
        for guild in discord_client.guilds:
            print(f"- Syncing members...")
            for member in guild.members:
                if is_member_in_db(member.id) is None:
                    add_member_to_db(
                        member.guild.id
                        , member.id
                        , member.name
                        , str(member.avatar)
                        , member.created_at
                        , member.nick
                        , member.display_name
                        , member.joined_at
                    )
                else:
                    update_member_info(
                        member.guild.id
                        , member.id
                        , member.name
                        , str(member.avatar)
                        , member.created_at
                        , member.nick
                        , member.display_name
                        , member.joined_at
                    )

    sync_guild_info()
    sync_channel_info()
    sync_role_info()
    sync_member_info()
