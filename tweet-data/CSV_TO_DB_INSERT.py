import csv
import sqlite3
import json

input_csv_path = '/Users/kristianbanchs/Desktop/Twitar/tweet-data/bio_set_1.csv'
output_db_path = '/Users/kristianbanchs/Desktop/Twitar/tweet-data/bio_set_1.sqlite'
media_url = None

# Connect to SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect(output_db_path)
cursor = conn.cursor()

# Create the tweets table if it does not exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tweets (
        id TEXT UNIQUE NOT NULL,
        created_at TEXT,
        screen_name TEXT,
        profile_img TEXT,
        verified INTEGER CHECK(verified IN (0, 1)),
        text TEXT,
        media TEXT,
        urls TEXT,
        thumbnail TEXT,
        favorite_count INTEGER,
        view_count INTEGER,
        retweet_count INTEGER,
        score INTEGER CHECK(score BETWEEN 0 and 5)
    );
""")

# Template for inserting data into the tweets table
insert_template = """INSERT OR IGNORE INTO tweets (id, created_at, screen_name, profile_img, verified, text, media, urls, thumbnail, favorite_count, view_count, retweet_count, score) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL);"""

with open(input_csv_path, 'r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        try:
            # Escape single quotes in text fields to prevent SQL errors
            row['text'] = row['text'].replace("'", "''")
            row['thumbnail'] = row['thumbnail'].replace("'", "''")
            row['screen_name'] = row['screen_name'].replace("'", "''")
            
            # Handling 'media' field and extracting media_url_https
            if row['media']:
                media_string = row['media'].replace("'", '"')  # Handle single quotes
                try:
                    media_data = json.loads(media_string)  # Parse media JSON
                    if isinstance(media_data, list) and 'media_url_https' in media_data[0]:
                        media_url = media_data[0]['media_url_https']
                    else:
                        print("media_url_https not found in the parsed data.")
                except json.JSONDecodeError as e:
                    print(f"JSON Decode Error in media field: {e}")
                    media_url = None  # Set media_url to None if there's a parsing error
            else:
                media_url = None  # Default to None if no media data exists

            # Handling 'urls' field and extracting 'expanded_url'
            urls = None  # Default value for urls
            if 'urls' in row and row['urls']:  # Ensure 'urls' exists and isn't empty
                try:
                    urls_data = json.loads(row['urls'].replace("'", '"'))  # Replace single quotes if needed
                    if isinstance(urls_data, list) and len(urls_data) > 0:
                        if 'expanded_url' in urls_data[0]:
                            urls = urls_data[0]['expanded_url']
                            print(f"Expanded URL: {urls}")
                        else:
                            print("expanded_url not found in the parsed data.")
                    else:
                        print("Invalid URL data format.")
                except json.JSONDecodeError as e:
                    print(f"JSON Decode Error for URLs: {e}")

            # Handling 'verified' field and ensuring it's a valid integer (0 or 1)
            verified = 1 if row['verified'] == 'True' else 0 if row['verified'] == 'False' else None

            # Gather data for insertion
            data = (
                row['id'],
                row['created_at'],
                row['screen_name'],
                row['profile_img'],
                verified,
                row['text'],
                media_url,
                urls,
                row['thumbnail'],
                int(row['favorite_count']) if row['favorite_count'] else None,
                int(row['view_count']) if row['view_count'] else None,
                int(row['retweet_count']) if row['retweet_count'] else None
            )

            # Execute the insert statement
            cursor.execute(insert_template, data)

        except sqlite3.IntegrityError as e:
            print(f"IntegrityError for ID {row['id']}: {e}")
        except ValueError as e:
            print(f"ValueError in row {row}: {e}")

# Commit the transaction and close the connection
conn.commit()
cursor.execute("SELECT COUNT(*) FROM tweets;")
row_count = cursor.fetchone()[0]
print(f"Total rows in database: {row_count}")
conn.close()
print(f"Data from {input_csv_path} has been successfully inserted into {output_db_path}")
