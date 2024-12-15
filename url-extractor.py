# utils/url_extractor.py
import yt_dlp
import re

def extract_video_urls(url):
    """
    Extract direct video streaming URLs from YouTube video link
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'no_color': True,
        'ignoreerrors': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            
            video_urls = []
            for format_info in info_dict.get('formats', []):
                if format_info.get('url') and is_valid_video_url(format_info['url']):
                    video_details = {
                        'url': format_info['url'],
                        'resolution': f"{format_info.get('height', 'Unknown')}p",
                        'ext': format_info.get('ext', 'Unknown'),
                        'filesize': format_info.get('filesize', 'Unknown'),
                        'format_note': format_info.get('format_note', 'Unknown'),
                        'fps': format_info.get('fps', 'Unknown'),
                        'vcodec': format_info.get('vcodec', 'Unknown')
                    }
                    video_urls.append(video_details)
            
            return video_urls
    
    except Exception as e:
        raise ValueError(f"Failed to extract video URLs: {str(e)}")

def extract_audio_urls(url):
    """
    Extract direct audio streaming URLs from YouTube video link
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'no_color': True,
        'ignoreerrors': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            
            audio_urls = []
            for format_info in info_dict.get('formats', []):
                if format_info.get('url') and is_valid_audio_url(format_info['url']):
                    audio_details = {
                        'url': format_info['url'],
                        'ext': format_info.get('ext', 'Unknown'),
                        'abr': format_info.get('abr', 'Unknown'),
                        'acodec': format_info.get('acodec', 'Unknown'),
                        'filesize': format_info.get('filesize', 'Unknown')
                    }
                    audio_urls.append(audio_details)
            
            return audio_urls
    
    except Exception as e:
        raise ValueError(f"Failed to extract audio URLs: {str(e)}")

def extract_thumbnail(url):
    """
    Extract thumbnail URL from YouTube video
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return info_dict.get('thumbnail', '')
    
    except Exception as e:
        raise ValueError(f"Failed to extract thumbnail: {str(e)}")

def get_video_details(url):
    """
    Extract comprehensive video details
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            
            return {
                'title': info_dict.get('title', 'Unknown'),
                'description': info_dict.get('description', 'No description'),
                'view_count': info_dict.get('view_count', 0),
                'like_count': info_dict.get('like_count', 0),
                'upload_date': info_dict.get('upload_date', 'Unknown'),
                'duration': info_dict.get('duration', 0),
                'channel': info_dict.get('uploader', 'Unknown'),
                'tags': info_dict.get('tags', [])
            }
    
    except Exception as e:
        raise ValueError(f"Failed to extract video details: {str(e)}")

def is_valid_video_url(url):
    """
    Validate video streaming URL
    """
    valid_patterns = [
        r'googlevideo\.com/videoplayback',
        r'googlevideo\.com/.*\.(mp4|webm)',
        r'googlevideo\.com/.*itag=\d+'
    ]
    
    return any(re.search(pattern, url) for pattern in valid_patterns)

def is_valid_audio_url(url):
    """
    Validate audio streaming URL
    """
    valid_patterns = [
        r'googlevideo\.com/videoplayback',
        r'googlevideo\.com/.*\.(m4a|webm|mp3)',
        r'googlevideo\.com/.*acodec='
    ]
    
    return any(re.search(pattern, url) for pattern in valid_patterns)
