import time
import requests
import datetime
from datetime import timezone, timedelta
import sqlite3
import os
import re
import json
from bs4 import BeautifulSoup

##############################################################################
# 1. USER CREDENTIALS
##############################################################################

BSKY_HANDLE = "baguettefran.bsky.social"
BSKY_PASSWORD = "Bluesky4668!"

# List of target user handles we want to scrape
TARGET_HANDLES = [
"nature.com",
"naturecellbiology.bsky.social",
"natrevimmunol.bsky.social",
"edyong209.bsky.social",
"realscientists.bsky.social",
"biology.bsky.social",
"sciam.bsky.social",
"newscientist.bsky.social",
"genetics.bsky.social",
"darwinday.bsky.social",
"memesarchive.bsky.social",
"sciencenews.bsky.social",
"biotweeps.bsky.social",
"carlzimmer.bsky.social",
"fabyollaveras.bsky.social",
"sciencealert.bsky.social",
"bbcearth.bsky.social",
"enviro.bsky.social",
"health.bsky.social",
"sciencedaily.bsky.social",
"sciencefocus.bsky.social",
"horizon.bsky.social",
"chemistryworld.bsky.social",
"royalsociety.bsky.social",
"worldsciencefestival.bsky.social",
"physorg.bsky.social",
"livescience.bsky.social",
"explore.bsky.social",
"futurity.bsky.social",
"microbiomedigest.bsky.social",
"astrobiology.bsky.social",
"marinebiology.bsky.social",
"neurosciencenews.bsky.social",
"bioinformatics.bsky.social"
]


#############################################################################,
# 2. LOGIN & OBTAIN JWT TOKEN
##############################################################################

def bluesky_login(handle: str, password: str):
    """
    Logs in to Bluesky and returns an access token + some basic account info.
    """
    url = "https://bsky.social/xrpc/com.atproto.server.createSession"

    payload = {
        "identifier": handle,
        "password": password
    }

    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data["accessJwt"], data["handle"], data["did"]

##############################################################################
# 3. FETCH AUTHOR FEED WITH PAGINATION
##############################################################################

