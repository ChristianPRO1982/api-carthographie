import os
from dotenv import load_dotenv

import mysql.connector

class cARThographieDB:
    def __init__(self):
        load_dotenv(override=True) # uniquement en DEV local
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        if self.DEBUG:
            print("DEBUG mode is ON")
            self.host = os.getenv("LOCAL_FUNCTIONAL_HOST")
            self.user = os.getenv("LOCAL_FUNCTIONAL_USER")
            self.password = os.getenv("LOCAL_FUNCTIONAL_PASSWORD")
            self.database = os.getenv("LOCAL_FUNCTIONAL_DATABASE")
        else:
            print("DEBUG mode is OFF")
            self.host = os.getenv("DOCKER_MYSQL_HOST")
            self.user = os.getenv("DOCKER_MYSQL_USER")
            self.password = os.getenv("DOCKER_MYSQL_PASSWORD")
            self.database = os.getenv("DOCKER_MYSQL_DATABASE")
            print("host: ", self.host)
            print("user: ", self.user)
            print("password: ", self.password)
            print("database: ", self.database)
        self.connection = None
        self.SQL_LIMIT = os.getenv("SQL_LIMIT", 1000)


    def connect(self):
        if not self.connection or not self.connection.is_connected():
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        return self.connection


    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None


    def get_all_songs_pages(self):
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CEIL(COUNT(1) / {self.SQL_LIMIT}) AS pages,
       {self.SQL_LIMIT} AS song_per_page
  FROM l_songs
""")
        songs = cursor.fetchall()
        cursor.close()
        self.close()
        return songs


    def table_c_artists(self, api_key: str)-> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO c_artists VALUES (', artist_id, ', "', REPLACE(name, '"', '“'),'");') AS value
  FROM c_artists
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()

        return json
    

    def table_c_artist_links(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO c_artist_links VALUES (', artist_id, ', "', REPLACE(link, '"', '“'),'");') AS value
  FROM c_artist_links
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json
    

    def table_c_bands(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO c_bands VALUES (', band_id, ', "', REPLACE(name, '"', '“'),'");') AS value
  FROM c_bands
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json
    

    def table_c_band_links(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO c_band_links VALUES (', band_id, ', "', REPLACE(link, '"', '“'),'");') AS value
  FROM c_band_links
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json
    

    def table_c_group_user(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO c_group_user VALUES (', group_id, ', "', username,'", ', admin, ');') AS value
  FROM c_group_user
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json
    

    def _table_c_group_user_ask_to_join(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO c_group_user_ask_to_join VALUES (', group_id, ', "', username,'");') AS value
  FROM c_group_user_ask_to_join
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json
    

    def table_c_groups(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO c_groups VALUES (', group_id, ', "', name,'", "', REPLACE(info, '"', '“'),'", "', IFNULL(token, ""), '", ', private, ');') AS value
  FROM c_groups
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json
    

    def table_c_user_change_email(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO c_user_change_email VALUES ("', username, '", "', token, '", "', create_time, '", "', last_email, '", "', new_email, '");') AS value
  FROM c_user_change_email
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json

    def table_c_users(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO c_users VALUES ("', username,'", "', REPLACE(theme, '"', '“'),'");') AS value
  FROM c_users
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json
    

    def table_l_genres(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO l_genres VALUES (', genre_id, ', "', REPLACE(`group`, '"', '“'), '", "', REPLACE(name, '"', '“'), '");') AS value
  FROM l_genres
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json


    def table_l_site(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO l_site VALUES ("', language, '", "', REPLACE(title, '"', '“'), '", "', REPLACE(title_h1, '"', '“'), '", "', REPLACE(home_text, '"', '“'), '", "', REPLACE(bloc1_text, '"', '“'), '", "', REPLACE(bloc2_text, '"', '“'), '");') AS value
  FROM l_site
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json
    

    def table_l_site_params(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO l_site_params VALUES (', verse_max_lines, ', ', verse_max_characters_for_a_line, ', "', REPLACE(FR_chorus_prefix, '"', '“'), '", "', REPLACE(FR_verse_prefix1, '"', '“'), '", "', REPLACE(FR_verse_prefix2, '"', '“'), '", "', REPLACE(EN_chorus_prefix, '"', '“'), '", "', REPLACE(EN_verse_prefix1, '"', '“'), '", "', REPLACE(EN_verse_prefix2, '"', '“'), '");') AS value
  FROM l_site_params
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json
    

    def table_l_songs(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO l_songs VALUES (', song_id, ', "', REPLACE(title, '"', '“'), '", "', REPLACE(sub_title, '"', '“'), '", "', REPLACE(description, '"', '“'), '", ', status, ', ', licensed, ');') AS value
  FROM l_songs
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json
    

    def table_l_song_artists(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO l_song_artists VALUES (', song_id, ', ', artist_id, ');') AS value
  FROM l_song_artists
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json
    

    def table_l_song_bands(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO l_song_bands VALUES (', song_id, ', ', band_id, ');') AS value
  FROM l_song_bands
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json


    def _table_l_song_genre(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO l_song_genre VALUES (', song_id, ', ', genre_id, ');') AS value
  FROM l_song_genre
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json
    

    def table_l_song_link(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO l_song_link VALUES (', song_id, ', "', link, '");') AS value
  FROM l_song_link
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json
    

    def table_l_songs_mod_message(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}

        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO l_songs_mod_message VALUES (', message_id, ', ', song_id, ', "', message, '", ', status,', "', date, '");') AS value
  FROM l_songs_mod_message
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json
    

    def table_l_verses(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO l_verses VALUES (', verse_id, ', ', song_id, ', ', num, ', ', num_verse, ', ', chorus, ', ', followed, ', ', notcontinuenumbering, ', "', text, '", "', IFNULL(prefix, ""), '");') AS value
  FROM l_verses
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json
    

    def table_l_verse_prefixes(self, api_key: str) -> list:
        if api_key != os.getenv("API_KEY"):
            return {"error": "Unauthorized"}
        
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(f"""
SELECT CONCAT('INSERT INTO l_verse_prefixes VALUES (', prefix_id, ', "', prefix, '", "', comment, '");') AS value
  FROM l_verse_prefixes
""")
        inserts = cursor.fetchall()
        cursor.close()

        json = []
        for insert in inserts:
            fields = {}
            fields["INSERT"] = insert
            json.append(fields)

        self.close()
        return json