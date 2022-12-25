import time
import pandas as pd
import numpy as np
import pytube
import youtube_dl
from pytube import *
import os

import boto3

AWS_ACCESS_KEY_ID = 'T7HMYxxxxxxxx' # insert here your real access key code
AWS_SECRET_ACCESS_KEY = 'gavJNExxxxxxxx'
REGION = 'eu-central-1'

transcribe = boto3.client('transcribe',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,  # insert your access key ID here,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          # insert your secret access key here
                          region_name=REGION)  #


def check_job_name(job_name):
    job_verification = True

    # all the transcriptions
    existed_jobs = transcribe.list_transcription_jobs()

    for job in existed_jobs['TranscriptionJobSummaries']:
        if job_name == job['TranscriptionJobName']:
            job_verification = False
            break

    if not job_verification:
        # command = input(job_name + " has existed. \nDo you want to override the existed job (Y/N): ")
        # if command.lower() == "y" or command.lower() == "yes":
        transcribe.delete_transcription_job(TranscriptionJobName=job_name)
    # elif command.lower() == "n" or command.lower() == "no":
    #     job_name = input("Insert new job name? ")
    #     check_job_name(job_name)
    # else:
    #     print("Input can only be (Y/N)")
    #     command = input(job_name + " has existed. \nDo you want to override the existed job (Y/N): ")
    return job_name


def amazon_transcribe(audio_file_name):
    job_uri = "s3://finvid/" + audio_file_name  # your S3 access link
    # Usually, I put like this to automate the process with the file name
    # "s3://bucket_name" + audio_file_name

    # Usually, file names have spaces and have the file extension like .mp3
    # we take only a file name and delete all the space to name the job
    job_name = (audio_file_name.split('.')[0]).replace(" ", "")

    # file format
    file_format = audio_file_name.split('.')[1]

    # check if name is taken or not
    job_name = check_job_name(job_name)
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat=file_format,
        LanguageCode='en-US')

    while True:
        result = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if result['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            print(result['TranscriptionJob']['TranscriptionJobStatus'])
            break
        time.sleep(15)

    if result['TranscriptionJob']['TranscriptionJobStatus'] == "COMPLETED":
        data = pd.read_json(result['TranscriptionJob']['Transcript']['TranscriptFileUri'])

    return data['results'][1][0]['transcript'], data


def find_word(data, word_to_find):  # todo send lower letters word
    words = [r['alternatives'][0]['content'] for r in [y for x, y in data.results.items()][0]]
    words_numpy_list = np.array(words)
    words_numpy_list = np.char.lower(words_numpy_list)
    idx = np.where(words_numpy_list == word_to_find)  # list of indices of the elements
    start_time_list = [r.get("start_time") for r in [y for x, y in data.results.items()][0]]
    the_times_of_the_word = [start_time_list[x] for x in idx[0]]
    return the_times_of_the_word


def download_audio_file():
    convert_url = input("insert url  :")
    video_info = youtube_dl.YoutubeDL().extract_info(url=convert_url, download=False)
    video_name = video_info['title']
    yt = YouTube(convert_url)
    stream = max(yt.streams.filter(type="audio", file_extension="mp4"), key=lambda x: x.abr)
    stream.download(os.getcwd() + "\\audio")
    uploade_to_s3(video_name)
    return video_name + '.mp4'


def uploade_to_s3(file_name):  # upload to s3 amazon basket
    # define AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and bucket_name
    # bucket_name: name of s3 storage folder
    print("upload the audio file to the s3")
    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=REGION)
    s3.upload_file(os.getcwd() + "\\audio" + "\\" + file_name + '.mp4', "finvid",
                   file_name + '.mp4')


#

def main():
    start = time.time()
    file_name = download_audio_file()
    data, data_handle = amazon_transcribe(file_name)
    desired_list = find_word(data_handle, "tomorrow".lower())
    print(data)
    print(desired_list)
    end = time.time()
    print(end - start)


# print(data)


if __name__ == "__main__":
    main()
