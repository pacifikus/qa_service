import os
from dataclasses import dataclass
from typing import List

import prettytable as pt
import telebot
from dotenv import load_dotenv
from telebot import types

load_dotenv()

tg_token = os.getenv("TG_TOKEN")
bot = telebot.TeleBot(tg_token)


@dataclass
class TableRow:
    question: str
    url: str


def start_search(text):
    return [
        TableRow(
            "PLS-DA on sklearn: correlated features",
            "https://datascience.stackexchange.com/questions/70312/"
            "pls-da-on-sklearn-correlated-features",
        ),
        TableRow(
            "Lasso regression / SVM convergence CPU -> GPU",
            "https://datascience.stackexchange.com/questions/116258/"
            "lasso-regression-svm-convergence-cpu-gpu",
        ),
        TableRow(
            "Normalize predictors in random forest",
            "https://datascience.stackexchange.com/questions/116272/"
            "normalize-predictors-in-random-forest",
        ),
    ]


def format_answer(data: List[TableRow]):
    table = pt.PrettyTable(["Result"])
    table.align["Result"] = "c"

    for item in data:
        table.add_row([item.question])
        table.add_row([item.url + "\n"])

    return f"```{table}```"


@bot.message_handler(content_types=["text"], commands=["start"])
def handle_item_name(message: types.Message):
    text = (
        "Hello! I'm ML QA bot.\nType your question about Data Science"
        " here and I'll try to find similar questions with answers"
        " on StackExchange"
    )
    message = bot.send_message(
        message.from_user.id,
        text=text,
    )
    bot.register_next_step_handler(message, callback_worker)


def callback_worker(message: types.Message):
    data = start_search(message.text)
    answer = format_answer(data)
    message = bot.send_message(
        message.from_user.id,
        text=answer,
        parse_mode="MarkdownV2",
    )
    bot.register_next_step_handler(message, callback_worker)


if __name__ == "__main__":
    bot.infinity_polling()
