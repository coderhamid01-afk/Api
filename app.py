from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    # Complete Movie Streaming & Search UI Interface
    portal_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Movie Stream App</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; font-family: sans-serif; background-color: #0b0f19; color: #fff; }
            body { padding: 20px; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
            h1 { font-size: 24px; color: #38bdf8; margin-bottom: 20px; text-align: center; }
            .search-box { width: 100%; max-width: 500px; display: flex; gap: 10px; margin-bottom: 30px; }
            input { flex: 1; padding: 12px 16px; border-radius: 8px; border: 1px solid #334155; background: #1e293b; color: #fff; font-size: 16px; outline: none; }
            input:focus { border-color: #38bdf8; }
            button { background: #0284c7; border: none; padding: 12px 20px; border-radius: 8px; color: #fff; font-weight: bold; cursor: pointer; font-size: 16px; }
            button:hover { background: #0369a1; }
            
            #playerContainer { width: 100%; max-width: 800px; height: 450px; background: #000; border-radius: 12px; overflow: hidden; display: none; margin-top: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); position: relative; }
            iframe { width: 100%; height: 100%; border: none; }
            .hint { color: #94a3b8; font-size: 14px; text-align: center; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h1>🎬 Movie Search & Watch Portal</h1>
        
        <div class="search-box">
            <input type="text" id="movieIdInput" placeholder="TMDB Movie ID daalo (jaise 157336)..." />
            <button onclick="playMovie()">Play</button>
        </div>
        
        <div class="hint">Tip: Interstellar ki ID '157336' hai aur Avengers ki '24428' hai.</div>

        <div id="playerContainer">
            <iframe id="movieIframe" src="" allowfullscreen allow="autoplay; encrypted-media"></iframe>
        </div>

        <script>
            function playMovie() {
                var movieId = document.getElementById('movieIdInput').value.trim();
                if(!movieId) {
                    alert('Pehle movie ID toh daal bhai!');
                    return;
                }
                
                var container = document.getElementById('playerContainer');
                var iframe = document.getElementById('movieIframe');
                
                // Yahan hum AutoEmbed ya NetMirror ka embed link set kar sakte hain
                iframe.src = "https://player.autoembed.cc/embed/movie/" + movieId;
                container.style.display = 'block';
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(portal_html)

@app.route('/get-stream', methods=['GET'])
def get_stream():
    movie_id = request.args.get('id', '157336')
    return jsonify({
        "success": True,
        "movie_id": movie_id,
        "stream_url": f"https://player.autoembed.cc/embed/movie/{movie_id}",
        "type": "multi_audio_player"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
