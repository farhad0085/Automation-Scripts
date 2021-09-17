import config
import json
from exceptions import RequestFailed
import requests
import os
import csv
import datetime
import time


def get_data():
    url = "https://api.opensea.io/graphql/"
    headers = {
        "x-api-key": config.OPENAPI_API_KEY,
        "x-build-id": config.OPENAPI_BUILD_ID,
        'Content-Type': 'application/json',
        "user-agent": "postman",
    }

    body = {
        "id": "CollectionsScrollerQuery",
        "query": """query CollectionsScrollerQuery(
                $categories: [CategorySlug!]
            ) {
                trendingCollections(first: 12, categories: $categories) {
                    edges {
                        node {
                            ...CollectionCard_data
                        }
                    }
                }
            }
            
            fragment CollectionCard_data on CollectionType {
                id
                name
                slug
                owner {
                    displayName
                    user {
                        username
                    }
                }
            }
        """,
        "variables": {
            "categories": None
        }
    }

    try:
        response = requests.post(url, headers=headers, json=body).json()
        return response.get("data", {}).get("trendingCollections", {}).get("edges", [])
    except:
        raise RequestFailed("Request failed. Please try again later")


def get_json_data(data):
    collection_data = []

    for item in data:
        node = item.get("node") or {}
        artist = node.get("owner") or {}
        user = artist.get("user") or {}

        collection_id = node.get("id")
        collection_name = node.get("name", "")
        collection_slug = node.get("slug") or ""
        artist_display_name = artist.get("displayName", "")
        artist_url = user.get('username') or ""
        if artist_url:
            artist_url = "https://opensea.io/" + artist_url
        else:
            artist_url = ""

        collection_data.append({
            "collection_id": collection_id,
            "collection_name": collection_name,
            "collection_slug": "https://opensea.io/collection/" + collection_slug,
            "artist_display_name": artist_display_name,
            "artist_url": artist_url,
            "date_added": datetime.datetime.utcnow()
        })
    return collection_data


def write_to_csv(data, csv_file):
    create_csv_file(csv_file)

    with open(csv_file, "a", encoding="utf8", newline="") as writeFile:
        write_csv = csv.writer(writeFile)
        for item in data:
            write_csv.writerow(item.values())


def create_csv_file(csv_file):
    if not os.path.exists(csv_file):
        csv_headers = [
            'Collection ID', 'Collection Name', 'Collection URL',
            'Artist Name', 'Artist URL', "Date Added"
        ]
        with open(csv_file, "w", encoding="utf8", newline="") as write_file:
            write_csv = csv.writer(write_file)
            write_csv.writerow(csv_headers)


def get_data_from_csv(csv_file):
    create_csv_file(csv_file)

    data = []

    with open(csv_file, "r", encoding="utf8") as file:
        reader = csv.reader(file)
        for index, row in enumerate(reader):
            if index:
                data.append(row)
    return data


def get_new_collections(json_data, csv_data):
    csv_data_ids = [item[0] for item in csv_data]
    json_data_ids = [item["collection_id"] for item in json_data]

    new_ids = []
    for id in json_data_ids:
        if id not in csv_data_ids:
            new_ids.append(id)

    new_collections = list(filter(lambda x: x["collection_id"] in new_ids, json_data))
    return new_collections


def send_message_to_discord(data):
    message = f"""Hello,
    A new collection is posted.

    Collection ID: {data["collection_id"]}
    Collection Name: {data["collection_name"]}
    Collection URL: {data["collection_slug"]}
    Artist Name: {data["artist_display_name"]}
    Artist URL: {data["artist_url"]}
    Date Added: {data["date_added"]} (UTC)
    """

    json_data = {
        "content": message
    }
    response = requests.post(config.DISCORD_WEBHOOK_URL, json=json_data)
    print("A new message has been sent with following text:")
    print(message)


def main():
    csv_file = "Collection_data.csv"
    data_from_csv = get_data_from_csv(csv_file)
    json_data = get_json_data(get_data())

    new_collections = get_new_collections(json_data, data_from_csv)
    # send this new collections data to discord.
    write_to_csv(new_collections, csv_file)
    
    for collection in new_collections:
        send_message_to_discord(collection)

if __name__ == "__main__":
    while True:
        main()
        print("Sleeping for 15 minutes...")
        time.sleep(900) # run every 15 minutes