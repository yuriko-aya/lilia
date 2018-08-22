#!/usr/bin/env python3

import discord
import string
import random
import glob
import os
import asyncio
from pathlib import Path
import image_dl
import dne
import mxl

TOKEN = 'NDYzNTI0NzU4MTU2MzQ1MzQ2.DhzHmw.FURe39VzD4WXzkgZ_LG5iNeX6vU'

client = discord.Client()

def file_name_generator(size=8, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))
    
def get_file_name(image):
    return print(glob.glob('E:/alice/.lilia/' + image + '*')[0])
    
def uppercase_abuse(message):
    words = message.split()
    upnum = len([word for word in words if word.isupper()])
    lonum = len([word for word in words if word.islower()])
    tinum = len([word for word in words if word.istitle()])
    mixnum = len([word for word in words if not word.islower() and not word.isupper() and not word.istitle()])
    if len(words) >= 3:
        return int(lonum)+int(tinum) < int(upnum)#+int(mixnum) 
    
async def random_post_nsfw():
    await client.wait_until_ready()
#    channel = discord.Object(id='464298646440116224') #nsfw LTF
    channel = discord.Object(id='462828782454177812') #nsfw YL
    while not client.is_closed:
        if random.random() < 0.01:
            rand_file = random.choice(os.listdir('E:/alice/.lilia/imgsrc'))
            await client.send_file(channel, 'E:/alice/.lilia/imgsrc/' + rand_file)
        await asyncio.sleep(120)

@client.event
async def on_member_join(member):
    msg = 'Selamat datang {0.mention} di Yuri Lovers, silahkan baca #rules dan #announcement dulu baru cari pasangan'.format(member)
    channel = client.get_channel('462858637845725195')
    await client.send_message(channel, msg)

@client.event    
async def on_member_remove(member):
    msg = 'Selamat jalan {0.mention}, terima kasih atas kunjungannya, kami tunggu kedatangan anda kembali'.format(member)
    channel = client.get_channel('462858637845725195')
    await client.send_message(channel, msg)

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
        
    print('[' + str(message.timestamp) + ' : ' + str(message.server) + '] ' + str(message.channel) + '->' + str(message.author) + ': ' + str(message.content))
        
    nsfw_channel = discord.utils.get(client.get_all_channels(), server=message.server, name='nsfw')
    
    file = random.choice(os.listdir('E:/alice/.lilia/imgsrc'))

    if message.author == client.user:
        return
        
    if uppercase_abuse(str(message.content)):
        msg = "Penyalah gunaan huruf besar, {0.author.mention}, Anda telah diperingatkan!".format(message)
        await client.send_message(message.channel, msg)
    
#    if str(message.author) == 'Shinobu#3641':
#        msg = 'Could you shut up Shinobu!'
#        await client.send_message(message.channel, msg)

    if message.content.startswith(('->help', '!help', '.help', '--help')):
        msg = 'Maaf sekali master {0.author.mention}, hanya Anda yang dapat membantu diri Anda sendiri. Bukan Saya atau orang lain. Atau Anda bisa bertanya pada master <@346541452807110666>'.format(message)
        await client.send_message(message.channel, msg)
                
    if message.content.startswith('!lilia'):
        commands = message.content.split()
        
        if commands[1] in {'help','->help', '!help', '.help', '--help'}:
            msg = 'Maaf sekali master {0.author.mention}, hanya Anda yang dapat membantu diri Anda sendiri. Bukan Saya atau orang lain. Atau Anda bisa bertanya pada master <@346541452807110666>'.format(message)
            await client.send_message(message.channel, msg)
                
        elif commands[1] == 'commands':
            msg = """ 
Hello, my name Lilia Anabel.
I only available at Yuri Lovers server.
you can use me with `!lilia` as prefix.
I'm just created recently by my master so I don't have a lot function

**gift**:
command: `!lilia gift to @user`
gift nswf image and mention @user

**yuribomb**:
command: `!lilia yuribomb number`
post multiple nsfw images, number is optional, max 8

**find**:
command: `!lilia find something`
retrive first image from google image with provided query(ies)

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
            msg = 'Ini gift dari {.author.mention} untuk Anda, '.format(message) + commands[3]
            await client.send_file(nsfw_channel, 'E:/alice/.lilia/imgsrc/' + file, content=msg)
        
        elif commands[1] == 'yuribomb':
            if len(commands) >= 3 and commands[2].isdigit():
                numbers = int(commands[2])
            else:
                numbers = 4
            if numbers <= 8:
                for i in range(numbers):
                    s_file = random.choice(os.listdir('E:/alice/.lilia/imgsrc'))
                    await client.send_file(nsfw_channel, 'E:/alice/.lilia/imgsrc/' + s_file)
            else:
                msg = 'Anda meminta terlalu banyak, Master {0.author.mention}'.format(message)
                await client.send_message(message.channel, msg)    
        
        elif commands[1] == 'dne' and len(commands) >= 4:
            if commands[2] == 'encode':
                msg = 'Ini hasilnya, {0.author}: '.format(message)+dne.dencode(' '.join(commands[3:len(commands)]), 'encode')
                await client.send_message(message.channel, msg)
            if commands[2] == 'decode':
                msg = 'Hasil: '+dne.dencode(' '.join(commands[3:len(commands)]), 'decode')
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
        
        elif commands[1] == 'find':
            query = ' '.join(commands[2:len(commands)])
            file_name = file_name_generator()
            image_dl.run(query, 'E:/alice/.lilia/', num_images=1, images_name=file_name)
            check_file = glob.glob('E:/alice/.lilia/' + file_name + '*')
            if check_file:
                img_file = str(os.path.basename(check_file[0]))
                msg = 'Ini ' + query + ' yang anda minta, Master {0.author.mention}'.format(message)
                await client.send_file(message.channel, img_file, content=msg)
            else:
                msg = 'Maaf sekali {0.author.mention}, Saya tidak bisa memenuhi permintaan Anda.'.format(message)
                await client.send_message(message.channel, msg)
                
        else:
            query = ' '.join(commands[1:len(commands)])
            msg = 'Master, apa maksud anda dengan ' + query + '? Saya sama sekali tidak mengerti maksud Anda.'
            await client.send_message(message.channel, msg)
        
        
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='with Aya in PC'))

client.loop.create_task(random_post_nsfw())
client.run(TOKEN)
