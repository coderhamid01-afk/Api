from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    movie_id = request.args.get('id')
    
    # Agar ID nahi di toh API status dikhao
    if not movie_id:
        return jsonify({
            "status": "online",
            "provider": "AutoEmbed (Multi-Audio)",
            "message": "API Active! Test karne ke liye ?id=157336 lagao."
        })
    
    # AutoEmbed Player URL (Best for Multi-Audio & Subtitles)
    stream_url = f"https://player.autoembed.cc/embed/movie/{movie_id}"
    
    player_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AutoEmbed Secure Player</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; background-color: #000; }}
            body, html {{ width: 100%; height: 100%; overflow: hidden; position: relative; }}
            iframe {{ width: 100vw; height: 100vh; border: none; position: absolute; top: 0; left: 0; z-index: 1; }}
            
            /* Transparent Click-Shield Overlay to block initial ad trigger */
            #adShieldOverlay {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                z-index: 999;
                background: transparent;
                cursor: pointer;
            }}
        </style>
        <script>
            // Anti-Ad & Popup Blockers
            window.open = function() {{ return null; }};
            window.onblur = function() {{ setTimeout(function() {{ window.focus(); }}, 10); }};
            
            // Remove shield on first interaction
            function removeShield() {{
                var overlay = document.getElementById('adShieldOverlay');
                if (overlay) {{ overlay.remove(); }}
            }}
        </script>
    </head>
    <body>
        <div id="adShieldOverlay" onclick="removeShield()"></div>
        <iframe src="{stream_url}" allowfullscreen allow="autoplay; encrypted-media; picture-in-picture"></iframe>
    </body>
    </html>
    """
    return render_template_string(player_html)

# Android App aur Panel integration ke liye JSON endpoint
@app.route('/get-stream', methods=['GET'])
def get_stream():
    movie_id = request.args.get('id', '157336')
    clean_player_url = f"https://api-kappa-seven-44.vercel.app/?id={movie_id}"
    
    return jsonify({
        "success": True,
        "movie_id": movie_id,
        "provider": "AutoEmbed",
        "stream_url": clean_player_url,
        "type": "multi_audio_player"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

