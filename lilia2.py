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
import mysql.connector
import time
import requests
import aiohttp
import json
from bs4 import BeautifulSoup
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

now = datetime.today()
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler('/var/log/lilia/lilia.log',
                                   when="midnight",
                                   backupCount=5)
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

os.chdir('/home/alice/lilia/')


class LiliaBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bg_task = self.loop.create_task(self.background_task())

    async def on_ready(self):
        print('Looged in as')
        print(self.user.name)
        print(self.user.id)
        print('-----------------')
        activity = discord.Game('with AYA on her bed')
        await self.change_presence(status=discord.Status.online,
                                   activity=activity)

    async def background_task(self):
        await self.wait_until_ready()
        admin = self.get_user(346541452807110666)
        channel = self.get_channel(600315520302055434)
        config = configparser.ConfigParser()
        config.read(['feed.ini', 'config.ini'])
        port_list = json.loads(config.get('SERVER', 'port_list'))
        while not self.is_closed():
            feed = feedparser.parse('https://aya.sanusi.id/feed/')
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
                msg = ('@everyone Master AYA just published new '
                       + post_type + ' on her web, the title is '
                       + feed.entries[0].title
                       + ' and you can view it in here : '
                       + feed.entries[0].link)
                config['DEFAULT']['latest_post'] = feed.entries[0].published
                with open('feed.ini', 'w') as configfile:
                    config.write(configfile)
                await channel.send(msg)
            logger.info('Feed proceed finished')
            await asyncio.sleep(600)

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
            return int(lonum) + int(tinum) < int(upnum)  # +int(mixnum)

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

    def get_the_text(self, string):
        soup = BeautifulSoup(string)
        return soup.get_text()

    async def on_member_join(self, member):
        guild = member.guild
        role = discord.utils.get(guild.roles, name='Commoner')
        if guild.system_channel is not None:
            msg = 'Welcome to {0.name}, {1.mention} onee-sama,' \
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
            msg = 'I am really sorry {0.author.mention} onee-sama,' \
                  ' the only one who can hel you is yourself, not me' \
                  ' or anyone else'.format(message)
            await message.channel.send(msg)

        if '<@463524758156345346>' in message.content:
            msg = 'Did you call me, {0.author.mention} onee-sama?' \
                ' I am sorry but that is not how to use me' \
                ' Please kindly use `!lilia commands` to learn' \
                ' how to use me.'.format(message)
            await message.channel.send(msg)

        if message.content.startswith('-game'):
            result = message.content.split()
            if len(result) < 10:
                msg = "Something missing, usage is:"\
                    '-game game/tournament_name player1 point player2 point player3 point player4 point'
                await message.channel.send(msg)
            elif len(result) > 10:
                msg = "Something too much, usage is:"\
                    '-game game/tournament_name player1 point player2 point player3 point player4 point'
                await message.channel.send(msg)
            else:
                config = configparser.ConfigParser()
                config.read(['config.ini'])

                raw = {
                    result[2]: int(result[3]),
                    result[4]: int(result[5]),
                    result[6]: int(result[7]),
                    result[8]: int(result[9]),
                }
                raw_sorted = {k: v for k, v in sorted(raw.items(), key=lambda item: item[1], reverse=True)}
                data = {
                    'key': config['MJSCORE']['key'],
                    'game': result[1],
                    'result': raw_sorted,
                }
                post_data = requests.post(config['MJSCORE']['url'], data=json.dumps(data))
                if post_data.status_code == 200:
                    datas = json.loads(post_data.content)
                    message = "Game recorded, for game %s, Position 1: %s with %d points, Position 2: %s with %d points, "\
                            "Position 3: %s with %d points, and Position 4: %s with %d points" % (datas['game'], datas['position1']['player'], datas['position1']['score'],
                                datas['position2']['player'], datas['position2']['score'],
                                datas['position3']['player'], datas['position3']['score'],
                                datas['position4']['player'], datas['position4']['score'],)
                    await message.channel.send(message)
                else:
                    await message.channel.send(post_data.content)

        if message.content.startswith('!lilia'):
            commands = message.content.split()

            if commands[1] in {'help', '->help', '!help', '.help', '--help'}:
                msg = 'I am really sorry {0.author.mention} onee-sama,' \
                    ' the only one who can hel you is yourself, not me' \
                    ' or anyone else'.format(message)
                await message.channel.send(msg)

            elif commands[1] == 'gift':
                msg = 'This is gift from {0.author.mention} onee-sama for ' \
                      'you, '.format(message) + commands[3] + ' onee-sama'
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
                            str(i + 1) + ':',
                            file=discord.File(
                                '/home/alice/.lilia/imgsrc/'
                                + self.get_random_image()
                            ))
                else:
                    await message.channel.send(
                        'You requesting too much, {0.author.mention} onee-sama'
                        .format(message)
                    )

            elif commands[1].lower() in {
                'hi', 'hello', 'morning'
            } and len(commands) <= 3:
                msg = ' '.join(commands[1:]) +\
                    ' too, {0.author.mention}-sama'.format(message)
                await message.channel.send(msg)

            elif commands[1] == 'monitor':
                await self.check_portcities_instance_5()

            elif commands[1] == 'suicide':
                if message.author.id != 346541452807110666:
                    msg = 'I am sorry {0.author.mention} onee-sama, you do '\
                          'not have any right to order me to do that'.format(
                              message
                          )
                    await message.channel.send(msg)
                else:
                    msg = 'I understand, {0.author.mention} onee-sama' \
                          ' I will kill myslef now'.format(message)
                    await message.channel.send(msg)
                    # os.kill(os.getpid(), 9)
                    await self.close()

            elif commands[1] == 'spoiler':
                if message.author.id != 346541452807110666:
                    msg = 'I am sorry {0.author.mention} onee-sama, you do '\
                          'not have any right to order me to do that'.format(
                              message
                          )
                    await message.channel.send(msg)
                    return
                db_config = configparser.ConfigParser()
                db_config.read('config.ini')
                mydb = mysql.connector.connect(
                    host=db_config['DATABASE']['host'],
                    user=db_config['DATABASE']['user'],
                    passwd=db_config['DATABASE']['password'],
                    database=db_config['DATABASE']['database']
                )
                mycursor = mydb.cursor()
                sql_query = "SELECT post_title, post_content FROM wp_posts " \
                            "WHERE post_status='future' AND post_type='post' "\
                            "ORDER BY id DESC LIMIT 1"
                mycursor.execute(sql_query)
                posts = mycursor.fetchall()
                if posts:
                    for post in posts:
                        await message.channel.send('------------------------')
                        await message.channel.send(
                            'Starting to post earlly release')
                        await message.channel.send('------------------------')
                        await message.channel.send('**' + post[0] + '**')
                        await message.channel.send('------------------------')
                        lines = post[1].splitlines()
                        for line in lines:
                            msg = self.get_the_text(line)
                            msg += '_ _'
                            await message.channel.send(msg)
                            time.sleep(0.5)
                        await message.channel.send('------------------------')
                        await message.channel.send('End of **' + post[0] + '**')
                        await message.channel.send('------------------------')

            elif commands[1] == 'commands':
                msg = """
Hello, my name Lilia Anabel.
I only available at AYA Translation.
you can use me with `!lilia` as prefix.
I'm just created recently by AYA onee-sama so I don't have a lot function

**gift**:
command: `!lilia gift to @user`
gift NSFW image and mention @user

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
                msg = '{0.author.mention} onee-sama, what do you mean with '\
                      '{1}? I do not understand'.format(message, query)
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
