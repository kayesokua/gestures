from google.oauth2 import service_account
from googleapiclient.discovery import build
import pytube
from .helpers import *

credentials = service_account.Credentials.from_service_account_file('src/data/keyfile.json')
youtube = build('youtube', 'v3', credentials=credentials)

@measure_elapsed_time
def extract_video_from_youtube(query, count, output_dir):
    create_output_dir_if_not_exists(output_dir)
    # Make the API request to search for videos with the tag
    search_response = youtube.search().list(
        q=query,
        type='video',
        part='id',
        maxResults=count,
        order='viewCount',
        relevanceLanguage='en',
        safeSearch='strict',
        videoDuration='short',
        regionCode='US'
    ).execute()

    # Extract the video IDs from the search results
    video_ids = [item['id']['videoId'] for item in search_response['items']]

    # Get the URLs for the videos
    video_urls = ['https://www.youtube.com/watch?v=' + video_id for video_id in video_ids]

    i = 0
    # Download the videos in low resolution
    if count >= i:
        for url in video_urls:
            video = pytube.YouTube(url)
            video_stream = video.streams.get_lowest_resolution()
            # Set the output filename to be "<query>_<video_title>.mp4"
            query_title = query.replace('+', '_')
            date_title = datetime_str()
            output_filename = f"{query_title}_{date_title}_{i}.mp4"
            video_stream.download(output_path=output_dir, filename=output_filename)
            print(f"{i}/{count} Downloaded")
            i += 1
    print(f"Downloaded {i} videos")