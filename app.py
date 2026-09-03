from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Main Player Route - Tere Vercel Link Par Chalega
@app.route('/', methods=['GET'])
def home():
    tmdb_id = request.args.get('id')
    
    # Agar bina ID ke link khole toh status dikhao
    if not tmdb_id:
        return jsonify({
            "status": "online",
            "message": "Teri Vercel API Active Hai! Test karne ke liye URL ke aage ?id=157336 lagao."
        })
    
    # JS-based Pop-up Blocker + Clean Embed (Bina sandbox error ke)
    player_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Movie Player - {tmdb_id}</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; background-color: #000; }}
            body, html {{ width: 100%; height: 100%; overflow: hidden; display: flex; justify-content: center; align-items: center; }}
            iframe {{ width: 100%; height: 100%; border: none; }}
        </style>
        <script>
            // Automatic Pop-up Tabs & New Windows Blocker
            window.open = function() {{ return null; }};
            window.onblur = function() {{
                setTimeout(function() {{ window.focus(); }}, 50);
            }};
        </script>
    </head>
    <body>
        <iframe 
            src="https://vidsrc.me/embed/movie/{tmdb_id}" 
            allowfullscreen 
            allow="autoplay; encrypted-media; picture-in-picture">
        </iframe>
    </body>
    </html>
    """
    return render_template_string(player_html)

# JSON Route - Android App ke liye
@app.route('/get-stream', methods=['GET'])
def get_stream():
    tmdb_id = request.args.get('id', '157336')
    clean_player_url = f"https://api-kappa-seven-44.vercel.app/?id={tmdb_id}"
    
    return jsonify({
        "success": True,
        "tmdb_id": tmdb_id,
        "stream_url": clean_player_url,
        "type": "vercel_clean_player"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
