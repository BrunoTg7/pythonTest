import streamlit as st
import yt_dlp

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'merge_output_format': 'mp4',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
       

def main():
    st.title("YouTube Video Downloader")

    urls = st.text_area("Cole aqui as URLs dos vídeos, separadas por vírgula:")

    if st.button("Download"):
        url_list = [url.strip() for url in urls.split(',')]
        if url_list:
            for url in url_list:
                if not url.startswith("https://"):
                    url = "https://" + url
                try:
                    with st.spinner(f"Baixando o vídeo de {url}..."):
                        download_video(url)
                        st.success(f"Download concluído para: {url}")
                except Exception as e:
                    st.error(f"Erro ao baixar {url}: {e}")
        else:
            st.warning("Por favor, insira pelo menos uma URL válida.")

if __name__ == "__main__":
    main()



#python -m venv myenv

#myenv\Scripts\activate  streamlit run speedtest.py streamlit run youtube.py

#pip install streamlit speedtest-cli pandas matplotlib pytube
