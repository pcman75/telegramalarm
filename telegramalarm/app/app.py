import os, json, requests, logging
from threading import Timer

import hypercorn.asyncio
from quart import Quart, redirect, render_template_string, request, url_for

from telethon import TelegramClient, events, utils
from telethon.sessions import StringSession

from hassapi import triggerSensor
from webtemplates import BASE_TEMPLATE, PHONE_FORM, CODE_FORM

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# Session name, API ID and hash to use; loaded from config file
with open('/data/options.json') as f:
  aoconfig = json.load(f)

logger.setLevel(logging._nameToLevel[aoconfig['LOG_LEVEL']])
                
# Telethon client
client = TelegramClient('/data/telegramalarm', aoconfig['TG_API_ID'], aoconfig['TG_API_HASH'])
phone = None

# Quart app
app = Quart(__name__)

# This is our update handler. It is called when a new update arrives.
@client.on(events.NewMessage())
async def handler(event):
    logger.debug(event.stringify())
    chat = await event.get_chat()
    sender = await event.get_sender()
    chat_name = utils.get_display_name(chat)
    logger.debug(f'Chat: {chat_name}')
    logger.debug(f'Sender: {utils.get_display_name(sender)}')
    logger.debug(f'Message: {event.raw_text}')
    logger.debug(f'channels: {aoconfig["channels"]}')
    if(chat_name in aoconfig['channels']):
        triggerSensor(chat_name, "on", event.raw_text, logger)
        timer = Timer(5, triggerSensor, [chat_name, "off", event.raw_text, logger])
        timer.start() # after 5 seconds, turn off the alarm


# Connect the client before we start serving with Quart
@app.before_serving
async def startup():
    await client.connect()

    #Before Telegram sends updates, you need to make a high-level request, like client.get_me()
    if await client.is_user_authorized():
        me = await client.get_me()
        for channel in aoconfig['channels']:
            triggerSensor(channel, "off", "initial", logger)

        logger.info(me.stringify())
    else:
        logger.info("Client is not authorized. Go to Ingress page")

# After we're done serving (near shutdown), clean up the client 
@app.after_serving
async def cleanup():
    await client.disconnect()

@app.route('/', methods=['GET', 'POST'])
async def root():
    # We want to update the global phone variable to remember it
    global phone

    # Check form parameters (phone/code)
    if 'phone' in request.args:
        phone = request.args['phone']
        try:
            await client.send_code_request(phone)
        except Exception as e:
            logger.error('Failed to upload to ftp: '+ str(e))
            return await render_template_string(BASE_TEMPLATE, content=str(e))

    if 'code' in request.args:
        await client.sign_in(code=request.args['code'])

    # If we're logged in, show the session string
    if await client.is_user_authorized():
        me = await client.get_me()        
        result = f'<H1>Welcome</H1><p>You are logged in to Telegram as: {utils.get_display_name(me)}</p>'

        return await render_template_string(BASE_TEMPLATE, content=result)

    # Ask for the phone if we don't know it yet
    if phone is None:
        return await render_template_string(BASE_TEMPLATE, content=PHONE_FORM)

    # We have the phone, but we're not logged in, so ask for the code
    return await render_template_string(BASE_TEMPLATE, content=CODE_FORM)


async def main():
    config = hypercorn.Config()
    config.bind = f'{os.environ["hostname"]}:{os.environ["portname"]}'
    
    await hypercorn.asyncio.serve(app, config)


# By default, `Quart.run` uses `asyncio.run()`, which creates a new asyncio
# event loop. If we create the `TelegramClient` before, `telethon` will
# use `asyncio.get_event_loop()`, which is the implicit loop in the main
# thread. These two loops are different, and it won't work.
#
# So, we have to manually pass the same `loop` to both applications to
# make 100% sure it works and to avoid headaches.
#
# To run Quart inside `async def`, we must use `hypercorn.asyncio.serve()`
# directly.
#
# This example creates a global client outside of Quart handlers.
# If you create the client inside the handlers (common case), you
# won't have to worry about any of this, but it's still good to be
# explicit about the event loop.
if __name__ == '__main__':
    client.loop.run_until_complete(main())
