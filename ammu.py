import os
import whisper
import openai
import subprocess

openai.api_key = os.getenv("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")  

def extract_audio(video_path, audio_path="audio.wav"):
    """Extracts audio from a video file using FFmpeg."""
    command = f'ffmpeg -i "{video_path}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{audio_path}"'
    subprocess.run(command, shell=True)

def transcribe_audio(audio_path):
    """Converts audio to text using Whisper AI."""
    model = whisper.load_model("large")
    result = model.transcribe(audio_path)
    return result["text"]

def refine_text_with_gpt4(text):
    """Enhances transcription using GPT-4 AI."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": text}]
    )
    return response["choices"][0]["message"]["content"]

def convert_media_to_text(file_path):
    """Detects if input is video or audio, then transcribes it."""
    audio_path = "audio.wav"
    
    if file_path.lower().endswith((".mp4", ".mkv", ".avi", ".mov")):
        extract_audio(file_path, audio_path)
        file_path = audio_path

    if file_path.lower().endswith((".wav", ".mp3", ".aac", ".flac")):
        raw_text = transcribe_audio(file_path)
        refined_text = refine_text_with_gpt4(raw_text)
        
        with open("final_transcript.txt", "w") as f:
            f.write(refined_text)
        
        print("✅ Transcription saved: 'final_transcript.txt'")
        print("📝 Preview:\n", refined_text[:500], "...")


convert_media_to_text("video,mp4")