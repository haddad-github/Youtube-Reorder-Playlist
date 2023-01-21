from constants import API_KEY
from googleapiclient.discovery import build

#Initiate API (uses google cloud' project's API key)
youtube = build('youtube', 'v3', developerKey=API_KEY)

#Playlist ID is the part starting with "P" after one of the equal signs
#from https://www.youtube.com/watch?v=8ejF8Qv6VZk&list=PLRfY4Rc-GWzhdCvSPR7aTV0PJjjiSAGMs
playlist_id = 'PLRfY4Rc-GWzhdCvSPR7aTV0PJjjiSAGMs'

#Get playlist items request
request_playlist = youtube.playlistItems().list(
    part=['snippet', 'contentDetails'],
    playlistId=playlist_id,
)

#Execute the request
playlist_videos = request_playlist.execute()

#Print the videos inside the playlist, as requested
print(playlist_videos)