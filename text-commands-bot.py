import discord
from discord.ext import commands
import json

adminUsers = {}
adminUsers_server_specific = {}

commands_dict = {}
help_message = "Hi! With this bot you can create new commands that will show you some info when being called.\nFor example you can make it so that the bot will write a guide when ``!guide`` is called.\n\nThese controls are binded to the admin user(s):\nStart by entering ``!add-cmd``, proceeding by entering the desired command and then the information you want to get when the command is triggered.\nWith ``!remove-cmd`` you can remove a command from the dictionary; same procedure.\n\nYou can also look over all of the commands by sending ``!read-all``."
is_busy = False

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def read_commands(self, serverID, request_type, message_content, message_channel):
        global commands_dict
        if str(serverID) not in commands_dict:
            return 'There are currently no commands saved for your server'
        else:
            if request_type=='r_specific':
                command_from_dict = commands_dict[str(serverID)][message_content]['triggered_message']
                return command_from_dict
            elif request_type=='r_all_a':
                return commands_dict
            elif request_type=='r_all':
                commands_from_server = ''
                for command in commands_dict[str(serverID)]:
                    commands_from_server += (f'command: ``{command}``, triggered message: {commands_dict[str(serverID)][command]["triggered_message"]}\n\n')
                return commands_from_server
                
            # else: print('Error: Incorrect request_type for read_commands()')

    async def add_remove_commands(self, serverID, user_id, request_type, message_channel):
        global is_busy
        global commands_dict
        is_busy = True
        if request_type=='a':
            if str(serverID) not in commands_dict:
                commands_dict[str(serverID)] = {}

            def check(m):
                return m.author.id == user_id and m.channel == message_channel
            
            await message_channel.send('Enter the new command, it should start with ``!``')
            command_message = await bot.wait_for('message', timeout=30.0, check=check)
            command = command_message.content
            if not command.startswith('!'):
                await message_channel.send('The command should start with ``!``\nYou need to start over')
                is_busy = False
                return
            await message_channel.send('Enter the message you want to get after the command is triggered:')
            new_text_message = await bot.wait_for('message', timeout=60.0, check=check)
            new_text = new_text_message.content
            commands_dict[str(serverID)][command] = {'triggered_message': new_text}
            if command in commands_dict[str(serverID)] and new_text in commands_dict[str(serverID)][command]:
                await message_channel.send('Command was succesfully created!')
                is_busy = False
            else:
                await message_channel.send('There was an error saving the command')
            is_busy = False

        elif request_type=='r':
            if str(serverID) not in commands_dict:
                await message_channel.send('There are no comamnds saved on your server')
                is_busy = False
                return
            def check(m):
                return m.author.id == user_id and m.channel == message_channel
            await message_channel.send('Enter the command you want to remove')
            command_message = await bot.wait_for('message', timeout=30.0, check=check)
            command = command_message.content
            if command in commands_dict[str(serverID)]:
                del commands_dict[str(serverID)][command]
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
                    await message.channel.send(str(result))
                elif command == "!help" and message.author.id in adminUsers:
                    await message.channel.send(str(result))
                elif command == "!read-all" and (message.author.id in adminUsers_server_specific or message.author.id in adminUsers):
                    await message.channel.send(result)
            else:
                if command in commands_dict[str(message.guild.id)]:
                    result = await self.read_commands('r_specific', command)
                    await message.channel.send(str(result))
                else:
                    await message.channel.send('There was no command found with this name')

intents = discord.Intents.default()
intents.message_content = True
bot = Client(command_prefix=";", activity=discord.Game(name="lurking"), intents=intents)

bot.run('YOUR TOKEN')