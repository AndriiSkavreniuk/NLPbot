import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import get_intent
from big_config import BOT_CONFIG
from gen_resp import get_generative_response


def get_response_by_intent(intent):
    phrases = BOT_CONFIG['intents'][intent]['responses']
    return random.choice(phrases)


def get_phailure_phrase():
    phrases = BOT_CONFIG['failure_phrases']
    return random.choice(phrases)


stats = {'intent': 0, 'generative': 0, 'stub': 0}


def go_bot(text):
    """Генерация ответной реплики"""
    # NLU
    intent = get_intent.get_intent(text)

    # Generate answer

    # rules
    if intent:
        stats['intent'] += 1
        return get_response_by_intent(intent)

    # use generative model
    response = get_generative_response(text)
    if response:
        stats['generative'] += 1
        return response

    # stub
    stats['stub'] += 1
    return get_phailure_phrase()


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def bot_answer(update, context):
    """Echo the user message."""
    question = update.message.text
    answer = go_bot(question)
    print(question, answer)
    print(stats)
    print()
    update.message.reply_text(answer)


def main():
    """Start the bot."""
    updater = Updater("bot_token", use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, bot_answer))

    # Start the Bot
    updater.start_polling()
    updater.idle()


go_bot('о чем думаешь?')