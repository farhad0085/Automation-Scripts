import config
import json
from exceptions import RequestFailed
import requests
import os
import csv
import datetime
import time
from pprint import pprint


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
    csv_headers = [
        'Collection ID', 'Collection Name', 'Collection URL',
        'Artist Name', 'Artist URL', "Date Added", "Date Removed"
    ]
    with open(csv_file, "w", encoding="utf8", newline="") as write_file:
        write_csv = csv.writer(write_file)
        write_csv.writerow(csv_headers)
        for item in data:
            write_csv.writerow(item)


def create_csv_file(csv_file):
    if not os.path.exists(csv_file):
        csv_headers = [
            'Collection ID', 'Collection Name', 'Collection URL',
            'Artist Name', 'Artist URL', "Date Added", "Date Removed"
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
    
    # adding deleted time
    new_items = []
    for item in list(new_collections):
        item["date_removed"] = None
        new_items.append(item)
    return new_items


def send_message_to_discord(data, title=""):
    if not title:
        title = "A new collection is posted."
    
    if data["date_removed"]:
        date_removed_message = f"Date removed: {data['date_removed']} (UTC)"
    else:
        date_removed_message = ''

    message = f"""Hello,
    {title}

    Collection ID: {data["collection_id"]}
    Collection Name: {data["collection_name"]}
    Collection URL: {data["collection_slug"]}
    Artist Name: {data["artist_display_name"]}
    Artist URL: {data["artist_url"]}
    Date Added: {data["date_added"]} (UTC)
    {date_removed_message}
    """

    json_data = {
        "content": message
    }
    response = requests.post(config.DISCORD_WEBHOOK_URL, json=json_data)
    print("A new message has been sent with following text:")
    print(message)


def get_removed_items(csv_data, api_data):
    csv_ids = [item[0] for item in csv_data]
    api_ids = [item["collection_id"] for item in api_data]

    deleted_ids = []
    for id in csv_ids:
        if id not in api_ids:
            deleted_ids.append(id)

    deleted_objs = filter(lambda x: x[0] in deleted_ids, csv_data)
    removed_objs = []
    for item in list(deleted_objs):
        if not item[6]:
            item[6] = datetime.datetime.utcnow()
        removed_objs.append(item)
    return removed_objs


def get_final_data(old_collections, new_collections, deleted_collections):
    output = []

    deleted_collections_ids = [item[0] for item in deleted_collections]
    old_collections_ids = [item[0] for item in old_collections]

    final_old_collections = []
    for old_id in old_collections_ids:
        old_obj = next(filter(lambda x: x[0] == old_id, old_collections))
        if old_id in deleted_collections_ids:
            deleted_obj = next(filter(lambda x: x[0] == old_id, deleted_collections))
            old_obj[6] = deleted_obj[6]
            final_old_collections.append(old_obj)
        else:
            final_old_collections.append(old_obj)
    
    output += final_old_collections
    output += [list(item.values()) for item in new_collections]
    return output


def main():
    csv_file = "Collection_data.csv"
    data_from_csv = get_data_from_csv(csv_file)
    json_data = get_json_data(get_data())

    new_collections = get_new_collections(json_data, data_from_csv)
    
    
    last_12_items_from_csv = data_from_csv[-12:]
    deleted_objs = get_removed_items(last_12_items_from_csv, json_data)
    final_data = get_final_data(data_from_csv, new_collections, deleted_objs)

    # send this new collections data to discord.
    write_to_csv(final_data, csv_file)
    
    for collection in new_collections:
        send_message_to_discord(collection)
    for collection in deleted_objs:
        send_message_to_discord(collection, message="A collection is deleted.")

if __name__ == "__main__":
    while True:
        main()
        print("Sleeping for 15 minutes...")
        time.sleep(900) # run every 15 minutes