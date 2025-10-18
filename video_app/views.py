from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.utils.encoding import iri_to_uri
import requests

API_URL = "https://video-api-1-0-6zux.onrender.com/api/fetch" 

def home(request):
    return render(request, 'video_app/index.html')



def fetch_video(request):
    video_url = request.GET.get('url')
    if not video_url:
        return render(request, 'video_app/index.html', {'error': 'Please enter a video URL'})

    try:
        response = requests.get(API_URL, params={'url': video_url}, timeout=60)
        data = response.json()

        if 'error' in data:
            return render(request, 'video_app/index.html', {'error': data['error']})

      
        return render(request, 'video_app/index.html', {'video': data})

    except Exception as e:
        return render(request, 'video_app/index.html', {'error': str(e)})

def download_video(request):
    video_url = request.GET.get('url')
    title = request.GET.get('title', 'video.mp4')

    if not video_url:
        return render(request, 'video_app/index.html', {'error': 'No video URL provided'})

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
                      "image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "DNT": "1"
        }

        r = requests.get(video_url, stream=True, headers=headers)

        response = StreamingHttpResponse(
            r.iter_content(chunk_size=1024*1024)
        )
        response["Content-Disposition"] = f'attachment; filename="{iri_to_uri(title)}"'
        response['Content-Type'] = r.headers.get('content-type', 'application/octet-stream')
        response['Content-Length'] = r.headers.get('content-length', None)
        response['Cache-Control'] = 'no-cache'

        return response

    except Exception as e:
        return render(request, 'video_app/index.html', {'error': str(e)})
