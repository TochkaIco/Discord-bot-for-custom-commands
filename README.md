# Discord-bot-for-custom-commands
This bot allows lets you create custom commands for your server; after being triggered - a message will be sent with a guide, welcome message or something else you set up.

example: command - ``!welcome``, message - ``Hi and welcome to the server! You can grab roles for your preference in #roles. Please make sure to go through #rules, if you have any questions you can dm @admin.``

The commands are saved for the specific server they were added in. A user whose userID is placed in the ``adminUsers`` variable - can user ``!read-all-admin`` to read through all the commands that are saved for all the servers. Users whose userID is placed in the ``adminUsers_server_specific`` can use ``!read-all`` to view all the commands for their server.

Admin users can add/remove commands for their server with ``!add-cmd`` and ``!remove-cmd``. Anyone in a server can use the newly created commands for the server.

At the moment, whenever you enter the creation/removal process, the bot stops reacting to other users' messages until the process is finished. This means that while you're adding/removing commands, no one will be able trigger bot's commands.

All the commands that are customly created are saved in a data.db file (can be called differently, you'll just have to change ``db_file_name`` in ``database.py`` and in ``db-create.py``). Before starting the bot, you need to run ``db-create.py`` to create the Table for the commands.

The TOKEN for your bot should be placed on the last line where it says ``YOUR TOKEN``. You can get your token on the discord developer portal(https://discord.com/developers/applications). Make sure to enable Privileged Gateway Intents in the ``Bot`` section.
