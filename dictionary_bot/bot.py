import json
import os

import telegram
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from dictionary import get_info

telegram_bot_token = ""

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher


# set up the introductory statement for the /start command
def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text="Hello there. Provide any English word and I will give you a bunch "
        "of information about it.",
    )


# obtain the information of the word provided and format before presenting
def get_word_info(update, context):
    word_info = get_info(update.message.text)

    # if the user returns an invalid word,return the custom response and exit the function
    if word_info.__class__ is str:
        update.message.reply_text(word_info)

    # Get the word the user provided
    word = word_info["word"]  # type: ignore

    # Get the origin of the word
    origin = word_info["origin"]  # type: ignore
    meanings = "\n"

    synonyms = ""
    definition = ""
    example = ""
    antonyms = ""

    # a word may have several meanings. We'll use this counter to track each of the meanings provided from the response
    meaning_counter = 1

    for word_meaning in word_info["meanings"]:  # type: ignore
        meanings += "Meaning" + str(meaning_counter) + ":\n"

        for word_definition in word_meaning["definitions"]:  # type: ignore
            # extract each of the definitions of the word
            definition = word_definition["definition"]  # type: ignore

            # extract each example for the respective definition
            if "example" in word_definition:
                example = word_definition["example"]  # type: ignore

            # extract the collection of synonyms for the word based on the defintion
            for word_synonym in word_definition["synonyms"]:  # type: ignore
                synonyms += word_synonym + ", "

            # extract the antonyms of the word based on the definition
            for word_antonym in word_definition["antonyms"]:  # type: ignore
                antonyms += word_antonym + ", "

        meanings += "Definition: " + definition + "\n\n"
        meanings += "Example: " + example + "\n\n"
        meanings += "Synonym: " + synonyms + "\n\n"
        meanings += "Antonym: " + antonyms + "\n\n\n"

        meaning_counter += 1

    # format the data into a string
    message = f"Word: {word}\n\nOrigin: {origin}\n{meanings}"

    update.message.reply_text(message)


# run the start function when the user invokes the /start command
dispatcher.add_handler(CommandHandler("start", start))

# invoke the get_word_info function when the user sends a message that is not a command
dispatcher.add_handler(MessageHandler(Filters.text, get_word_info))
updater.start_webhook(
    listen="0.0.0.0",
    port=int(os.environ.get("PORT", 5000)),
    url_path=telegram_bot_token,
    webhook_url=+telegram_bot_token,  # type: ignore
)
