import Bot_Core.Core as Core
from Bot_Core.Core import colour_list, core_config
from Bot_Core.imports import *

#Declares the name of the bot for later use
name = "Beelzebub"

DISCORD_TOKEN = Core.createBot(name) #Creates the bot and outputs the token for later use

#Code for the handover command which changes the permissions on the old committee role and then creates the new one before adding members to it
@Core.bot.command(name="handover", help="Used after the AGM to change committee roles.")
async def handover(ctx):
    Core.logCommand(ctx) #Logs the command
    if not(core_config["admin_ID"] in [role.id for role in ctx.author.roles]): #Checks if the person running the command is an Admin
        await ctx.send("Sorry, you must be an Admin to use this Command")
    else:
        #Creates the new committee role and updates the old one
        date = datetime.now() #Gets the current Date
        century = date.strftime('%C') #Obtains the century from the date
        year = int(date.strftime('%y')) #Obtains the year from the date
        old_committee = "Committee {}{}-{}".format(century, (year - 1), year) #Combines the year and century to get last year's committee name
        new_committee = "Committee {}{}-{}".format(century, year, (year + 1)) #Combines the year and century to get this year's committee name
        #The above code obtains the names for the two committee roles

        old_committee_role = discord.utils.get(ctx.guild.roles, name=old_committee) #Gets the old committe role from the name
        old_committee_permissions = discord.Permissions.none() #Sets the permissions to be no extra
        old_committee_position = old_committee_role.position #Gets the position of the role in the heirarchy
        await old_committee_role.edit(permissions=old_committee_permissions, colour=colour_list["stings_gold"]) #Pushes the changes
        #The above code updates the old committee role

        new_committee_permissions = discord.Permissions(permissions=core_config["Committee_Permissions_Code"]) #Sets the new committee permissions, value obtained from https://discordlookup.com/permissions-calculator/17618388000774
        await ctx.guild.create_role(permissions=new_committee_permissions, colour=colour_list["stings_yellow"], name=new_committee, hoist=True) #Creates the role
        new_committee_role =  discord.utils.get(ctx.guild.roles, name=new_committee) #Gets the new committe role from the name
        new_committee_position = old_committee_position + 1 #Sets the position to be one higher than the old role
        await new_committee_role.edit(position=new_committee_position) #Pushes the position change
        #The above code creates the new committee role and gives it a higher position than the old committee role

        channel_name = "committee-chat-{}{}-{}".format(century, year, (year + 1)) #Creates the channel name from the year and century
        StinGS_member_role = ctx.guild.get_role(core_config["StinGS_Default_Role"]) #Gets the standard member role from the ID in the config
        overwrites = {
            new_committee_role : discord.PermissionOverwrite(read_messages = True), #Allows the new committee to see the channel
            StinGS_member_role : discord.PermissionOverwrite(read_messages = False) #Denys everyone else permission to see the channel
        } #Note that the committee do not need permission to write in the channel because that is not a permission denied to the base role
        await ctx.guild.create_text_channel(channel_name, catagory=core_config["Committee_Catagory_ID"], overwrites=overwrites) #Creates the role and puts it in the Committee catagory
        #The above code creates the new committee channel and sets the channel permissions so that only committee can see it

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author #Checks if the new message was sent by the same person and in the same channel as the command was triggered in

        await ctx.send("Please enter the new committee members user IDs seperated by a comma") #Sends the message asking for the new committee members to be identified
        try: #Attempts to get a response
            response = await Core.bot.wait_for("message",check=check, timeout=60) #Waits 60s for a message event that matches the check funtion
        except asyncio.TimeoutError: #If 60s passes the error occurs and the following message is sent
            await ctx.send("Sorry you took too long to respond. Please use the command again.")

        new_committee_member_list = response.split(",") #Splits the response at the commas to obtain individual role IDs
        for committee_member in new_committee_member_list: #Iterates through the member list
            member_ID = int(committee_member.strip(" @")) #Removes any spaces or @
            member = ctx.guild.get_member(member_ID) #Gets the member from the User ID
            await member.add_roles(new_committee_role) #Adds the committee role to the member
        #The above code adds the members specified in the message to the new committee role

        await ctx.send("Committee handover completed.\nPlease remember to manually update the admins.") #Sends the message informing the user that the command is done

Core.main() #Loads the functions inside the main loop of the core file, generally core bot commands

Core.bot.run(DISCORD_TOKEN) #Runs the bot using the discord token outputed from the bot creation function