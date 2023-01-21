from Google import Create_Service

CLIENT_SECRET_FILE = 'client_secret_file.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']

youtube = Create_Service(CLIENT_SECRET_FILE, 'youtube', 'v3', SCOPES)

youtube.playlists().insert(
    part='snippet',
    body={
        'snippet':{
            'title':'testPlaylist',
            'description':'testDescription',
            'privacyStatus':'public'
        }
    }
).execute()
