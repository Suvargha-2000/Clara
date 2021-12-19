import json 

with open("links/songs.json") as file2:
    songs_data = json.load(file2)
    print(songs_data[1]["name"])