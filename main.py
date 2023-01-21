from Google import Create_Service

###BUILD API###
CLIENT_SECRET_FILE = 'client_secret_file.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']

youtube = Create_Service(CLIENT_SECRET_FILE, 'youtube', 'v3', SCOPES)

###GET INPUT PLAYLIST VIDEOS###
input_playlist = 'PLRfY4Rc-GWzhdCvSPR7aTV0PJjjiSAGMs'

all_videos = []

#Loop in order to get refresh tokens until no more
while True:

    #Get playlist's videos
    request_playlist = youtube.playlistItems().list(
        part=['snippet','contentDetails'],
        playlistId=input_playlist,
        maxResults=1000
    )

    playlist_videos = request_playlist.execute()

    #For every video in that playlist, get its stats
    for video in playlist_videos['items']:
        video_id = video['contentDetails']['videoId']
        request_video_stats = youtube.videos().list(
            part='statistics',
            id = video_id
        )

        video_stats = request_video_stats.execute()

        current_video_id = video_stats['items'][0]['id']
        current_video_views = video_stats['items'][0]['statistics']['viewCount']
        current_video_likes = video_stats['items'][0]['statistics']['likeCount']
        current_video_comments = video_stats['items'][0]['statistics']['commentCount']

        #Build a dictionary out of it and append it to the list of dictionary encompassing all videos
        current_video_stats = {}
        current_video_stats[current_video_id] = {'views':current_video_views, 'likes':current_video_likes, 'comments':current_video_comments}

        all_videos.append(current_video_stats)

    #Get token to access the 5 next video data points
    if 'nextPageToken' in playlist_videos:
        reqPL = youtube.playlistItems().list(
            part=['snippet', 'contentDetails'],
            playlistId=input_playlist,
            pageToken=playlist_videos['nextPageToken'],
            maxResults=1000
        )
    else:
        break

###ORDER VIDEOS BY VIEW COUNT OR LIKES OR COMMENTS###
def orderBy(video_list, filter='views'):
    if filter == 'views':
        sorted_videos = sorted(video_list, key=lambda x: int(list(x.values())[0]['views']), reverse=True)

    elif filter == 'likes':
        sorted_videos = sorted(video_list, key=lambda x: int(list(x.values())[0]['likes']), reverse=True)

    elif filter == 'comments':
        sorted_videos = sorted(video_list, key=lambda x: int(list(x.values())[0]['comments']), reverse=True)

    return sorted_videos

orderedVideos = orderBy(all_videos, filter='views')

###CREATE PLAYLIST###
title = 'testNewPlaylist'
description = 'testByViews'
privacy_status = 'private'

new_playlist = youtube.playlists().insert(
    part='snippet',
    body={
        'snippet':{
            'title': title,
            'description': description,
            privacy_status: privacy_status
        }
    }
).execute()

###ADD VIDEOS IN ORDER INTO THE NEW PLAYLIST###
for video in orderedVideos:
    video_id = list(video.keys())[0]
    youtube.playlistItems().insert(
        part='snippet',
        body={
            'snippet':{
                'playlistId': new_playlist['id'],
                'resourceId':{
                    'kind':'youtube#video',
                    'videoId':video_id
                }
            }
        }
    ).execute()
