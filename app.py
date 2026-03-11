import streamlit as st
from pytubefix import YouTube
import moviepy as mp
import os

st.set_page_config(page_title="yungtub  Downloader", page_icon="🚀")

st.title("🚀 Multi-Downloader (MP4 & MP3)")
st.write("Tempel link Yungtube.")

url = st.text_input("Link YouTube:", placeholder="https://www.youtube.com/...")

if url:
    try:
        yt = YouTube(url)
        st.image(yt.thumbnail_url, width=300)
        st.subheader(yt.title)
        
        # Membuat dua kolom untuk tombol
        col1, col2 = st.columns(2)

        # PILIHAN 1: VIDEO (MP4)
        with col1:
            if st.button("🎬 Download Video (MP4)"):
                with st.spinner("Mengunduh video..."):
                    video = yt.streams.get_highest_resolution()
                    file_path = video.download()
                    with open(file_path, "rb") as f:
                        st.download_button("Simpan MP4", f, file_name=os.path.basename(file_path))
                    os.remove(file_path) # Bersihkan file setelah dikirim ke browser

        # PILIHAN 2: AUDIO (MP3)
        with col2:
            if st.button("🎵 Download Audio (MP3)"):
                with st.spinner("Mengonversi ke MP3..."):
                    audio = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
                    temp_audio = audio.download()
                    
                    # Proses Konversi
                    base, ext = os.path.splitext(temp_audio)
                    mp3_file = base + ".mp3"
                    clip = mp.AudioFileClip(temp_audio)
                    clip.write_audiofile(mp3_file, bitrate="320k", logger=None)
                    clip.close()
                    
                    with open(mp3_file, "rb") as f:
                        st.download_button("Simpan MP3", f, file_name=os.path.basename(mp3_file))
                    
                    # Hapus file sampah
                    os.remove(temp_audio)
                    os.remove(mp3_file)

    except Exception as e:
        st.error(f"Error: {e}")
