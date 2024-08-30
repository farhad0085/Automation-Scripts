from config import Config
import requests
import pandas as pd
import os
from datetime import datetime

config = Config()


def get_poll_response():
    response = requests.get(config.poll_url, auth=config.auth).json()
    return response


def get_polls(response):
    includes = response.get("includes", None)
    if includes:
        polls = includes.get("polls", [])
        return polls
    return []


def get_current_date_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def save_polls_to_csv(polls):

    for poll in polls:
        options = poll.get("options", [])
        if not options:
            continue

        labels = ["datetime"]
        votes = [get_current_date_time()]

        total_vote = 0
        for option in options:
            label = option['label']
            vote = option['votes']
            labels.append(label)
            votes.append(vote)
            total_vote += vote

        labels.append("total")
        votes.append(total_vote)

        file_name = os.path.join(config.poll_path, f"{poll['id']}.csv")

        df_votes = pd.DataFrame([votes])
        if not os.path.exists(file_name):
            df_votes.to_csv(file_name, header=labels, index=False)
        else:
            df = pd.read_csv(file_name)
            df.loc[len(df)] = votes
            df.to_csv(file_name, index=False)


if __name__ == "__main__":
    response = get_poll_response()
    polls = get_polls(response)
    save_polls_to_csv(polls)
