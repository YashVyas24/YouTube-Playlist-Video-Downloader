# 🎬 YouTube Playlist & Video Downloader

A simple Streamlit web app to download **YouTube videos** or **playlists** as **MP4** or **MP3**, with quality selection and progress tracking.

---

## 🔧 Features

- Download single videos or entire playlists  
- Choose between **Video (MP4)** and **Audio (MP3)**  
- Quality selection for video  
- Progress bar for downloads  
- Skips unavailable/private videos  

---

## 📦 Requirements

- Python 3.7+
- [FFmpeg](https://ffmpeg.org/download.html) (add to PATH)

Install dependencies:

```bash
pip install streamlit pytube pydub

## How to Run
bash
Copy
Edit
streamlit run app.py
App will open at: http://localhost:8501

🔗 Sample URLs
Video: https://www.youtube.com/watch?v=dQw4w9WgXcQ

Playlist: https://www.youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj

📁 Structure
bash
Copy
Edit
📦 project/
├── app.py          # Streamlit UI
├── downloader.py   # Download logic

📝 License
MIT License
yaml
Copy
Edit

## Let me know if you also want:
- A project logo badge  
- Deploy to Streamlit Cloud instructions  
- `.exe` or `.bat` version for non-tech users
