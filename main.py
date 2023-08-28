from gcs_client import transcribe_video_with_Google
from youtube_transcript_api import YouTubeTranscriptApi
from transformer import bind_sentences
from helper import insert_data
from confluent_kafka import Consumer, KafkaError

def kafka_consumer():
    # Define the Kafka configuration
    conf = {
        'bootstrap.servers': 'YOUR_BROKER',  # Replace with your broker's address
        'group.id': 'yourgroup',
        'auto.offset.reset': 'earliest',  # start reading from the beginning of the topic
    }

    # Create the consumer instance with the given configuration
    consumer = Consumer(conf)

    # Subscribe to the topic
    consumer.subscribe(['youtube-links'])

    try:
        while True:
            # Poll for a new message. The timeout defines how long it will wait
            message = consumer.poll(timeout=1.0)
            if message is None:
                continue
            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event - not an error.
                    print('Reached the end of partition {} at offset {}.\n'.format(
                        message.partition(), message.offset()))
                else:
                    # Print any other errors:
                    print('Error while consuming message: {}'.format(message.error()))
            else:
                # Proper message received. Process the YouTube link:
                youtube_link = message.value().decode('utf-8')
                process_youtube_link(youtube_link)

    except KeyboardInterrupt:
        pass
    finally:
        # Close the consumer
        consumer.close()

def process_youtube_link(video_url):
    secret_key = "yourGCSKey.json"
    bucket="yourGCSBucket"
    language="en-US"

    # get Google's Speech-to-text transcript of the video
    words_info = transcribe_video_with_Google(secret_key, bucket, video_url, language)

    # get built-in captions of the same video
    caption = YouTubeTranscriptApi.get_transcript(video_url.split("v=")[1], languages=['en'])

    # transform captions and generated text to the same formatting
    sentence_pairs = bind_sentences(words_info, caption)

    # add results to database
    for transcribed, captioned in sentence_pairs:
        # calculate similarity score between sentences
        # result is of the form [(transcribed sentence, caption sentence, similarity score)]
        #score = get_similarity_score(sentence1, sentence2) # method removed for NDA reasons
        score = 1.00
        service = "Google"
        insert_data(transcribed, captioned, score, service, video_url, language)


if __name__ == '__main__':
    kafka_consumer()
