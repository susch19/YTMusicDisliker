import sys
import ytmusicapi
import time


def dislike_artist_songs(artist_names):
    """
    Searches for artists on YouTube Music using ytmusicapi to dislike all of these songs.
    
    :param artist_names: List of artist names to search and dislike
    """
    yt_music = ytmusicapi.YTMusic("browser.json")
    
    for artist_name in artist_names:
        try:
            artist_channel_id = ""
            if artist_name.startswith("id:"):
                artist_channel_id = artist_name[3:]
            else:
                search_results = yt_music.search(query=artist_name, filter='artists')
                
                artist = False
                for art in search_results:
                    if art['artist'] != artist_name:
                        print(f"The artist name '{artist_name}' did not match '{art['artist']}'")
                        continue
                    artist = art
                    break
                if artist == False:
                    continue
                print(f"\r\nFound '{artist_name}' for the artist: '{artist['artist']}'\r\n")
                artist_channel_id = artist.get('browseId')
            artist_info = yt_music.get_artist(artist_channel_id)
            
            songs_section = artist_info.get('songs')
            songs_browse_id = songs_section.get('browseId')

            if songs_browse_id != None:
                yt_music.rate_playlist(playlistId=songs_browse_id, rating=ytmusicapi.LikeStatus.DISLIKE)
                dislike_songs(yt_music, yt_music.get_playlist(playlistId= songs_browse_id, limit= None))
            else:
                dislike_songs(yt_music, {'tracks': songs_section.get('results')})
  
                for s in artist_info.get('singles').get('results'):
                    album = yt_music.get_album(s.get('browseId'))
                    yt_music.rate_playlist(playlistId=s.get('browseId'), rating=ytmusicapi.LikeStatus.DISLIKE)
                    dislike_songs(yt_music, album)
            
        except Exception as e:
            print(f"Error searching for artist {artist_name}: {e}")
    
def dislike_songs(yt_music: ytmusicapi, songs):

    for s in songs.get('tracks'):
        if s['likeStatus'] != 'DISLIKE':
            res = yt_music.rate_song(videoId=s['videoId'], rating=ytmusicapi.LikeStatus.DISLIKE)
            print(f"{s['title']} was disliked")
            time.sleep(2)
        else:
            print(f"{s['title']} already disliked")
    
def main():
    if len(sys.argv) < 2:
        print("Please provide artist names as comma-separated arguments.")
        print("Alternativly provide the channel id instead of the name. For this 'id:' has to be prefixed, so that it can be detected as an id.")
        print("Names and ids can be mixed.")
        print("Examples:")
        print("python script.py 'id:UCa7IczYhKhSnhHNZ0uI93ng,id:UCrtlfQiKPeN1EboJuCESD6g'")
        print("python script.py 'The Beatles, Pink Floyd')
        print("python script.py 'The Beatles,id:UCrtlfQiKPeN1EboJuCESD6g')
        sys.exit(1)
    print(
"""
Copy authentication headers from Firefox
    To run authenticated requests, set it up by first copying your request headers from an authenticated POST request in your browser. To do so, follow these steps:
    
    Open a new tab
    Open the developer tools (Ctrl-Shift-I) and select the “Network” tab
    Go to https://music.youtube.com and ensure you are logged in

    Find an authenticated POST request. The simplest way is to filter by "/browse" using the search bar of the developer tools. If you don’t see the request, try scrolling down a bit or clicking on the library button in the top bar.
    Verify that the request looks like this: Status 200, Method POST, Domain music.youtube.com, File "browse?..."
    Copy the request headers (right click > copy > copy request headers)
"""
    )
    ytmusicapi.setup(filepath="browser.json")
    artist_input = sys.argv[1]
    
    artist_names = [name.strip().strip("'\"") for name in artist_input.split(',')]
    
    dislike_artist_songs(artist_names)
    
if __name__ == "__main__":
    main()
