import Bot_Core.Core as Core
from Bot_Core.Core import colour_list, core_config
from Bot_Core.imports import *

#Declares the name of the bot for later use
name = "Beelzebub"

DISCORD_TOKEN = Core.createBot(name) #Creates the bot and outputs the token for later use

#Code for the handover command which changes the permissions on the old committee role and then creates the new one before adding members to it
@Core.bot.command(name="handover", help="Used after the AGM to change committee roles.")
async def handover(ctx):
    Core.logCommand(ctx)
    if not(core_config["admin_ID"] in [role.id for role in ctx.author.roles]): #Checks if the person running the command is an Admin
        await ctx.send("Sorry, you must be an Admin to use this Command")
    else:
        #Creates the new committee role and updates the old one
        date = datetime.now()
        century = date.strftime('%C')
        year = int(date.strftime('%y'))
        old_committee = "Committee {}{}-{}".format(century, (year - 1), year)
        new_committee = "Committee {}{}-{}".format(century, year, (year + 1))
        #The above code obtains the names for the two committee roles
        old_committee_role = discord.utils.get(ctx.guild.roles, name=old_committee)
        old_committee_permissions = discord.Permissions.none()
        old_committee_position = old_committee_role.position
        await old_committee_role.edit(permissions=old_committee_permissions, colour=colour_list["stings_gold"])
        #The above code updates the old committee roles
        new_committee_permissions = discord.Permissions(permissions=core_config["Committee_Permissions_Code"])
        await ctx.guild.create_role(permissions=new_committee_permissions, colour=colour_list["stings_yellow"], name=new_committee, hoist=True)
        new_committee_role =  discord.utils.get(ctx.guild.roles, name=new_committee)
        new_committee_position = old_committee_position + 1
        await new_committee_role.edit(position=new_committee_position)
        #The above code creates the new committee role and gives it a higher position than the old committee role

        channel_name = "committee-chat-{}{}-{}".format(century, year, (year + 1))
        StinGS_member_role = ctx.guild.get_role(core_config["StinGS_Default_Role"])
        overwrites = {
            new_committee_role : discord.PermissionOverwrite(read_messages = True), 
            StinGS_member_role : discord.PermissionOverwrite(read_messages = False)
        }
        await ctx.guild.create_text_channel(channel_name, catagory=core_config["Committee_Catagory_ID"], overwrites=overwrites)
        #The above code creates the new committee channel and sets the channel permissions so that only committee can see it

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        await ctx.send("Please tag the new committee members seperated by a comma")
        try:
            response = await Core.bot.wait_for("message",check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send("Sorry you took too long to respond. Please use the command again.")
        new_committee_member_list = response.split(",")
        for committee_member in new_committee_member_list:
            member_ID = int(committee_member.strip(" @"))
            member = ctx.guild.get_member(member_ID)
            await member.add_roles(new_committee_role)
        #The above code adds the members specified in the message to the new committee role

        await ctx.send("Committee handover completed.\nPlease remember to manually update the admins.")

Core.main()

Core.bot.run(DISCORD_TOKEN)