def get_author_feed(access_token: str, actor_handle: str, limit=100, cursor=None):
    url = "https://bsky.social/xrpc/app.bsky.feed.getAuthorFeed"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "actor": actor_handle,
        "limit": limit
    }
    if cursor:
        params["cursor"] = cursor

    for attempt in range(5):  # Retry up to 5 times
        try:
            resp = requests.get(url, headers=headers, params=params)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.HTTPError as e:
            if resp.status_code == 429:
                wait_time = 2 ** attempt
                print(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e

##############################################################################
# 4. FILTER POSTS FOR THE LAST 24 HOURS
##############################################################################

def filter_posts_last_24h(feed_items):
    now_utc = datetime.datetime.now(timezone.utc)
    three_day_ago = now_utc - timedelta(days=3)

    recent_posts = []
    print(len(feed_items), ": LENGTHTHTTT")
    
    for item in feed_items:
        post = item.get("post", {})
        record = post.get("record", {})
        embed = record.get("embed", {})


        created_at_str = record.get("createdAt")
        
        if not created_at_str:
            continue
        
        ### CHEKING NORMAL POST AS WELL
        # if "reply" in record: 
        #     continue

        # if embed.get("$type") == "app.bsky.embed.record":
        #     continue

        ## DONE CHECKING 


        try:
            created_at_dt = datetime.datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
        except ValueError:
            continue
        if created_at_dt >= three_day_ago:
            recent_posts.append(item)
        
    print("RECENT POSTS LEN: ", len(recent_posts))
    return recent_posts

##############################################################################
# 5. FETCH OPEN GRAPH METADATA
##############################################################################

# def fetch_open_graph_metadata(url):
#     """
#     Fetch Open Graph metadata from the given URL.
#     Returns a dictionary with 'title', 'description', and 'image'.
#     """
#     try:
#         response = requests.get(url, timeout=5)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, 'html.parser')


#         metadata = {
#             'title': soup.find('meta', property='og:title')['content'] if soup.find('meta', property='og:title') else None,
#             'description': soup.find('meta', property='og:description')['content'] if soup.find('meta', property='og:description') else None,
#             'image': soup.find('meta', property='og:image')['content'] if soup.find('meta', property='og:image') else None
#         }

#         return metadata
#     except Exception as e:
#         print(f"Error fetching Open Graph metadata for {url}: {e}")
#         return None

##############################################################################
# 6. EXTRACT RELEVANT DATA FROM EACH POST
##############################################################################

def extract_links_from_facets(facets):
    """
    Extract links from the facets field.
    """
    links = []
    if not facets:
        return links

    for facet in facets:
        features = facet.get("features", [])
        for feature in features:
            if feature.get("$type") == "app.bsky.richtext.facet#link":
                links.append(feature.get("uri"))
    return links

def extract_embedded_media(post):
    
    
    """
    Extracts media links from various embed types such as images, external links, videos, etc.
    """
    record = post.get("record")
    embed = record.get("embed")
    author = post.get("author")

    return_pair = ("", "")
    if not embed:
        return return_pair

    embed_type = embed.get("$type")



    ## Checking isf we have an IMAGE data type and returning
    if embed_type == "app.bsky.embed.images":
        print("WE GOT AN IMAGE!")
        images = embed["images"]
        image_data = []
        for image in images:
            image_data.append({
                "did": author.get("did"),
                "alt_text": image.get("alt"),
                "image_link": image["image"]["ref"]["$link"],
                "mime_type": image["image"]["mimeType"],
                "size": image["image"]["size"]
            })
        json_string = json.dumps(image_data)
        return_pair = ("image", json_string)
        return return_pair

    ## Checking isf we have an EXTERNAL data type and returning
    elif "app.bsky.embed.external" in embed_type:
        print("WE GOT AN EXTERNAL!")
        external_data = []
        external = embed.get("external", {})
        thumb = external.get("thumb")
        ref = thumb.get("ref")
        print("THIS iS THE STUFF: ", external.get("uri"), ref.get("$link"))
        external_data.append({
            "uri": external.get("uri"),
            "did": author.get("did"),
            "title": external.get("title"),
            "description": external.get("description"),
            "thumb": ref.get("$link")
        })
        json_string = json.dumps(external_data)
        return_pair = ("external", json_string)
        return return_pair

    ## Checking isf we have an RECORDWITHMEDIA data type and returning
    # elif embed_type == "app.bsky.embed.recordWithMedia":
    #     media = embed.get("media", {})
    #     if media.get("$type") == "app.bsky.embed.images":
            
    #         for image in media.get("images", []):
    #             pic = image.get("image")
    #             ref = pic.get("ref")
    #             link = ref.get("$link")
    #             media_links.append(link)
                
    #     elif media.get("$type") == "app.bsky.embed.external":
    #         media_links.append(media.get("uri"))
    #     json_string = json.dumps(external_data)
    #     return_pair = ("external", json_string)
    #     return return_pair

    return return_pair

def extract_photo_links(text):
    """
    Extract photo URLs from the text content using a regex.
    """
    image_url_pattern = r'(https?://\S+\.(?:png|jpe?g|gif))'
    return re.findall(image_url_pattern, text)

def parse_post_data(feed_item):
    post = feed_item.get("post", {})
    author = post.get("author", {})
    record = post.get("record", {})

    # Basic fields
    profile_name = author.get("displayName") or author.get("handle", "Unknown")
    profile_pic = author.get("avatar", None)
    text_content = record.get("text", "")
    created_at = record.get("createdAt", "")

    # Engagement metrics
    reply_count = post.get("replyCount", 0)
    repost_count = post.get("repostCount", 0)
    like_count = post.get("upvoteCount", 0)

    # Extract photo links from text content
    photo_links = extract_photo_links(text_content)

    # Extract links from facets
    facets = record.get("facets", [])
    facet_links = extract_links_from_facets(facets)

    # Extract embedded media links
    
    media_pair = extract_embedded_media(post)

    # Fetch metadata for each link and add it to embeds

    # if media_pair[0] == "external": 
    #     retrieved_data = json.loads(media_pair[1])
    #     metadata = fetch_open_graph_metadata(media_pair[1].)
    #     if metadata:
    #         embeds.append({
    #             "type": "link",
    #             "url": link,
    #             "title": metadata.get("title"),
    #             "description": metadata.get("description"),
    #             "thumbnail": metadata.get("image")
    #         })
    #     else:
    #         embeds.append({
    #             "type": "link",
    #             "url": link,
    #             "title": None,
    #             "description": None,
    #             "thumbnail": None
    #         })

    # print(f"Photo links found: {photo_links}")
    # print(f"Facet links found: {facet_links}")
    # print(f"Embedded media links found: {embed_links}")

    return {
        "handle": author.get("handle", "Unknown"),
        "display_name": profile_name,
        "avatar": profile_pic,
        "text_content": text_content,
        "created_at": created_at,
        "like_count": like_count,
        "repost_count": repost_count,
        "reply_count": reply_count,
        "media": media_pair[1],
        "media_type": media_pair[0]
    }

##############################################################################
# 7. DATABASE FUNCTIONS
##############################################################################

def init_db(db_path="bluesky_posts_1.sqlite"):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    create_posts_table_sql = """
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        handle TEXT,
        display_name TEXT,
        avatar TEXT,
        text_content TEXT,
        created_at TEXT,
        like_count INTEGER,
        repost_count INTEGER,
        reply_count INTEGER,
        media TEXT,  -- Store media as JSON string
        media_type TEXT,
        score INTEGER
    );
    """
    conn.execute(create_posts_table_sql)
    return conn

def insert_post(conn, post_data):
    print("GOT CALLED")
    insert_sql = """
    INSERT INTO posts
      (handle, display_name, avatar, text_content, created_at,
       like_count, repost_count, reply_count, media, media_type)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    cursor = conn.execute(insert_sql, (
        post_data["handle"],
        post_data["display_name"],
        post_data["avatar"],
        post_data["text_content"],
        post_data["created_at"],
        post_data["like_count"],
        post_data["repost_count"],
        post_data["reply_count"],
        post_data["media"],  # Media JSON string
        post_data["media_type"]
    ))
    conn.commit()

# def insert_embed(conn, post_id, embed_data):
#     insert_sql = """
#     INSERT INTO embeds
#       (post_id, type, url, title, description, thumbnail)
#     VALUES (?, ?, ?, ?, ?, ?);
#     """
#     conn.execute(insert_sql, (
#         post_id,
#         embed_data["type"],
#         embed_data.get("url"),
#         embed_data.get("title"),
#         embed_data.get("description"),
#         embed_data.get("thumbnail"),
#     ))

##############################################################################
# 8. MAIN SCRIPT
##############################################################################

def main():
    access_token, my_handle, my_did = bluesky_login(BSKY_HANDLE, BSKY_PASSWORD)
    print(f"Logged in as: {my_handle} (DID: {my_did})")

    conn = init_db("bluesky_posts_1.sqlite")

    for target in TARGET_HANDLES:
        print(f"\nProcessing handle: {target}")
        try:
            data = get_author_feed(access_token, target, limit=100)
            feed_items = data.get("feed", [])
            cursor = data.get("cursor", None)

            recent_posts = filter_posts_last_24h(feed_items)
            print(len(recent_posts), " :THIS SHOULD BE 12")

            for item in recent_posts:
                # Write the full post data to a JSON file for inspection
                print("IN ITEM")
                parsed = parse_post_data(item)
                print("PARSED")
                insert_post(conn, parsed)
                print("inserted")

                

            time.sleep(1)
            print(f"Inserted {len(recent_posts)} post(s) from {target} into the database.")

        except requests.HTTPError as e:
            print(f"Error fetching feed for {target}: {e}")
        except Exception as ex:
            print(f"Unexpected error for {target}: {ex}")

    conn.close()
    print("\nDone. All posts saved in 'bluesky_posts_1.sqlite'.")

if __name__ == "__main__":
    main()