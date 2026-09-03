from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app) # Android app se API calls block na ho isliye CORS enabled hai

# Health Check Route
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "message": "Movie Streaming API Active Hai!"
    })

# Main Stream Fetcher Route
@app.route('/get-stream', methods=['GET'])
def get_stream():
    tmdb_id = request.args.get('id')
    
    if not tmdb_id:
        return jsonify({
            "success": False, 
            "error": "TMDB ID missing hai! Link ke aage ?id=TMDB_ID paas karo."
        }), 400

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Referer': 'https://vidsrc.me/'
        }
        
        target_url = f"https://vidsrc.me/embed/movie/{tmdb_id}"
        response = requests.get(target_url, headers=headers, timeout=10)
        
        # Background Scraping for .m3u8 direct stream link
        m3u8_links = re.findall(r'file:\s*["\'](https?://[^\s"\']+\.m3u8[^\s"\']*)["\']', response.text)
        
        if m3u8_links:
            return jsonify({
                "success": True,
                "tmdb_id": tmdb_id,
                "stream_url": m3u8_links[0],
                "type": "hls_direct",
                "note": "Direct ExoPlayer Playable (.m3u8)"
            })
        else:
            return jsonify({
                "success": True,
                "tmdb_id": tmdb_id,
                "stream_url": target_url,
                "type": "embed_fallback",
                "note": "Embed fallback link"
            })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

