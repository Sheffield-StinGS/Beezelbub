import Bot_Core
from Bot_Core import datetime, discord, commands

name = "Beezelbub"

DISCORD_TOKEN = Bot_Core.createBot(name)
@Bot_Core.bot.command(name="handover", help="Used after the AGM to change committee roles.")
async def handover(ctx):
    if not(837636971433558017 in [role.id for role in ctx.author.roles]):
        response = "Sorry, you must be an Admin to use this Command"
    else:
        date = datetime.now()
        century = date.strftime('%C')
        year = int(date.strftime('%y'))
        old_committee = "Committee {}{}-{}".format(century, (year - 1), year)
        new_committee = "Committee {}{}-{}".format(century, year, (year + 1))
        old_committee_role = discord.utils.get(ctx.guild.roles, name=old_committee)
        await old_committee_role.edit(permissions=0,)
        response = "Test"
    await ctx.send(response)

Bot_Core.main()

Bot_Core.bot.run(DISCORD_TOKEN)