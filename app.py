from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    movie_id = request.args.get('id')
    
    # 1. Agar ID di hai, toh Ad-Free Secure Player dikhao
    if movie_id:
        stream_url = f"https://vidsrc.me/embed/movie/{movie_id}"
        
        player_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Secure Movie Player</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; background-color: #000; }}
                body, html {{ width: 100%; height: 100%; overflow: hidden; position: relative; }}
                iframe {{ width: 100vw; height: 100vh; border: none; position: absolute; top: 0; left: 0; z-index: 1; }}
                
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
                
                .back-btn {{
                    position: fixed;
                    top: 20px;
                    left: 20px;
                    z-index: 1000;
                    background: rgba(20, 20, 20, 0.8);
                    color: #fff;
                    padding: 10px 20px;
                    border-radius: 30px;
                    text-decoration: none;
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 14px;
                    font-weight: 600;
                    border: 1px solid #444;
                    backdrop-filter: blur(5px);
                    transition: background 0.2s;
                }}
                .back-btn:hover {{
                    background: #e50914;
                    border-color: #e50914;
                }}
            </style>
            <script>
                window.open = function() {{ return null; }};
                window.onblur = function() {{ setTimeout(function() {{ window.focus(); }}, 10); }};
                function removeShield() {{
                    var overlay = document.getElementById('adShieldOverlay');
                    if (overlay) {{ overlay.remove(); }}
                }}
            </script>
        </head>
        <body>
            <a href="/" class="back-btn">⬅ Back to Search</a>
            <div id="adShieldOverlay" onclick="removeShield()"></div>
            <iframe src="{stream_url}" allowfullscreen allow="autoplay; encrypted-media; picture-in-picture"></iframe>
        </body>
        </html>
        """
        return render_template_string(player_html)
    
    # 2. Agar ID nahi hai, toh Netflix-Style Search Homepage dikhao
    search_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mini Netflix - Search Movies</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #141414; color: #fff; }
            body { display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding: 40px 20px; }
            h1 { color: #e50914; margin-bottom: 25px; font-size: 2.8rem; text-align: center; font-weight: 800; letter-spacing: 1px; }
            
            .search-box { display: flex; gap: 12px; width: 100%; max-width: 650px; margin-bottom: 40px; }
            input { flex: 1; padding: 14px 24px; font-size: 16px; border-radius: 30px; border: 1px solid #333; background: #222; color: #fff; outline: none; transition: border-color 0.2s; }
            input:focus { border-color: #e50914; }
            button { padding: 14px 28px; border-radius: 30px; border: none; background: #e50914; color: #fff; font-weight: bold; font-size: 16px; cursor: pointer; transition: background 0.2s; }
            button:hover { background: #b80710; }
            
            .results-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 20px; width: 100%; max-width: 1100px; }
            .movie-card { background: #1f1f1f; border-radius: 12px; overflow: hidden; cursor: pointer; transition: transform 0.2s, border-color 0.2s; border: 1px solid #333; display: flex; flex-direction: column; }
            .movie-card:hover { transform: scale(1.05); border-color: #e50914; }
            .movie-card img { width: 100%; height: 230px; object-fit: cover; background: #2c2c2c; }
            .movie-info { padding: 12px; font-size: 14px; text-align: center; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
            .loading { color: #888; font-size: 16px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>🎬 Mini Netflix</h1>
        <div class="search-box">
            <input type="text" id="query" placeholder="Search any movie (e.g. Interstellar, Avatar, Batman)..." onkeydown="if(event.key==='Enter') searchMovies()">
            <button onclick="searchMovies()">Search</button>
        </div>
        <div class="results-grid" id="results"></div>

        <script>
            const TMDB_API_KEY = "3fd2be6f0c70a2a598f084ddfb75487c"; // Public demo key
            
            async function searchMovies() {
                const query = document.getElementById('query').value.trim();
                const grid = document.getElementById('results');
                if(!query) return;
                
                grid.innerHTML = '<p class="loading" style="grid-column: 1/-1; text-align: center;">Searching movies...</p>';
                
                try {
                    const res = await fetch(`https://api.themoviedb.org/3/search/movie?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(query)}`);
                    const data = await res.json();
                    
                    grid.innerHTML = '';
                    
                    if(!data.results || data.results.length === 0) {
                        grid.innerHTML = '<p class="loading" style="grid-column: 1/-1; text-align: center;">No movies found!</p>';
                        return;
                    }
                    
                    data.results.forEach(movie => {
                        if (!movie.poster_path) return;
                        const card = document.createElement('div');
                        card.className = 'movie-card';
                        card.onclick = () => {
                            window.location.href = `/?id=${movie.id}`;
                        };
                        
                        card.innerHTML = `
                            <img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" alt="${movie.title}">
                            <div class="movie-info">${movie.title}</div>
                        `;
                        grid.appendChild(card);
                    });
                } catch(err) {
                    grid.innerHTML = '<p class="loading" style="grid-column: 1/-1; text-align: center; color: #ff4444;">Error fetching movies!</p>';
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(search_html)

@app.route('/get-stream', methods=['GET'])
def get_stream():
    movie_id = request.args.get('id', '157336')
    clean_player_url = f"https://api-kappa-seven-44.vercel.app/?id={movie_id}"
    return jsonify({"success": True, "movie_id": movie_id, "stream_url": clean_player_url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
