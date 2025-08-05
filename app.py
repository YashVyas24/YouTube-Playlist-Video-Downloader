import streamlit as st
from downloader import get_video_streams, download_single_video, download_playlist
from pytube import Playlist

st.set_page_config(page_title="YouTube Downloader", layout="centered")
st.title("🎥 YouTube Playlist & Video Downloader")
st.write("Download videos or audio from **YouTube** with quality control.")

url = st.text_input("🔗 Enter a YouTube video or playlist URL:").strip()

# Green box if URL looks valid
if url.startswith("http") and ("youtube.com" in url or "youtu.be" in url):
    st.markdown("""
    <style>
    input[type="text"] {
        border: 2px solid #28a745 !important;
    }
    </style>
    """, unsafe_allow_html=True)

download_type = st.radio("Download Type:", ["Video", "Audio (MP3)"])
download_mode = st.radio("What would you like to download?", ["Single Video", "Playlist"])

resolution = None

if url:
    try:
        target_url = url if download_mode == "Single Video" else Playlist(url).video_urls[0]
        title, streams = get_video_streams(target_url)
        st.markdown(f"**📌 Title:** {title}")

        if download_type == "Video":
            resolutions = sorted({s.resolution for s in streams if s.resolution}, reverse=True)
            resolution = st.selectbox("Choose resolution:", resolutions)

    except Exception as e:
        st.error(f"⚠️ Could not fetch video info: {e}")

if st.button("🚀 Start Download"):
    if not url:
        st.warning("Please enter a valid URL.")
    else:
        status = st.empty()
        progress = st.progress(0)

        if download_mode == "Single Video":
            result = download_single_video(
                url,
                resolution=resolution if download_type == "Video" else None,
                download_type='audio' if download_type == "Audio (MP3)" else 'video'
            )
        else:
            result = download_playlist(
                url,
                resolution=resolution if download_type == "Video" else None,
                download_type='audio' if download_type == "Audio (MP3)" else 'video',
                update_status=status.write,
                update_progress=progress.progress
            )

        if result.startswith("✅"):
            st.success(result)
        else:
            st.error(result)
