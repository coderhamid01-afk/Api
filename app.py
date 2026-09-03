from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    movie_id = request.args.get('id', '157336')
    
    # VidSrc Player URL
    stream_url = f"https://vidsrc.me/embed/movie/{movie_id}"
    
    player_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Shielded Movie Player</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; background-color: #000; }}
            body, html {{ width: 100%; height: 100%; overflow: hidden; position: relative; }}
            
            iframe {{ 
                width: 100vw; 
                height: 100vh; 
                border: none; 
                display: block; 
                position: absolute; 
                top: 0; 
                left: 0; 
                z-index: 1; 
            }}
            
            /* Transparent Click-Shield Overlay to block the first ad trigger */
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
            // Block window.open and focus shifts
            window.open = function() {{ return null; }};
            window.onblur = function() {{ setTimeout(function() {{ window.focus(); }}, 10); }};
            
            // Function to remove the shield on the very first user interaction
            function removeShield() {{
                var overlay = document.getElementById('adShieldOverlay');
                if (overlay) {{
                    overlay.remove();
                }}
            }}
        </script>
    </head>
    <body>
        <!-- Invisible Click Shield to catch and kill the first ad popup click -->
        <div id="adShieldOverlay" onclick="removeShield()"></div>
        
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
        "type": "shielded_player"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
