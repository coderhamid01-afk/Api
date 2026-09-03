from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = FlaskName = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    movie_id = request.args.get('id')
    
    if not movie_id:
        return jsonify({
            "status": "online",
            "message": "VidSrc Stable API Active! Test with ?id=157336 (TMDB) or ?id=tt0816692 (IMDB)"
        })
    
    # Handle both TMDB ID and IMDb ID for VidSrc
    if str(movie_id).startswith('tt'):
        stream_url = f"https://vidsrc.xyz/embed/movie?imdb={movie_id}"
    else:
        stream_url = f"https://vidsrc.xyz/embed/movie?tmdb={movie_id}"
    
    # Clean, High-Speed Fullscreen Player with VidSrc Stable Engine
    player_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Movie Stream</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; background-color: #000; }}
            body, html {{ width: 100%; height: 100%; overflow: hidden; }}
            iframe {{ width: 100vw; height: 100vh; border: none; display: block; }}
        </style>
        <script>
            // Anti-Ad / Anti-Popup Shield
            window.open = function() {{ return null; }};
            window.onblur = function() {{ setTimeout(function() {{ window.focus(); }}, 10); }};
        </script>
    </head>
    <body>
        <iframe 
            src="{stream_url}" 
            allowfullscreen 
            allow="autoplay; encrypted-media; picture-in-picture">
        </iframe>
    </body>
    </html>
    """
    return render_template_string(player_html)

@app.route('/get-stream', methods=['GET'])
def get_stream():
    movie_id = request.args.get('id', '157336')
    clean_player_url = f"https://api-kappa-seven-44.vercel.app/?id={movie_id}"
    
    return jsonify({
        "success": True,
        "movie_id": movie_id,
        "stream_url": clean_player_url,
        "type": "vidsrc_stable_player"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
