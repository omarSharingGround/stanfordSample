from google.cloud import speech

def transcribe_gcs(key_path:str, gcs_uri: str, language: str, frame_rate: int, channels: int):
    path_to_private_key = key_path

    client = speech.SpeechClient.from_service_account_file(path_to_private_key)

    speaker_diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=2,
        max_speaker_count=2,
    )
    
    audio = speech.RecognitionAudio(uri=gcs_uri)
    recognition_config  = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=frame_rate,
        language_code=language,
        audio_channel_count = channels,
        diarization_config=speaker_diarization_config,
    )

    
    # Set the remote path for the audio file
    audio = speech.RecognitionAudio(
        uri=gcs_uri,
    )

    # Use non-blocking call for getting file transcription
    response = client.long_running_recognize(
        config=recognition_config, audio=audio
    ).result(timeout=3000)

    # The transcript within each result is separate and sequential per result.
    # However, the words list within an alternative includes all the words
    # from all the results thus far. Thus, to get all the words with speaker
    # tags, you only have to take the words list from the last result
    result = response.results[-1]
    words_info = result.alternatives[0].words

    # Print the output
    for i in range(len(words_info)):
        word_info = words_info[i]
        print(f"word: '{word_info.word}', speaker_tag: {word_info.speaker_tag}, time: {words_info.start_time.seconds}")

    return words_info



