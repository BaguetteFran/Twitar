import csv
import sqlite3
import json

input_csv_path = '/Users/kristianbanchs/DailyT/tweet-data/Biology_tweets_1.csv'
output_db_path = '/Users/kristianbanchs/DailyT/data-grader-tweet/trial_database_1.sqlite'
media_url = None
# Connect to SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect(output_db_path)
cursor = conn.cursor()
# Create the tweets table if it does not exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tweets (
        id TEXT PRIMARY KEY,
        created_at TEXT,
        screen_name TEXT,
        profile_img TEXT,
        verified INTEGER CHECK(score BETWEEN 0 and 1),
        text TEXT,
        img_url TEXT,
        media TEXT,
        favorite_count INTEGER,
        view_count INTEGER,
        retweet_count INTEGER,
        score INTEGER CHECK(score BETWEEN 0 and 5)
    );
""")

# Template for inserting data into the tweets table
insert_template = """INSERT OR IGNORE INTO tweets (id, created_at, screen_name, profile_img, verified, text, img_url, media, favorite_count, view_count, retweet_count, score) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL);"""

with open(input_csv_path, 'r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        try:
            # Escape single quotes in text fields to prevent SQL errors
            row['text'] = row['text'].replace("'", "''")
            row['screen_name'] = row['screen_name'].replace("'", "''")
            if row['media']:
                media_string = row['media'].replace("'",'"')
                try: 
                    media_data = json.loads(media_string)
    
                    # Step 3: Access the 'media_url_https' key in the first item of the list
                    if isinstance(media_data, list) and 'media_url_https' in media_data[0]:
                        media_url = media_data[0]['media_url_https']
                    else:
                        print("media_url_https not found in the parsed data.")
                except json.JSONDecodeError as e:
                    print("JSON Decode Error:", e)

            # Handle NULL values in optional columns
            img_url = row['img_url'].replace("'", "''") if row['img_url'] else None
            verified = 1 if row['verified'] == 'True' else 0
            # if row['verified']:
            #     verified = True
            # else:
            #     verified = False
            # Gather data for insertion
            data = (
                row['id'],
                row['created_at'],
                row['screen_name'],
                row['profile_img'],
                verified,
                row['text'],
                img_url,
                media_url,
                int(row['favorite_count']),
                int(row['view_count']),
                int(row['retweet_count'])
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
