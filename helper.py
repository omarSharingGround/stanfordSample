import subprocess
import os
import wave
import sqlite3

# runs ffmpeg command to convert mp3 file to wav formatting
def convert_mp3_to_wav(path, input_file, input_format, output_file, output_format):
    command = ['ffmpeg', '-i', path+input_file+input_format, path+output_file+output_format]
    subprocess.run(command)

# deletes local file
def delete_file(path, input_file, input_format):
    # Specify the file path
    file_path = path + input_file + input_format

    # Check if the file exists and then delete it
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted.")
    else:
        print(f"{file_path} does not exist.")

# returns the frame rate and number of channels for a given video
def frame_rate_channel(path, input_file, input_format):

    audio_file_name = path + input_file + input_format
    
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate,channels

def insert_data(sentence1, sentence2, similarity_score, service, url, language):
    # Connect to a SQLite database
    conn = sqlite3.connect('yourDB.db')
    cursor = conn.cursor()

    # Insert a new row of data
    cursor.execute('''
    INSERT INTO SentenceSimilarity (transcript, caption, similarity_score, service, url, language) 
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (sentence1, sentence2, similarity_score, service, url, language))

    # Commit the changes
    conn.commit()