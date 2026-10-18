import os
import requests
import urllib.parse
from PIL import Image, ImageDraw


def search_pexels_video(keyword: str, api_key: str, min_duration: int = 3) -> str:
    """
    Searches for a vertical video on Pexels API matching the keyword.
    Returns the video download URL or None.
    """
    url = f"https://api.pexels.com/videos/search?query={urllib.parse.quote(keyword)}&per_page=10&orientation=portrait"
    headers = {"Authorization": api_key}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            videos = data.get("videos", [])
            for video in videos:
                if video.get("duration", 0) >= min_duration:
                    video_files = video.get("video_files", [])
                    # Find HD vertical video file
                    for vf in video_files:
                        if vf.get("link"):
                            return vf["link"]
                    if video_files:
                        return video_files[0].get("link")
    except Exception as e:
        print(f"[Aviso] Erro na busca Pexels para '{keyword}': {e}")
    return None


def create_fallback_vertical_video(output_path: str, duration: float = 5.0, color_rgb=(20, 24, 40), width: int = 1080, height: int = 1920) -> str:
    """
    Generates a vertical video file (MP4) using MoviePy / ImageClip fallback.
    """
    from moviepy import ColorClip

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    clip = ColorClip(size=(width, height), color=color_rgb, duration=duration)
    clip.write_videofile(output_path, fps=30, codec="libx264", logger=None)
    return output_path


def fetch_background_video(keyword: str, output_path: str, target_duration: float = 5.0) -> str:
    """
    Fetches B-roll video from Pexels API or generates fallback vertical background if unavailable.
    """
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    api_key = os.getenv("PEXELS_API_KEY")

    if api_key:
        print(f"[Video] Buscando vídeo B-roll no Pexels para '{keyword}'...")
        video_url = search_pexels_video(keyword, api_key, min_duration=int(target_duration))
        if video_url:
            try:
                resp = requests.get(video_url, stream=True, timeout=15)
                if resp.status_code == 200:
                    with open(output_path, "wb") as f:
                        for chunk in resp.iter_content(chunk_size=1024*1024):
                            f.write(chunk)
                    print(f"[Video] Vídeo Pexels baixado: {output_path}")
                    return output_path
            except Exception as e:
                print(f"[Aviso] Falha ao baixar vídeo do Pexels: {e}")

    print(f"[Video] Usando vídeo de fundo vertical padrão para '{keyword}'...")
    colors = [(25, 30, 50), (40, 20, 60), (15, 45, 45), (60, 30, 30)]
    idx = abs(hash(keyword)) % len(colors)
    return create_fallback_vertical_video(output_path, duration=target_duration, color_rgb=colors[idx])


if __name__ == "__main__":
    out_file = "test_bg.mp4"
    fetch_background_video("space background", out_file, target_duration=3.0)
    if os.path.exists(out_file):
        print(f"Vídeo de fundo criado com sucesso: {os.path.getsize(out_file)} bytes")
        os.remove(out_file)
