import Bot_Core.Core as Core
from Bot_Core.Core import datetime, discord, commands, colour_list, core_config

name = "Beezelbub"

DISCORD_TOKEN = Core.createBot(name)
@Core.bot.command(name="handover", help="Used after the AGM to change committee roles.")
async def handover(ctx):
    Core.logCommand(ctx)
    '''if not(core_config["admin_ID"] in [role.id for role in ctx.author.roles]):
        response = "Sorry, you must be an Admin to use this Command"
    else:'''
    date = datetime.now()
    century = date.strftime('%C')
    year = int(date.strftime('%y'))
    old_committee = "Committee {}{}-{}".format(century, (year - 1), year)
    new_committee = "Committee {}{}-{}".format(century, year, (year + 1))
    old_committee_role = discord.utils.get(ctx.guild.roles, name=old_committee)
    old_committee_permissions = discord.Permissions.none()
    new_committee_permissions = discord.Permissions(permissions=core_config["Committee_Permissions_Code"])
    await old_committee_role.edit(permissions=old_committee_permissions, colour=colour_list["stings_gold"])
    await ctx.guild.create_role(permissions=new_committee_permissions, colour=colour_list["stings_yellow"], name=new_committee)
    response = "Test"
    await ctx.send(response)

Core.main()

Core.bot.run(DISCORD_TOKEN)