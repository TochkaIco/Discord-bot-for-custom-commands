import discord
from discord.ext import commands
import database

adminUsers = {}
adminUsers_server_specific = {}
help_message = "Hi! With this bot you can create new commands that will show you some info when being called.\nFor example you can make it so that the bot will write a guide when ``!guide`` is called.\n\nThese controls are binded to the admin user(s):\nStart by entering ``!add-cmd``, proceeding by entering the desired command and then the information you want to get when the command is triggered.\nWith ``!remove-cmd`` you can remove a command from the dictionary; same procedure.\n\nYou can also look over all of the commands by sending ``!read-all``."
is_busy = False  # Global flag to indicate if the bot is busy

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def read_commands(self, serverID, request_type, message_content, message_channel):
        ifexists = database.guildID_check(serverID)
        if not ifexists == 'exists':
            return 'There are currently no commands saved for your server'
        else:
            if request_type=='r_specific':
                command_from_db = database.command_lookup(serverID, message_content)
                return command_from_db[0]
            elif request_type=='r_all_a':
                return database.show_all()
            elif request_type=='r_all':
                command_from_db = database.show_all_server_specific(serverID)
                return command_from_db
                
            else: print('Error: Incorrect request_type for read_commands()')

    async def add_remove_commands(self, serverID, user_id, request_type, message_channel): #request_type specifies whether the command is created or removed
        global is_busy
        global commands_dict
        is_busy = True
        if request_type=='a':
            def check(m):
                return m.author.id == user_id and m.channel == message_channel
            
            await message_channel.send('Enter the new command, it should start with ``!``')
            command_message = await bot.wait_for('message', timeout=30.0, check=check) #FIX THIS
            command = command_message.content
            if not command.startswith('!'):
                await message_channel.send('The command should start with ``!``\nYou need to start over')
                is_busy = False
                return
            await message_channel.send('Enter the message you want to get after the command is triggered:')
            new_text_message = await bot.wait_for('message', timeout=60.0, check=check)
            new_text = new_text_message.content
            database.add_record((serverID, command, new_text))
            await message_channel.send('The command has been created.')
            is_busy = False

        elif request_type=='r':
            if not database.guildID_check(serverID) == 'exists':
                await message_channel.send('There are no comamnds saved on your server')
                is_busy = False
                return
            def check(m):
                return m.author.id == user_id and m.channel == message_channel
            await message_channel.send('Enter the command you want to remove')
            command_message = await bot.wait_for('message', timeout=30.0, check=check)
            command = command_message.content
            if database.command_check(serverID, command) == 'exists':
                database.delete_record(serverID, command)
                await message_channel.send('The command was succesfully removed')
                is_busy = False
            else:
                await message_channel.send('There was no command found with this name')
                is_busy = False
                return


    async def on_message(self, message):
        if message.author==self.user: return
        elif is_busy: return
        elif message.content.startswith('!'):
            command = message.content
            # Create a mapping of commands to their actions
            command_actions = {
                "!help": lambda: message.channel.send(help_message),
                "!read-all": lambda: self.read_commands(message.guild.id, 'r_all', None, message.channel),
                "!read-all-admin": lambda: self.read_commands(message.guild.id, 'r_all_a', None, message.channel),
                "!add-cmd": lambda: self.add_remove_commands(message.guild.id, message.author.id, 'a', message.channel),
                "!remove-cmd": lambda: self.add_remove_commands(message.guild.id, message.author.id, 'r', message.channel)
            }

            # Check if the command is in the predefined actions
            if command in command_actions:
                result = await command_actions[command]()
                if command == "!read-all-admin" and message.author.id in adminUsers:
                    result_f = ''
                    for item in result:
                        result_f += f"rawid: ``{item[0]}``, command: ``{item[2]}``, text: {item[3]}\n-----------------------\n"
                        if len(result_f) > 2000:
                            await message.channel.send(result_f[:2000])
                            await message.channel.send(result_f[2000:])
                            result_f = ''
                    await message.channel.send(result_f)
                elif command == "!read-all" and (message.author.id in adminUsers_server_specific or message.author.id in adminUsers):
                    result_f = ''
                    for item in result:
                        result_f += f"command: ``{item[0]}``, text: ``{item[1]}``\n-----------------------\n"
                        if len(result_f) > 2000:
                            await message.channel.send(result_f[:2000])
                            await message.channel.send(result_f[2000:])
                            result_f = ''
                    await message.channel.send(result_f)
            else:
                if database.guildID_check(message.guild.id) == 'exists':
                    if database.command_check(message.guild.id, command) == 'exists':
                        result = await self.read_commands(message.guild.id, 'r_specific', command, message.channel)
                        if len(result) > 2000:
                            await message.channel.send(result[:2000])
                            await message.channel.send(result[2000:])
                        else:
                            await message.channel.send(result)
                    else:
                        await message.channel.send('There was no command found with this name')
                else:
                    await message.channel.send('There are no commands on your server')
                        

intents = discord.Intents.default()
intents.message_content = True
bot = Client(command_prefix=";", activity=discord.Game(name="testing"), intents=intents)

bot.run('YOUR TOKEN')