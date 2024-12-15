# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from utils.url_extractor import extract_video_urls, extract_audio_urls, extract_thumbnail, get_video_details

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract_urls', methods=['POST'])
def extract_urls():
    url = request.json.get('url')
    extraction_type = request.json.get('type', 'video')
    
    try:
        if extraction_type == 'video':
            urls = extract_video_urls(url)
        elif extraction_type == 'audio':
            urls = extract_audio_urls(url)
        elif extraction_type == 'thumbnail':
            urls = [{'url': extract_thumbnail(url)}]
        elif extraction_type == 'details':
            urls = [get_video_details(url)]
        else:
            return jsonify({
                'success': False, 
                'error': 'Invalid extraction type'
            }), 400
        
        return jsonify({
            'success': True, 
            'urls': urls
        })
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
