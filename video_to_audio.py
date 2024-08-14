from moviepy.editor import VideoFileClip
import os

def extract_audio_from_video(video_path, audio_path):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path, codec='mp3')  
        print(f"Audio extracted successfully to {audio_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    video_path = "path/to/your/video.mp4"
    audio_path = "path/to/your/audio/file.wav"  
    extract_audio_from_video(video_path, audio_path)