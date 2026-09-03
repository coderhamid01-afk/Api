from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    movie_id = request.args.get('id', '157336')
    
    # Stable VidSrc link jo pehle badhiya chal raha tha
    stream_url = f"https://vidsrc.me/embed/movie/{movie_id}"
    
    player_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Movie Player</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; background-color: #000; }}
            body, html {{ width: 100%; height: 100%; overflow: hidden; }}
            iframe {{ width: 100vw; height: 100vh; border: none; display: block; }}
        </style>
        <script>
            // Silent Pop-up & Ad Blocker
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
        "type": "clean_player"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
