from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Main Route - Direct Ad-Blocked Player
@app.route('/', methods=['GET'])
def home():
    tmdb_id = request.args.get('id')
    
    # Agar bina ID ke link khole toh status dikhao
    if not tmdb_id:
        return jsonify({
            "status": "online",
            "message": "API active hai! Test karne ke liye link ke aage ?id=157336 lagao."
        })
    
    # HTML Sandbox jo Pop-up Ads ko 100% Block kar deta hai
    player_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ad-Free Player - {tmdb_id}</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; background-color: #000; }}
            body, html {{ width: 100%; height: 100%; overflow: hidden; display: flex; justify-content: center; align-items: center; }}
            iframe {{ width: 100%; height: 100%; border: none; }}
        </style>
    </head>
    <body>
        <!-- Sandbox attribute disables popups, new tabs, and redirects -->
        <iframe 
            src="https://vidsrc.me/embed/movie/{tmdb_id}" 
            sandbox="allow-scripts allow-same-origin allow-forms allow-presentation"
            allowfullscreen>
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
        "type": "adfree_player"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

