from pytube import YouTube, Playlist
from pydub import AudioSegment
import os
from pathlib import Path
from urllib.error import HTTPError
from pytube.exceptions import VideoUnavailable, RegexMatchError

DOWNLOADS_FOLDER = str(Path.home() / "Downloads")

def is_video_available(url):
    try:
        yt = YouTube(url)
        yt.check_availability()
        return True
    except Exception:
        return False

def get_video_streams(url):
    try:
        yt = YouTube(url)
        yt.check_availability()
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        return yt.title, streams
    except (VideoUnavailable, HTTPError, RegexMatchError) as e:
        raise Exception("❌ Invalid or unavailable video.") from e
    except Exception as e:
        raise Exception(f"❌ Unexpected error: {str(e)}") from e

def download_single_video(url, resolution, download_type='video'):
    try:
        yt = YouTube(url)
        if download_type == 'audio':
            stream = yt.streams.filter(only_audio=True).first()
            audio_path = stream.download(output_path=DOWNLOADS_FOLDER)
            mp3_path = os.path.splitext(audio_path)[0] + ".mp3"
            AudioSegment.from_file(audio_path).export(mp3_path, format="mp3")
            os.remove(audio_path)
        else:
            stream = yt.streams.filter(progressive=True, res=resolution, file_extension='mp4').first()
            if not stream:
                return "❌ Selected resolution not available."
            stream.download(output_path=DOWNLOADS_FOLDER)
        return f"✅ Downloaded: {yt.title}"
    except Exception as e:
        return f"❌ Failed: {str(e)}"

def download_playlist(url, resolution, download_type='video', update_status=None, update_progress=None):
    try:
        playlist = Playlist(url)
        video_urls = [v for v in playlist.video_urls if is_video_available(v)]
        total = len(video_urls)

        for i, video_url in enumerate(video_urls, start=1):
            try:
                yt = YouTube(video_url)
                if update_status:
                    update_status(f"Downloading {i}/{total}: {yt.title}")

                if download_type == 'audio':
                    stream = yt.streams.filter(only_audio=True).first()
                    audio_path = stream.download(output_path=DOWNLOADS_FOLDER)
                    mp3_path = os.path.splitext(audio_path)[0] + ".mp3"
                    AudioSegment.from_file(audio_path).export(mp3_path, format="mp3")
                    os.remove(audio_path)
                else:
                    stream = yt.streams.filter(progressive=True, res=resolution, file_extension='mp4').first()
                    if stream:
                        stream.download(output_path=DOWNLOADS_FOLDER)

                if update_progress:
                    update_progress(i / total)

            except Exception as ve:
                if update_status:
                    update_status(f"⚠️ Skipped one video: {str(ve)}")

        return f"✅ Playlist downloaded to: {DOWNLOADS_FOLDER}"
    except Exception as e:
        return f"❌ Error: {str(e)}"
