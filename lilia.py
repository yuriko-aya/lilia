#!/usr/bin/env python3

import discord
import string
import random
import glob
import os
import asyncio
from pathlib import Path
import configparser
import feedparser
import image_dl
import dne
import mxl

TOKEN = ''

client = discord.Client()
config = configparser.ConfigParser()

#os.chdir('/home/alice/.lilia/')

def file_name_generator(size=8, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))

def get_file_name(image):
    return print(glob.glob('/home/alice/.lilia/' + image + '*')[0])

def uppercase_abuse(message):
    words = message.split()
    upnum = len([word for word in words if word.isupper()])
    lonum = len([word for word in words if word.islower()])
    tinum = len([word for word in words if word.istitle()])
#    mixnum = len([word for word in words if not word.islower() and not word.isupper() and not word.istitle()])
    if len(words) >= 3:
        return int(lonum)+int(tinum) < int(upnum)#+int(mixnum)

async def random_post_nsfw():
    await client.wait_until_ready()
    channel = discord.Object(id='464298646440116224') #nsfw LTF
#    channel = discord.Object(id='521650709121466388') #nsfw ATL
    while not client.is_closed:
        if random.random() < 0.01:
            rand_file = random.choice(os.listdir('/home/alice/.lilia/imgsrc'))
            await client.send_file(channel, '/home/alice/.lilia/imgsrc/' + rand_file)
        await asyncio.sleep(120)

async def rss_update():
    await client.wait_until_ready()
    channel = discord.Object(id='521269328046325776')
    while not client.is_closed:
        feed = feedparser.parse('https://aya.sanusi.id/feed/')
        config.read('feed.ini')
        if feed.entries[0].published != config['DEFAULT']['latest_post']:
            if len(feed.entries[0].tags) > 1:
                if feed.entries[0].tags[0].term == 'Novel' or feed.entries[0].tags[1].term == 'Novel':
                    post_type = 'Novel'
                else:
                    post_type = feed.entries[0].tags[0].term
            else:
                post_type = feed.entries[0].tags[0].term
            msg = '@everyone Master AYA just published new ' + post_type + ' on her web, the title is ' + feed.entries[0].title + ' and you can view it in here : ' + feed.entries[0].link
            config['DEFAULT']['latest_post'] = feed.entries[0].published
            with open ('feed.ini', 'w') as configfile:
                config.write(configfile)
            await client.send_message(channel, msg)
        await asyncio.sleep(300)


@client.event
async def on_member_join(member):
    msg = 'Welcome to AYA Translation, {0.mention} sama, I hope you enjoy here.'.format(member)
#    channel = client.get_channel('470591265659027468')
    channel = discord.utils.get(member.server.channels, name='general')
    role = discord.utils.get(member.server.roles, name='Commoner')
    await client.send_message(channel, msg)
    await client.add_roles(member, role)

@client.event
async def on_member_remove(member):
    msg = 'One of our dear comrade, {0} left us, let us wish the best for them'.format(member)
#    channel = client.get_channel('470591265659027468')
    channel = discord.utils.get(member.server.channels, name='general')
    await client.send_message(channel, msg)

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself

    print('[' + str(message.timestamp) + ' : ' + str(message.server) + '] ' + str(message.channel) + '->' + str(message.author) + ': ' + str(message.content))

    nsfw_channel = discord.utils.get(client.get_all_channels(), server=message.server, name='nsfw')

    file = random.choice(os.listdir('/home/alice/.lilia/imgsrc'))

    if message.author == client.user:
        return

    if uppercase_abuse(str(message.content)):
        msg = "Uppercase abuse, {0.author.mention}, you've been warned!".format(message)
        await client.send_message(message.channel, msg)

#    if str(message.author) == 'Shinobu#3641':
#        msg = 'Could you shut up Shinobu!'
#        await client.send_message(message.channel, msg)

    if message.content.startswith(('->help', '!help', '.help', '--help')):
        msg = 'I am really sorry master {0.author.mention}, the only one who can hel you is yourself, not me or anyone else'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!lilia'):
        commands = message.content.split()

        if commands[1] in {'help','->help', '!help', '.help', '--help'}:
            msg = 'I am really sorry master {0.author.mention}, the only one who can hel you is yourself, not me or anyone else'.format(message)
            await client.send_message(message.channel, msg)

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
            await client.send_message(message.channel, msg)

        elif commands[1] == 'gift':
            msg = 'This is gift from {.author.mention} for you, '.format(message) + commands[3]
            await client.send_file(nsfw_channel, '/home/alice/.lilia/imgsrc/' + file, content=msg)

        elif commands[1] == 'yuribomb':
            if len(commands) >= 3 and commands[2].isdigit():
                numbers = int(commands[2])
            else:
                numbers = 4
            if numbers <= 8:
                for i in range(numbers):
                    s_file = random.choice(os.listdir('/home/alice/.lilia/imgsrc'))
                    msg = str(i+1) + ':'
                    await client.send_file(nsfw_channel, '/home/alice/.lilia/imgsrc/' + s_file, content=msg)
            else:
                msg = 'You requesting too much, Master {0.author.mention}'.format(message)
                await client.send_message(message.channel, msg)

        elif commands[1] == 'dne' and len(commands) >= 4:
            if commands[2] == 'encode':
                msg = 'This is the result, {0.author}: '.format(message)+dne.dencode(' '.join(commands[3:len(commands)]), 'encode')
                await client.send_message(message.channel, msg)
            if commands[2] == 'decode':
                msg = 'Result: '+dne.dencode(' '.join(commands[3:len(commands)]), 'decode')
                await client.send_message(message.channel, msg)

        elif commands[1] == 'mxl' and len(commands) >= 4:
            if commands[2] == 'encode':
                msg = 'Ini hasilnya, {0.author}: '.format(message)+mxl.dencode(' '.join(commands[3:len(commands)]), 'encode')
                await client.send_message(message.channel, msg)
            if commands[2] == 'decode':
                msg = 'Hasil: '+mxl.dencode(' '.join(commands[3:len(commands)]), 'decode')
                await client.send_message(message.channel, msg)

        elif commands[1].lower() in {'hi', 'hello', 'pagi', 'siang', 'sore', 'selamat', 'met'} and len(commands) <= 3:
            msg = ' '.join(commands[1:len(commands)]) + ' juga Master {0.author.mention}'.format(message)
            await client.send_message(message.channel, msg)

#        elif commands[1] == 'find':
#            query = ' '.join(commands[2:len(commands)])
#            file_name = file_name_generator()
#            image_dl.run(query, '/home/alice/.lilia/', num_images=1, images_name=file_name)
#            check_file = glob.glob('/home/alice/.lilia/' + file_name + '*')
#            if check_file:
#                img_file = str(os.path.basename(check_file[0]))
#                msg = 'Ini ' + query + ' yang anda minta, Master {0.author.mention}'.format(message)
#                await client.send_file(message.channel, img_file, content=msg)
#            else:
#                msg = 'Maaf sekali {0.author.mention}, Saya tidak bisa memenuhi permintaan Anda.'.format(message)
#                await client.send_message(message.channel, msg)

        else:
            query = ' '.join(commands[1:len(commands)])
            msg = 'Master, what do you mean wuth ' + query + '? I do not undersatnd.'
            await client.send_message(message.channel, msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='with AYA on her bed'))

#client.loop.create_task(random_post_nsfw())
client.loop.create_task(rss_update())
client.run(TOKEN)
