from downloader import saveYTVideoAsAudio
from uploader import uploadFileToBucket
from transcriber import transcribe_gcs
from helper import convert_mp3_to_wav, delete_file, frame_rate_channel


def transcribe_video_with_Google(secret: str, bucket:str, video_url: str, language:str):

    # download Youtube video as an audio, mp3 file and save it locally
    title, savePath = saveYTVideoAsAudio(link=video_url, path="temp")
    print("Saved in:", savePath, "\n under title:", title)

    # transform file to .wav formatting for better encoding that is easier to recognize by GCS
    convert_mp3_to_wav("temp/", title, ".mp3", title, ".wav")

    # delete local .mp3 file
    delete_file("temp/", title, ".mp3")

    # get .wav file config
    frame_rate, channels = frame_rate_channel("temp/", title, ".wav")

    # uplaod .wav file to Google Cloud Bucket
    gcs_uri = uploadFileToBucket(
        keyPath=secret,
        bucketName=bucket,
        filePath=savePath+".wav",
        uploadName=title
    )

    print("File uploaded on GCS with uri:", gcs_uri)

    # delete local .wav file
    delete_file("temp/", title, ".wav")

    # Use GCP Speech-to-Text to transcribe audio file
    words_info = transcribe_gcs(key_path=secret, gcs_uri=gcs_uri, language=language, frame_rate=frame_rate, channels=channels)
    print("transcribed successfully!")

    return words_info

