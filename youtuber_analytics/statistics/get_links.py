from typing import List

import googleapiclient.discovery
import json
import re

URL_REGEX = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'


def get_youtube_api():
    api_service_name = "youtube"
    api_version = "v3"

    with open("../.creds/token.json", "r") as f:
        api_token = json.load(f)["token"]

    return googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_token)


def get_youtuber_channel_by_username(api, username):
    request = api.channels().list(
        part="snippet,contentDetails,statistics",
        forUsername=username
    )
    result = request.execute()
    if result['pageInfo']["totalResults"] > 1:
        print("More than one youtuber found, giving you the first one listed")
    return request.execute()["items"][0]


def get_playlist_items(api, playlist_id):
    playlist_items = []
    request = api.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id
    )
    result = request.execute()
    playlist_items += result["items"]
    while "nextPageToken" in result.keys():
        request = api.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            pageToken=result["nextPageToken"]
        )
        result = request.execute()
        playlist_items += result["items"]

    return playlist_items


def get_link_from_description(playlist_item) -> List[str]:
    description = playlist_item["snippet"]["description"]
    return re.findall(URL_REGEX, description)


def save_links_from_description(playlist_items):
    with open("links", "w") as f:
        for i, playlist_item in enumerate(playlist_items):
            print(f"Inspecting item no {i}")
            links = get_link_from_description(playlist_item)
            for link in links:
                print(link)
                print(link, file=f)


if __name__ == "__main__":
    api = get_youtube_api()
    youtuber = get_youtuber_channel_by_username(api, "mrbillstunes")
    playlist_id = youtuber["contentDetails"]["relatedPlaylists"]["uploads"]
    print("Getting playlist items...")
    playlist_items = get_playlist_items(api, playlist_id)
    print("Getting links...")
    save_links_from_description(playlist_items)
    print("Done")
