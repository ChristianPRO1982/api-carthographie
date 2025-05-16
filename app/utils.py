import os
from dotenv import load_dotenv

import mysql.connector

class cARThographieDB:
    def __init__(self):
        load_dotenv()
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        if self.DEBUG:
            print("DEBUG mode is ON")
            self.host = os.getenv("LOCAL_FUNCTIONAL_HOST")
            self.user = os.getenv("LOCAL_FUNCTIONAL_USER")
            self.password = os.getenv("LOCAL_FUNCTIONAL_PASSWORD")
            self.database = os.getenv("LOCAL_FUNCTIONAL_DATABASE")
        else:
            print("DEBUG mode is OFF")
            self.host = os.getenv("DOCKER_FUNCTIONAL_HOST")
            self.user = os.getenv("DOCKER_FUNCTIONAL_USER")
            self.password = os.getenv("DOCKER_FUNCTIONAL_PASSWORD")
            self.database = os.getenv("DOCKER_FUNCTIONAL_DATABASE")
        self.connection = None


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


    def get_all_songs_title(self):
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("""
  SELECT CONCAT(title,
                CASE
                    WHEN sub_title != '' THEN CONCAT(' - ', sub_title)
                    ELSE ''
                END,
                CASE
                    WHEN artist != '' THEN CONCAT(' [', artist, ']')
                    ELSE ''
                END) AS full_title,
         CONCAT("https://www.carthographie.fr/songs/song/",
                song_id,
                "/") AS url
    FROM l_songs ls
ORDER BY title, sub_title
""")
        songs = cursor.fetchall()
        cursor.close()
        self.close()
        return songs


    def get_all_songs_verses(self):
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("""
   SELECT CONCAT(ls.title,
                 CASE
                     WHEN ls.sub_title != '' THEN CONCAT(' - ', ls.sub_title)
                     ELSE ''
                 END,
                 CASE
                     WHEN ls.artist != '' THEN CONCAT(' [', ls.artist, ']')
                     ELSE ''
                 END) AS full_title,
          CONCAT("https://www.carthographie.fr/songs/song/",
                 ls.song_id,
                 "/") AS url,
          lv.`text`,
          lv.num,
          lv.num_verse,
          lv.chorus,
          lv.followed
     FROM l_songs ls
LEFT JOIN l_verses lv ON lv.song_id = ls.song_id
 ORDER BY ls.title, ls.sub_title, lv.num
""")
        songs = cursor.fetchall()
        cursor.close()
        self.close()
        return songs


    def get_all_songs_full(self):
        self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("""
   SELECT CONCAT(ls.title,
                 CASE
                     WHEN ls.sub_title != '' THEN CONCAT(' - ', ls.sub_title)
                     ELSE ''
                 END,
                 CASE
                     WHEN ls.artist != '' THEN CONCAT(' [', ls.artist, ']')
                     ELSE ''
                 END) AS full_title,
          CONCAT("https://www.carthographie.fr/songs/song/",
                 ls.song_id,
                 "/") AS url,
          lv.`text`,
          lv.num,
          lv.num_verse,
          lv.chorus,
          lv.followed
     FROM l_songs ls
LEFT JOIN l_verses lv ON lv.song_id = ls.song_id
 ORDER BY ls.title, ls.sub_title, lv.num
""")
        songs_full = cursor.fetchall()
        cursor.close()

        songs = []
        full_title = ""
        for song in songs_full:
            if song["full_title"] != full_title:
                if full_title != "":
                    full_text = self.get_lyrics(verses)
                    songs.append({
                        "full_title": full_title,
                        "url": song["url"],
                        "text": full_text
                    })
                full_title = song["full_title"]
                verses = []
            else:
                fields = {}
                fields["text"] = song["text"]
                fields["num"] = song["num"]
                fields["num_verse"] = song["num_verse"]
                fields["chorus"] = song["chorus"]
                fields["followed"] = song["followed"]
                verses.append(fields)

        self.close()
        return songs
    

    @staticmethod
    def get_lyrics(verses)->str:
        choruses = []
        lyrics = ""

        # Get all choruses
        for verse in verses:
            if verse["chorus"] == 1:
                choruses.append("<b>" + verse["text"].replace("\n", "<br>") + "</b>")

        start_by_chorus = True
        for verse in verses:
            if verse["chorus"] != 1:
                if verse["text"] and verse["chorus"] != 2:
                    lyrics += str(verse["num_verse"]) + ". " + verse["text"].replace("\n", "<br>") + "<br><br>"
                if verse["text"] and verse["chorus"] == 2:
                    lyrics += "<b>" + verse["text"].replace("\n", "<br>") + "</b><br><br>"
                if not verse["followed"] and choruses:
                    lyrics += "<br><br>".join(choruses) + "<br><br>"
            elif start_by_chorus:
                lyrics += "<br><br>".join(choruses) + "<br><br>"
            start_by_chorus = False
        
        if not lyrics:
            lyrics = "<br><br>".join(choruses)

        
        return lyrics