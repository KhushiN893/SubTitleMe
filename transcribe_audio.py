from processing import librosa, pipeline

def transcribe_audio(audio_file):
    try:
        # Load the audio file (librosa automatically converts the sampling rate to 16kHz)
        audio, sampling_rate = librosa.load(audio_file, sr=16000)
        
        # Initialize the ASR pipeline using Hugging Face's 'distil-whisper' model
        asr = pipeline("automatic-speech-recognition", model="distil-whisper/distil-small.en")

        # Perform the transcription on the audio data and directly return the chunks
        result = asr(audio, chunk_length_s=30, batch_size=4, return_timestamps=False)

        return result["chunks"]  # Return the chunks directly

    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return None
