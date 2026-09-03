from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Health Check
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "message": "Teri Vercel Ad-Free Movie API Active Hai!"
    })

# 1. AD-FREE PLAYER ROUTE (Teri Domain Par Chalega - 0 Popups)
@app.route('/play', methods=['GET'])
def play_movie():
    tmdb_id = request.args.get('id', '157336')
    
    # HTML Sandbox jo Pop-up Ads aur Redirects ko 100% KILL kar deta hai
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
    </head>
    <body>
        <!-- Sandbox attribute disables popups, new windows, and redirects -->
        <iframe 
            src="https://vidsrc.me/embed/movie/{tmdb_id}" 
            sandbox="allow-scripts allow-same-origin allow-forms allow-presentation"
            allowfullscreen>
        </iframe>
    </body>
    </html>
    """
    return render_template_string(player_html)

# 2. JSON API ROUTE (Jo App ke liye Clean Player Link Dega)
@app.route('/get-stream', methods=['GET'])
def get_stream():
    tmdb_id = request.args.get('id')
    
    if not tmdb_id:
        return jsonify({"success": False, "error": "TMDB ID required hai"}), 400

    # Clean Vercel Player Link
    clean_player_url = f"https://api-kappa-seven-44.vercel.app/play?id={tmdb_id}"
    
    return jsonify({
        "success": True,
        "tmdb_id": tmdb_id,
        "stream_url": clean_player_url,
        "type": "adfree_vercel_player",
        "note": "Is link par 0 popups aur 0 ads hain"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
