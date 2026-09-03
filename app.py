from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    # ID can be TMDB (e.g., 157336) OR IMDB (e.g., tt0816692)
    movie_id = request.args.get('id')
    
    if not movie_id:
        return jsonify({
            "status": "online",
            "message": "API Active! Test with TMDB ID (?id=157336) or IMDB ID (?id=tt0816692)"
        })
    
    # Check if ID is IMDb (starts with 'tt')
    is_imdb = str(movie_id).startswith('tt')
    
    # Dynamically setup URLs based on ID type
    url_autoembed = f"https://player.autoembed.cc/embed/movie/{movie_id}"
    url_vidsrc_vip = f"https://vidsrc.vip/embed/movie/{movie_id}"
    url_vidsrc_pro = f"https://vidsrc.pro/embed/movie/{movie_id}"
    
    if is_imdb:
        url_multiembed = f"https://multiembed.mov/?video_id={movie_id}&tmdb=0"
        url_smashy = f"https://embed.smashystream.com/playere.php?imdb={movie_id}"
    else:
        url_multiembed = f"https://multiembed.mov/?video_id={movie_id}&tmdb=1"
        url_smashy = f"https://embed.smashystream.com/playere.php?tmdb={movie_id}"
    
    player_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Universal Player - {movie_id}</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }}
            body, html {{ width: 100%; height: 100%; overflow: hidden; display: flex; flex-direction: column; background-color: #000; }}
            
            .server-bar {{
                display: flex; gap: 10px; padding: 10px 15px; background-color: #121212;
                border-bottom: 2px solid #282828; overflow-x: auto; white-space: nowrap; z-index: 100;
            }}
            .server-bar::-webkit-scrollbar {{ height: 6px; }}
            .server-bar::-webkit-scrollbar-thumb {{ background: #444; border-radius: 10px; }}

            .server-btn {{
                background-color: #1f1f1f; color: #e0e0e0; border: 1px solid #333;
                padding: 8px 16px; border-radius: 25px; cursor: pointer;
                font-size: 13px; font-weight: 600; transition: all 0.2s ease;
                display: flex; flex-direction: column; align-items: center;
            }}
            .server-btn span.subtitle {{ font-size: 9px; color: #888; margin-top: 2px; }}
            .server-btn:hover {{ color: #fff; background-color: #333; }}
            .server-btn.active {{ background-color: #e50914; color: #fff; border-color: #e50914; }}
            .server-btn.active span.subtitle {{ color: #ffcccc; }}
            
            .player-container {{ flex: 1; position: relative; width: 100%; height: 100%; }}
            iframe {{ width: 100%; height: 100%; border: none; position: absolute; top: 0; left: 0; }}
        </style>
        <script>
            // Advanced Anti-Popup & Ad-Blocker
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

            function switchServer(btn, url) {{
                document.getElementById('videoFrame').src = url;
                let btns = document.querySelectorAll('.server-btn');
                btns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            }}
        </script>
    </head>
    <body>
        <div class="server-bar">
            <button class="server-btn active" onclick="switchServer(this, '{url_autoembed}')">
                AutoEmbed <span>(Multi-Audio + Subs)</span>
            </button>
            <button class="server-btn" onclick="switchServer(this, '{url_vidsrc_vip}')">
                VidSrc VIP <span>(Global Dubs)</span>
            </button>
            <button class="server-btn" onclick="switchServer(this, '{url_multiembed}')">
                MultiEmbed <span>(Fast + Dubs)</span>
            </button>
            <button class="server-btn" onclick="switchServer(this, '{url_vidsrc_pro}')">
                VidSrc Pro <span>(Backup Server)</span>
            </button>
            <button class="server-btn" onclick="switchServer(this, '{url_smashy}')">
                SmashyStream <span>(Multi-Subs)</span>
            </button>
        </div>

        <div class="player-container">
            <iframe id="videoFrame" src="{url_autoembed}" allowfullscreen allow="autoplay; encrypted-media; picture-in-picture"></iframe>
        </div>
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
        "is_imdb": str(movie_id).startswith('tt'),
        "stream_url": clean_player_url,
        "type": "universal_adfree_player"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


