"""
main.py
"""

import logging
import json
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
from dictionary.get_random_definitions import fetch_random_definitions

import config


# Commands
async def random_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Get a random definition
    """
    definition_dict = fetch_random_definitions()
    for item in definition_dict:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'<b>{item["word"]}</b>\n\n{item["meaning"]}\n\n<i>{item["example"]}</i>', parse_mode=ParseMode.HTML)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Get help
    """
    await update.message.reply_text('Help!')


# Responses
def handle_response(text: str) -> str:
    """
    Handle the user's message
    """
    if text == 'hello':
        return 'Hey there'
    if text == 'bye':
        return 'Bye'
    return 'I dont know that'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the user's message
    """
    message_type: str = update.message.chat.type
    text: str = update.message.text
    logging.info(
        'User (%s) in %s: "%s"', update.message.chat.id, message_type, text)

    if message_type == 'private':
        response: str = handle_response(text)
    else:
        if config.BOT_NAME in text:
            response: str = handle_response(
                text.replace(config.BOT_NAME, '').strip())
        else:
            return
    logging.debug('Bot: %s', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f'Update {update} caused error {context.error}')


async def process_tg_event(event):
    logging.info(f'Bot {config.BOT_NAME} is starting up...')
    bot_app = Application.builder().token(config.TOKEN).build()
    bot_app.add_handler(CommandHandler('help', help_command))
    bot_app.add_handler(CommandHandler('random', random_command))
    bot_app.add_handler(MessageHandler(filters.TEXT, handle_message))
    bot_app.add_error_handler(error)
    try:
        await bot_app.initialize()
        await bot_app.process_update(
            Update.de_json(json.loads(event["body"]), bot_app.bot)
        )

        return {
            'statusCode': 200,
            'body': 'Success'
        }

    except Exception as e:
        logging.error(e)
        return {
            'statusCode': 500,
            'body': 'Failure'
        }


def lambda_handler(event, _context):
    return asyncio.get_event_loop().run_until_complete(process_tg_event(event))
