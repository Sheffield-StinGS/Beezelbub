import Bot_Core.Core as Core
from Bot_Core.Core import datetime, discord, commands, colour_list

name = "Beezelbub"

DISCORD_TOKEN = Core.createBot(name)
@Core.bot.command(name="handover", help="Used after the AGM to change committee roles.")
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

Core.main()

Core.bot.run(DISCORD_TOKEN)