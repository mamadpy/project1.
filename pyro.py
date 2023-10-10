
from json import load
from asyncio import run, sleep
from random import choice
from telethon.sync import TelegramClient
from rubpy import Client
import os
import zipfile

with open('config.json') as file:
 config = load(file)

for i in os.listdir('documents/'):
    os.remove(f'documents/{i}')

client = TelegramClient('session', config['api_id'], config['api_hash'])


async def get_channel_messages():
	async with Client(choice(['Session1', 'Session2', 'Session3', 'Session4'])) as bot:
		for url in config["channel_user"]:
			try:
				async for message in client.iter_messages(url, reverse=True):
					if message.photo != None:
						print(message.id)
						await client.download_media(message.photo, 'images/Image.png')
						print('download image')
						await bot.send_photo(config['chat_id'], 
							'images/Image.png', 
							message.text.replace("*", "")+f"\n🆑 {config['id_channel_rubika']}"
							)
						print('upload image')

					elif message.document != None:
						
						if "DocumentAttributeVideo" in str(message.document.attributes[0]):
							name1 = f"documents/{message.document.attributes[1].file_name}"
							await client.download_media(message.document, name1)
							print('download file')
							with zipfile.ZipFile(f"documents/{config['id_channel_rubika']}.zip", 'w') as myzip:
								myzip.write(name1)
								os.remove(name1)
							await bot.send_file(config['chat_id'], 
							f"documents/{config['id_channel_rubika']}.zip", 
							message.text.replace("*", "")+f"\n🆑 {config['id_channel_rubika']}"
							)
							print("upload file")
							os.remove(f"documents/{config['id_channel_rubika']}.zip")
							await sleep(config['sleep']*60)

						else:
							name2 = f"documents/{message.document.attributes[0].file_name}"
							await client.download_media(message.document, name2)
							print('download file')
							with zipfile.ZipFile(f"documents/{config['id_channel_rubika']}.zip", 'w') as myzip:
								myzip.write(name2)
								os.remove(name2)
							await bot.send_file(config['chat_id'], 
							f"documents/{config['id_channel_rubika']}.zip", 
							message.text.replace("*", "")+f"\n🆑 {config['id_channel_rubika']}"
							)
							print("upload file")
							os.remove(f"documents/{config['id_channel_rubika']}.zip")
							await sleep(config['sleep']*60)


			except Exception as e:
				print('errors: ', e)

with client:
    client.loop.run_until_complete(get_channel_messages())
run(get_channel_messages())