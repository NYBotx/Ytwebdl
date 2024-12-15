from flask import Flask, request, jsonify, render_template_string
from pytube import YouTube

app = Flask(__name__)

# HTML with embedded CSS and JS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Downloader</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(to bottom, #4e54c8, #8f94fb);
            color: white;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }

        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }

        p {
            font-size: 1rem;
        }

        .input-section {
            display: flex;
            gap: 10px;
            margin: 20px 0;
        }

        .input-section input {
            padding: 10px;
            border-radius: 8px;
            border: none;
            font-size: 1rem;
            width: 300px;
        }

        .input-section button {
            background-color: #34d399;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .input-section button:hover {
            background-color: #059669;
        }

        .video-details {
            width: 90%;
            max-width: 500px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            margin-top: 20px;
            display: none;
        }

        .video-details img {
            width: 100%;
            border-radius: 8px;
        }

        .download-options button {
            margin: 5px;
            padding: 8px 12px;
            border-radius: 8px;
            background-color: #34d399;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <header>
        <h1>🎥 YouTube Downloader</h1>
        <p>Download recorded and live videos directly!</p>
    </header>

    <main>
        <div class="input-section">
            <input type="text" id="videoUrl" placeholder="Paste YouTube video link here...">
            <button id="fetchBtn">Fetch Video</button>
        </div>

        <div id="videoDetails" class="video-details">
            <img id="videoThumbnail" src="" alt="Thumbnail">
            <h2 id="videoTitle">Video Title</h2>
            <div class="download-options" id="downloadOptions"></div>
        </div>
    </main>

    <script>
        document.getElementById('fetchBtn').addEventListener('click', async () => {
            const videoUrl = document.getElementById('videoUrl').value.trim();
            if (!videoUrl) {
                alert('Please enter a valid YouTube video URL!');
                return;
            }

            try {
                const response = await fetch('/fetch', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: videoUrl }),
                });

                if (!response.ok) throw new Error('Failed to fetch video details.');

                const data = await response.json();
                document.getElementById('videoThumbnail').src = data.thumbnail;
                document.getElementById('videoTitle').textContent = data.title;

                const downloadOptions = data.streams.map(stream => `
                    <button onclick="window.open('${stream.url}', '_blank')">${stream.type} (${stream.resolution || stream.abr})</button>
                `).join('');
                document.getElementById('downloadOptions').innerHTML = downloadOptions;

                document.getElementById('videoDetails').style.display = 'block';
            } catch (error) {
                console.error(error);
                alert('An error occurred while fetching video details.');
            }
        });
    </script>
</body>
</html>
"""

# Route for the homepage
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

# Route for fetching video details
@app.route('/fetch', methods=['POST'])
def fetch_video():
    data = request.json
    video_url = data.get('url')

    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        yt = YouTube(video_url)
        streams = [
            {
                'type': 'Video+Audio' if stream.includes_audio_track else 'Video',
                'resolution': stream.resolution,
                'abr': stream.abr,
                'url': stream.url,
            }
            for stream in yt.streams.filter(progressive=True)  # Progressive streams have both video & audio
        ]

        response = {
            'title': yt.title,
            'thumbnail': yt.thumbnail_url,
            'streams': streams,
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
