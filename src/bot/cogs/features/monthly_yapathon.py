"""
A simple monthly Yapathon, gives the yapper role to the member with the most points every month.
"""

import os
from discord.utils import get
from discord.ext import commands, tasks
import datetime

import logging

logger = logging.getLogger(__name__)


# NOTE: Currently this time is not customizable through /update_settings
DATE_AND_TIME = datetime.time(hour=17, minute=0, second=0, tzinfo=datetime.timezone.utc)


class MonthlyYapathon(commands.Cog):
    """
    This cog deals with all the stuff of monthly yapathon.
    """
    def __init__(self, bot):
        self.bot = bot
        self.yapper_role_id = self.bot.api.get_one_role("8")[0]["roles"][2]
        self.announcement_channel_id = self.bot.api.get_one_setting("5")[0]["setting"][2]
        self.appoint_monthly_yapper.start()

    def cog_unload(self):
        self.appoint_monthly_yapper.cancel()

    @tasks.loop(time=DATE_AND_TIME)
    async def appoint_monthly_yapper(self):
        """
        Function that is called to appoint monthly yapper.
        """
        logger.info("hmmm.")
        if datetime.datetime.now().date == 27:
            logger.info(f"Bot running appoint_monthly_yapper.")
            monthly_top_point_earner = self.bot.monthly_top_point_earner()

            if monthly_top_point_earner["status"] == "ok":
                try:
                    guild = bot.get_guild(os.get_env("MASTER_GUILD"))

                    new_yapper = get(guild.members, id=int(monthly_top_point_earner["message"][1]))
                    yapper_role = get(guild.roles, id=int(self.yapper_role_id))
                    announcement_channel = get(guild.channels, id=int(self.announcement_channel_id))

                    await new_yapper.add_roles(yapper_role)
                    await announcement_channel.send(f"The winner of last month's Monthly Yappaton is {new_yapper.mention}. Keep yapping and you might be the next one.")

                    self.bot.reset_monthly_points();
                    logger.info(f"Successfully appointed new yapper.")
                except Exception as err:
                    logger.error(f"Error appointing new monthly yapper: {err}")
            else:
                logger.error(f"Error appointing new monthly yapper: {monthly_top_point_earner["message"]}")

    @appoint_monthly_yapper.before_loop
    async def wait_until_bot_ready(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(MonthlyYapathon(bot))
