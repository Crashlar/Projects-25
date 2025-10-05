from flask import Flask, render_template, request, redirect, url_for, flash
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from transformers import pipeline
import re


app = Flask(__name__)
app.secret_key = 'ytsummarizer'

#Loading models
print("Now Loading Models...")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
print("Model Completely Loaded")

def get_video_id(url):
    pattern = r"(?:v=|youtu\.be/)([a-zA-z)-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        url = request.form.get('yt_url')
        video_id = get_video_id(url)

        if not video_id:
            flash("Invalid YouTube URL")
            return redirect(url_for('index'))
        
        try:
            transcript = YouTubeTranscriptApi().fetch(video_id, languages=['en']).to_raw_data()
            full_text = " ".join([entry['text'] for entry in transcript])

            # Check if too long
            if len(full_text) > 1000:
                full_text = full_text[:1000]

            summary = summarizer(full_text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']

            return render_template('result.html', summary=summary, full=full_text)
        except TranscriptsDisabled:
            flash("transcript disabled for this video")
            return redirect(url_for('index.html'))
    
    return render_template('index.html')





if __name__ == "__main__":
    app.run()