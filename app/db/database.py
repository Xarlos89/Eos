import psycopg
from datetime import datetime


class DB:
    def __init__(self, db_string, discord_client):
        self.connection = psycopg.connect(db_string)
        self.cursor = self.connection.cursor()
        self.discord_client = discord_client

    """ 
    1st Layer.
     From here we create:
    - Basic Database interaction
    """

    def create_cursor(self):
        return self.connection.cursor()

    def close_cursor(self):
        self.cursor.close()
        self.connection.close()

    def commit_query(self):
        self.connection.commit()

    def select_one(self, query, *data):
        if data:
            self.cursor.execute(query, data)
        else:
            self.cursor.execute(query)
        data = self.cursor.fetchone()
        self.connection.commit()
        self.connection.close_cursor()
        return data

    def select_all(self, query, *data):
        if data:
            self.cursor.execute(query, data)
        else:
            self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.connection.commit()
        self.connection.close_cursor()
        return data

    def update(self, query, data):
        self.cursor.execute(query, (data,))
        self.connection.commit()
        self.connection.close_cursor()

    def insert(self, query, data):
        self.cursor.execute(query, (data,))
        self.connection.commit()
        self.connection.close_cursor()

    """ 
    2nd Layer.
     From here we create:
    - Existence Checks
    """

    def is_data_in_db(self, table_name, column_name, value):
        cursor = self.connection.cursor()
        query = f"SELECT * FROM {table_name} WHERE {column_name} = (%s)"
        cursor.execute(query, (value,))
        data = cursor.fetchone()

        if data is None:
            return False
        return True

    def is_guild_in_db(self, guild_id):
        return self.is_data_in_db("guilds", "discord_guild_id", str(guild_id))

    def is_settings_in_db(self, guild_id):
        return self.is_data_in_db("settings", "discord_guild_id", str(guild_id))

    def is_channel_in_db(self, channel_id):
        return self.is_data_in_db("channels", "channel_id", str(channel_id))

    def is_member_in_db(self, member_id):
        return self.is_data_in_db("members", "member_id", str(member_id))

    def is_role_in_db(self, role_id):
        return self.is_data_in_db("roles", "role_id", str(role_id))

    def is_command_in_db(self, command_id):
        return self.is_data_in_db("commands", "command_id", str(command_id))

    """
    3rd Layer. 
    From here we create:
    - Discord level CRUD commands. Add/remove/update/delete.
    - Discord level validation checks 

    TODO: Add function to add guild when guild does not exist.
    """

    # ---------- Add commands
    def add_guild_to_db(self, cur, g_name, g_logo, g_created_at, g_member_count, g_nsfw_level, g_language, dt_now,
                        discord_guild_id):
        query = """INSERT 
                        INTO guilds
                            (discord_guild_id, name, logo, created_at, member_count, nsfw_level, language, last_sync)
                        VALUES((%s), (%s), (%s), (%s),(%s), (%s), (%s))"""
        cur.execute(
            query
            , (g_name
               , g_logo
               , g_created_at
               , g_member_count
               , g_nsfw_level
               , g_language
               , dt_now
               , str(discord_guild_id),)
        )

    def add_settings_to_db(self, cur, discord_guild_id, logging, moderation, dt_now):
        query = """INSERT 
                        INTO settings
                            (discord_guild_id, logging, moderation, last_sync)
                        VALUES((%s), (%s), (%s), (%s))"""
        cur.execute(
            query
            , (str(discord_guild_id)
               , logging
               , moderation
               , dt_now
               )
        )

    def add_channel_to_db(self, cur, guild_id, channel_id, name, category, position, mention, jump_url,
                          permissions_synced, overwrites, created_at, last_synced):
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
        cur.execute(
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

    def add_member_to_db(self, cur, guild_id, member_id, name, avatar, created_at, nickname, display_name, joined_at):
        query = """INSERT 
                        INTO members
                            (discord_guild_id, member_id, name, avatar, created_at, nickname, display_name, joined_at, points)
                        VALUES((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))
                            """
        cur.execute(query,
                    (str(guild_id), str(member_id), name, avatar, created_at, nickname, display_name, joined_at,
                     10))

    def add_role_to_db(self, cur, id_guild, role_id, role_name, position, color, hoisted, mentionable, managed,
                       permissions, created_at, last_synced):
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
        cur.execute(
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

    # ---------- Update commands
    def update_guild_info(self, cur, g_name, g_logo, g_created_at, g_member_count, g_nsfw_level, g_language, dt_now,
                          guild_id):

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
                            discord_guild_id = (%s)"""
        cur.execute(
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

    def update_member_info(self, cur, guild_id, member_id, name, avatar, created_at, nickname, display_name, joined_at):
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
        cur.execute(
            query
            , (str(guild_id)
               , name
               , avatar
               , created_at
               , nickname
               , display_name
               , joined_at
               , str(member_id))
        )

    def update_role_in_db(self, cur, id_guild, role_id, role_name, position, color, hoisted, mentionable, managed,
                          permissions, created_at, last_synced):
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
        cur.execute(query, (
            str(id_guild), role_name, position, color, hoisted, mentionable, managed, permissions, created_at,
            last_synced,
            str(role_id)))

    def update_channel_in_db(self, cur, guild_id, channel_id, name, category, position, mention, jump_url,
                             permissions_synced, overwrites, created_at, last_synced):

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
        cur.execute(query, (
            str(guild_id), name, category, position, mention, jump_url, permissions_synced, overwrites, created_at,
            last_synced,
            str(channel_id)))

    # ---------- Delete commands
    def delete_guild(self, guild_id):
        cursor = self.connection.cursor()
        query = """
                DELETE
                    guilds
                WHERE
                    discord_guild_id = (%s)
                """
        cursor.execute(query, (str(guild_id),))

        self.cursor.connection.commit()
        self.cursor.connection.close()

    def delete_member(self, member_id, guild_id):
        cursor = self.connection.cursor()
        query = """
                DELETE FROM
                    members
                WHERE
                    member_id = (%s) 
                    and discord_guild_id = (%s)
                """
        cursor.execute(query, (member_id, str(guild_id),))

        self.cursor.connection.commit()
        self.cursor.connection.close()

    def delete_role(self, role_id, guild_id):
        cursor = self.connection.cursor()
        query = """
                DELETE FROM
                    roles
                WHERE
                    role_id = (%s) 
                    and discord_guild_id = (%s)
                """
        cursor.execute(query, (role_id, str(guild_id),))

        self.cursor.connection.commit()
        self.cursor.connection.close()

    def delete_channel(self, channel_id, guild_id):
        cursor = self.connection.cursor()
        query = """
                DELETE FROM
                    channels
                WHERE
                    channel_id = (%s) 
                    and discord_guild_id = (%s)
                """
        cursor.execute(query, (channel_id, str(guild_id),))

        self.cursor.connection.commit()
        self.cursor.connection.close()

    """
    4th Layer. 
    From here we create:
    - Database Syncs
    - Database Jobs
    - Any background database tasks
    
    """

    def sync(self, guilds=True, channels=True, members=True, roles=True, settings=True):
        cur = self.connection.cursor()

        def sync_guild_info(cur):
            for guild in self.discord_client.guilds:
                print("- Syncing Guild...")
                if self.is_guild_in_db(guild.id) is None:
                    self.add_guild_to_db(
                        cur
                        , guild.name
                        , str(guild.icon)
                        , guild.created_at
                        , guild.member_count
                        , guild.nsfw_level[0]
                        , guild.preferred_locale[1]
                        , datetime.now()
                        , guild.id
                    )
                else:
                    self.update_guild_info(
                        cur
                        , guild.name
                        , str(guild.icon)
                        , guild.created_at
                        , guild.member_count
                        , guild.nsfw_level[0]
                        , guild.preferred_locale[1]
                        , datetime.now()
                        , guild.id
                    )

        def sync_channel_info(cur):
            for guild in self.discord_client.guilds:
                print("- Syncing Channels")
                for channel in guild.channels:
                    if self.is_channel_in_db(channel.id) is None:
                        self.add_channel_to_db(
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
                        self.update_channel_in_db(
                            cur
                            , channel.guild.id
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

        def sync_role_info(cur):
            for guild in self.discord_client.guilds:
                print("- Syncing roles")
                for role in guild.roles:
                    if self.is_role_in_db(role.id) is None:
                        self.add_role_to_db(
                            cur
                            , str(role.guild.id)
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
                        self.update_role_in_db(
                            cur
                            , str(role.guild.id)
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

        def sync_member_info(cur):
            for guild in self.discord_client.guilds:
                print(f"- Syncing members...")
                for member in guild.members:
                    if self.is_member_in_db(member.id) is None:
                        self.add_member_to_db(
                            cur
                            , member.guild.id
                            , member.id
                            , member.name
                            , str(member.avatar)
                            , member.created_at
                            , member.nick
                            , member.display_name
                            , member.joined_at
                        )
                    else:
                        self.update_member_info(
                            cur
                            , member.guild.id
                            , member.id
                            , member.name
                            , str(member.avatar)
                            , member.created_at
                            , member.nick
                            , member.display_name
                            , member.joined_at
                        )

        def sync_settings_info(cur):
            for guild in self.discord_client.guilds:
                print("- Adding settings...")
                if not self.is_settings_in_db(guild.id):
                    self.add_settings_to_db(
                        cur
                        , guild.id
                        , True
                        , True
                        , datetime.now()
                    )

        if guilds:
            sync_guild_info(cur)
            self.connection.commit()

        if channels:
            sync_channel_info(cur)
            self.connection.commit()

        if roles:
            sync_role_info(cur)
            self.connection.commit()

        if members:
            # TODO: strange bug in this ONLY when run with all the others too.
            # File "/Users/xarlos/Documents/GitHub/Eos/Eos/app/db/database.py", line 66, in is_data_in_db
            # cursor.execute(query, (value,))
            sync_member_info(cur)
            self.connection.commit()

        if settings:
            sync_settings_info(cur)
            self.connection.commit()

        self.connection.close()
