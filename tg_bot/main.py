import json
import os
from dataclasses import dataclass
from typing import List

import pandas as pd
import prettytable as pt
import requests
import telebot
import yaml
from dotenv import load_dotenv
from telebot import types

load_dotenv()

tg_token = os.getenv("TG_TOKEN")
bot = telebot.TeleBot(tg_token)
base_url = "https://datascience.stackexchange.com/questions/"
config_path = "params.yaml"

with open(config_path) as conf_file:
    config = yaml.safe_load(conf_file)


@dataclass
class TableRow:
    question: str
    score: float
    url: str


def get_result_from_api(input_query, index_name, n_docs, distance):
    data = {
        "query": input_query,
        "index": index_name,
        "n_docs": n_docs,
        "distance": distance,
    }
    headers = {"Accept": "application/json"}
    response = json.loads(
        requests.post(
            url=config["search_app"]["url"],
            json=data,
            headers=headers,
        ).text
    )
    return (
        response["docs"],
        response["query_time"],
        response["num_found"],
        response["query_embedding"],
    )


def start_search(text):
    docs, query_time, num_found, query_embedding = get_result_from_api(
        text,
        config["indexing"]["elastic"]["index_name"],
        5,
        "Cosine similarity",
    )
    if num_found > 0:
        df = pd.DataFrame(docs, columns=["post_id", "text", "_score", "vector", "url"])
        urls = [base_url + str(post_id) for post_id in df["post_id"].values.tolist()]
        df["url"] = urls
        result = []
        for _, row in df.iterrows():
            result.append(
                TableRow(row["text"], row["_score"], row["url"]),
            )
        return result
    return "I can't find anything :с Try again, please"


def format_answer(data: List[TableRow]):
    table = pt.PrettyTable(["Result", "Score"])
    table.align["Result"] = "c"
    table.align["Score"] = "c"

    for item in data:
        table.add_row([f"{item.question}\n{item.url}\n", item.score])
        # table.add_row([item.score])
        # table.add_row([item.url + "\n"])

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
    if type(data) != str:
        answer = format_answer(data)
    else:
        answer = data
    message = bot.send_message(
        message.from_user.id,
        text=answer,
        parse_mode="MarkdownV2",
    )
    bot.register_next_step_handler(message, callback_worker)


if __name__ == "__main__":
    bot.infinity_polling()
