from processing import Flask, os, request, render_template,requests
from extract_audio import extract_audio_from_video
from transcribe_audio import transcribe_audio

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Step 1: Extract audio from the uploaded video file
        audio_file = extract_audio_from_video(file_path)
        if audio_file is None:
            return "Audio extraction failed", 500

        # Step 2: Transcribe the extracted audio
        transcription = transcribe_audio(audio_file)
        if transcription is None:
            return "Transcription failed", 500

        return f"File uploaded and transcribed successfully! Transcription: {transcription}"

@app.route('/upload-url', methods=['POST'])
def upload_url():
    if 'url' not in request.form:
        return "No URL provided", 400

    video_url = request.form['url']
    if not video_url:
        return "Invalid URL", 400

    try:
        # Step 1: Download the video file from the URL
        video_response = requests.get(video_url)
        if video_response.status_code != 200:
            return "Failed to download video", 400

        # Step 2: Save the video to the uploads folder
        video_filename = video_url.split("/")[-1]  # Get the filename from the URL
        video_file_path = os.path.join(UPLOAD_FOLDER, video_filename)
        with open(video_file_path, 'wb') as video_file:
            video_file.write(video_response.content)

        # Step 3: Extract audio from the downloaded video file
        audio_file = extract_audio_from_video(video_file_path)
        if audio_file is None:
            return "Audio extraction failed", 500

        # Step 4: Transcribe the extracted audio
        transcription = transcribe_audio(audio_file)
        if transcription is None:
            return "Transcription failed", 500

        return f"Video URL uploaded and transcribed successfully! Transcription: {transcription}"

    except Exception as e:
        print(f"An error occurred while processing the video URL: {e}")
        return "An error occurred while processing the video URL.", 500

if __name__ == '__main__':
    app.run(debug=True)