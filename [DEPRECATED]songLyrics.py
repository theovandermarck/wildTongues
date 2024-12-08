import requests

def get_song_lyrics(track_name, artist_name):
    url = f"https://lyrist.vercel.app/api/{track_name}/{artist_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Example usage
track_name = "cleopatra"
artist_name = "the lumineers"
lyrics = get_song_lyrics(track_name, artist_name)

if lyrics:
    while True:
        if (lyrics['lyrics'].find('[') !=-1 and lyrics['lyrics'].find(']')!=-1):
            lyrics['lyrics'] = lyrics['lyrics'][:lyrics['lyrics'].find('[')] + lyrics['lyrics'][lyrics['lyrics'].find(']')+1:]
        else:
            break
    print(lyrics['lyrics'])
else:
    print("Lyrics not found.")