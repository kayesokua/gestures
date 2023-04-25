import os
import time
import pytube
from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials = service_account.Credentials.from_service_account_file('./keyfile.json')
youtube = build('youtube', 'v3', credentials=credentials)

def measure_elapsed_time(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.3f} seconds")
        return result
    return wrapper

def create_output_dir_if_not_exists(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

@measure_elapsed_time
def extract_video_from_youtube(query, max_count):
    output_dir = f"../../data/external/"
    create_output_dir_if_not_exists(output_dir)

    query_1 = query +'+solo'
    query_2 = query+'+solo+choreography'
    query_3 = query+'+dance+cover'

    query_combinations = [query_1, query_2, query_3]
    download_count = 0

    while download_count < max_count:
        for query_combi in query_combinations:
            print(f"Searching for {query_combi}...")

            search_response = youtube.search().list(
                q=query_combi,
                type='video',
                part='id,snippet',
                order='viewCount',
                relevanceLanguage='en',
                safeSearch='strict',
                videoDuration='short',
                regionCode='US'
            ).execute()

            for item in search_response['items']:
                video_id = item['id']['videoId']
                url = f'https://www.youtube.com/watch?v={video_id}'
                video = pytube.YouTube(url)
                if video:
                    video_streams = video.streams.filter(file_extension='mp4', progressive=True)
                    stream = video_streams.get_highest_resolution()
                    if (stream.width == 640 and stream.height == 360
                            and video.length <= 120
                            and video.views >= 100):
                        print(video.title)
                        print(stream.resolution)
                        print(video.length)
                        print(video.rating)

                        output_filename = f"{query}_{download_count:03d}.mp4"
                        stream.download(output_path=output_dir, filename=output_filename)
                        download_count += 1
                        print(f"{download_count}/{max_count} Downloaded")

                        if download_count >= max_count:
                            break