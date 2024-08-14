import openai
import os
from pydub import AudioSegment
import math

def split_audio(input_file, chunk_length_ms=60000, output_folder="temp_audio_chunks"):
    audio = AudioSegment.from_wav(input_file)
    duration_ms = len(audio)
    chunks = math.ceil(duration_ms / chunk_length_ms)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    chunk_files = []
    for i in range(chunks):
        start = i * chunk_length_ms
        end = (i + 1) * chunk_length_ms
        chunk = audio[start:end]
        chunk_file = os.path.join(output_folder, f"chunk_{i}.wav")
        chunk.export(chunk_file, format="wav")
        chunk_files.append(chunk_file)

    return chunk_files

def transcribe_chunk(chunk_file, api_key):
    openai.api_key = api_key
    with open(chunk_file, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

def large_wav_to_text_openai(wav_file_path, txt_file_path, api_key):
    chunk_files = split_audio(wav_file_path)

    full_transcript = ""
    for chunk_file in chunk_files:
        chunk_transcript = transcribe_chunk(chunk_file, api_key)
        full_transcript += chunk_transcript + " "

    with open(txt_file_path, 'w', encoding='utf-8') as file:
        file.write(full_transcript.strip())

    print(f"Transcription complete. Text saved to {txt_file_path}")

    # Clean up temporary files
    for chunk_file in chunk_files:
        os.remove(chunk_file)
    os.rmdir("temp_audio_chunks")

# Example usage
wav_file = "path/to/audio/file.wav"
txt_file = "path/to/your/transcript/file.txt"
api_key = "your_api_key"  # Replace with your actual OpenAI API key

large_wav_to_text_openai(wav_file, txt_file, api_key)