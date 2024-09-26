from datetime import datetime
import discord


#### Documentation
# For Embed Colors: https://discordpy.readthedocs.io/en/stable/api.html?highlight=embed#discord.Colour

def embed_info(title, message, color):
    """
    Embedding for avatar change alerts.
    """
    embed = discord.Embed(
        title=f'{title}'
        , description=f'{message}'
        , color=color
        , timestamp=datetime.utcnow()
    )
    return embed

def embed_hc(api, db):
    """
    Embedding for avatar change alerts.
    """
    color = api.get("color") if api.get("color") == db.get("color") else discord.Color.yellow()

    embed = discord.Embed(
        title=f'Health checks'
        , color=color
        , timestamp=datetime.utcnow()
    )
    embed.add_field(
        name=api.get("message")
        , value=api.get("status_code")
        , inline=False
    )
    embed.add_field(
        name=db.get("message")
        , value=db.get("status_code")
        , inline=False
    )
    return embed
