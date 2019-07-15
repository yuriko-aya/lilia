#!/usr/bin/env python3

import discord
import random
import os
import asyncio
import configparser
import feedparser
import dne
import mxl
import logging
import re
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

now = datetime.today()
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler('discord.log',
                                    when="h",
                                    interval=6,
                                    backupCount=20)
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class LiliaBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bg_task = self.loop.create_task(self.rss_update())

    async def on_ready(self):
        print('Looged in as')
        print(self.user.name)
        print(self.user.id)
        print('-----------------')
        activity = discord.Game('with AYA on her bed')
        await self.change_presence(status=discord.Status.online,
                                   activity=activity)

    def get_random_image(self):
        s_file = random.choice(
            os.listdir('/home/alice/.lilia/imgsrc')
        )
        return s_file

    def uppercase_abuse(self, message):
        words = message.split()
        upnum = len([word for word in words if word.isupper()])
        lonum = len([word for word in words if word.islower()])
        tinum = len([word for word in words if word.istitle()])
        if len(words) >= 3:
            return int(lonum)+int(tinum) < int(upnum)  # +int(mixnum)

    def dencrypt(self, method, message):
        commands = message.content.split()
        used_method = eval(method)
        if commands[2] == 'encode':
            msg = 'This is the result, {0.author.mention}-sama: ' \
                    .format(message) \
                    + used_method.dencode(' '.join(commands[3:]), 'encode')
        elif commands[2] == 'decode':
            msg = 'This is the result, {0.author.mention}-sama: ' \
                    .format(message) \
                    + used_method.dencode(' '.join(commands[3:]), 'decode')
        else:
            msg = 'Somethign wrong with your request, ' \
                    '{0.author.mention}-sama'.format(message)
        return msg

    async def rss_update(self):
        await self.wait_until_ready()
        channel = self.get_channel(600315520302055434)
        # channel = discord.Object(id='521269328046325776')
        while not self.is_closed():
            feed = feedparser.parse('https://aya.sanusi.id/feed/')
            config = configparser.ConfigParser()
            config.read('feed.ini')
            if feed.entries[0].published != config['DEFAULT']['latest_post']:
                if len(feed.entries[0].tags) > 1:
                    if feed.entries[0].tags[0].term == 'Novel' \
                                                    or feed.entries[0].tags[1]\
                                                    .term == 'Novel':
                        post_type = 'Novel'
                    else:
                        post_type = feed.entries[0].tags[0].term
                else:
                    post_type = feed.entries[0].tags[0].term
                msg = ('Master AYA just published new ' +
                       post_type + ' on her web, the title is ' +
                       feed.entries[0].title +
                       ' and you can view it in here : ' +
                       feed.entries[0].link)
                config['DEFAULT']['latest_post'] = feed.entries[0].published
                with open('feed.ini', 'w') as configfile:
                    config.write(configfile)
                await channel.send(msg)
            await asyncio.sleep(60)

    async def on_member_join(self, member):
        guild = member.guild
	role =  discord.utils.get(guild.roles, name='Commoner')
        if guild.system_channel is not None:
            msg = 'Welcome to {0.name}, {1.mention}-sama,' \
                  ' We hope you enjoy your stay here'.format(guild, member)
            await guild.system_channel.send(msg)
            await member.add_roles(role)

    async def on_member_remove(self, member):
        guild = member.guild
        if guild .system_channel is not None:
            msg = 'One of our dear comrade, {0.name} has left us,' \
                  ' let us wish the best for them'.format(member)
            await guild.system_channel.send(msg)

    async def on_message(self, message):
        log_message = '[' + str(message.guild) + '] ' + \
                      str(message.channel) + \
                      ' -> ' + str(message.author) + ': ' + \
                      str(message.content)

        logger.info(log_message)

        print(str(message.created_at) + ': ' + log_message)

        if message.author.id == self.user.id:
            return

        if self.uppercase_abuse(str(message.content)):
            msg = 'Uppercase abuse, {0.author.mention},' \
                  ' you have been warned!'.format(message)
            await message.channel.send(msg)

        if message.content.startswith(('->help', '!help', '.help', '--help')):
            msg = 'I am really sorry master {0.author.mention},' \
                   ' the only one who can hel you is yourself, not me' \
                   ' or anyone else'.format(message)
            await message.channel.send(msg)

        if '<@463524758156345346>' in message.content:
            msg = 'Did you call me, {0.author.mention}-sama?' \
                ' I am sorry but that is not how to use me' \
                ' Please kindly use `!lilia commands` to learn' \
                ' how to use me.'.format(message)
            await message.channel.send(msg)

        if message.content.startswith('!lilia'):
            commands = message.content.split()

            if commands[1] in {'help', '->help', '!help', '.help', '--help'}:
                msg = 'I am really sorry master {0.author.mention},' \
                    ' the only one who can hel you is yourself, not me' \
                    ' or anyone else'.format(message)
                await message.channel.send(msg)

            elif commands[1] == 'gift':
                msg = 'This is gift from {0.author.mention}-sama for you, ' \
                      .format(message) + commands[3] + '-sama'
                dest = re.sub(r"\D+", "", commands[3])
                member_name = self.get_user(int(dest))
                await member_name.send(msg, file=discord.File(
                    '/home/alice/.lilia/imgsrc/' + self.get_random_image()
                ))

            elif commands[1] == 'mxl' and len(commands) >= 4:
                msg = self.dencrypt('mxl', message)
                await message.channel.send(msg)

            elif commands[1] == 'dne' and len(commands) >= 4:
                msg = self.dencrypt('dne', message)
                await message.channel.send(msg)

            elif commands[1] == 'yuribomb':
                nchannel = discord.utils.get(message.guild.channels,
                                             name='nsfw')
                if len(commands) >= 3 and commands[2].isdigit():
                    number = int(commands[2])
                else:
                    number = 4
                if number <= 8:
                    for i in range(number):
                        await nchannel.send(
                            str(i+1) + ':',
                            file=discord.File(
                                '/home/alice/.lilia/imgsrc/' +
                                self.get_random_image()
                            ))
                else:
                    await message.channel.send(
                        'You requesting too much, {0.author.mention}'
                        .format(message)
                    )

            elif commands[1].lower() in {
                'hi', 'hello', 'morning'
            } and len(commands) <= 3:
                msg = ' '.join(commands[1:]) +\
                    ' too, {0.author.mention}-sama'.format(message)
                await message.channel.send(msg)

            elif commands[1] == 'suicide':
                print(message.author.name)
                if message.author.id != 346541452807110666:
                    msg = 'I am sorry {0.author.mention}-sama, you do not' \
                          ' have any right to order me to do that'.format(
                              message
                          )
                    await message.channel.send(msg)
                else:
                    msg = 'Yes, Master {0.author.mention}' \
                          ' I will kill myslef now'.format(message)
                    await message.channel.send(msg)
                    # os.kill(os.getpid(), 9)
                    await self.close()

            elif commands[1] == 'commands':
                msg = """
Hello, my name Lilia Anabel.
I only available at AYA Translation.
you can use me with `!lilia` as prefix.
I'm just created recently by my master so I don't have a lot function

**gift**:
command: `!lilia gift to @user`
gift nswf image and mention @user

**yuribomb**:
command: `!lilia yuribomb number`
post multiple nsfw images, number is optional, max 8

***Encryption***
Double Number Encryption:
encode command: `!lilia dne encode message`
decode command: `!lilia dne decode message`

Move X Letter:
encode command: `!lilia mxl encode message`
decode command: `!lilia mxl decode message`

            """
                await message.channel.send(msg)

            else:
                query = ' '.join(commands[1:])
                msg = '{0.author.mention}-sama, what do you mean with {1}?' \
                      'I do not understand'.format(message, query)
                await message.channel.send(msg)

if __name__ == "__main__":
    token_config = configparser.ConfigParser()

    token_config.read('config.ini')
    '''
    config.ini contents:
    [TOKEN]
    token = your_token_code
    '''

    TOKEN = token_config['TOKEN']['token']

    client = LiliaBot()
    client.run(TOKEN)
