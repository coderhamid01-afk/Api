from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    movie_id = request.args.get('id')
    
    if not movie_id:
        return jsonify({
            "status": "online",
            "message": "Clean API Active! Test with ?id=157336 (TMDB) or ?id=tt0816692 (IMDB)"
        })
    
    # Ek hi sabse solid server jo Hindi/Multi-Audio aur Subtitles support karta hai
    stream_url = f"https://player.autoembed.cc/embed/movie/{movie_id}"
    
    # 100% Full-Screen Clean Player (No Buttons, No UI Clutter) + Ad Blocker
    player_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Movie Player</title>
        <style>
            /* Sab kuch black aur full screen */
            * {{ margin: 0; padding: 0; box-sizing: border-box; background-color: #000; }}
            body, html {{ width: 100%; height: 100%; overflow: hidden; }}
            iframe {{ width: 100vw; height: 100vh; border: none; display: block; }}
        </style>
        <script>
            // Silent Ad & Popup Blocker
            window.open = function() {{ return null; }};
            window.onblur = function() {{ setTimeout(function() {{ window.focus(); }}, 10); }};
            try {{
                var origLocation = window.location;
                Object.defineProperty(window, 'location', {{
                    configurable: false, enumerable: true,
                    get: function() {{ return origLocation; }},
                    set: function(val) {{ return origLocation; }}
                }});
            }} catch(e) {{}}
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

# Android App ke background JSON ke liye
@app.route('/get-stream', methods=['GET'])
def get_stream():
    movie_id = request.args.get('id', '157336')
    clean_player_url = f"https://api-kappa-seven-44.vercel.app/?id={movie_id}"
    
    return jsonify({
        "success": True,
        "movie_id": movie_id,
        "stream_url": clean_player_url,
        "type": "clean_adfree_player"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

