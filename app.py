from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    movie_id = request.args.get('id')
    
    # Testing interface page with a direct button to NetMirror
    test_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NetMirror Test Portal</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; font-family: sans-serif; background-color: #0f0f0f; color: #fff; }
            body { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; padding: 20px; text-align: center; }
            h1 { font-size: 24px; margin-bottom: 10px; color: #4ade80; }
            p { color: #a1a1aa; margin-bottom: 25px; font-size: 14px; }
            .btn { display: inline-block; background: #22c55e; color: #000; padding: 14px 28px; font-size: 16px; font-weight: bold; text-decoration: none; border-radius: 8px; box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3); }
            .btn:hover { background: #16a34a; }
        </style>
    </head>
    <body>
        <h1>NetMirror Testing Portal</h1>
        <p>Apne phone par testing ke liye neeche button dabao!</p>
        <a class="btn" href="https://netmirror.app" target="_blank">Open NetMirror</a>
    </body>
    </html>
    """
    return render_template_string(test_html)

@app.route('/get-stream', methods=['GET'])
def get_stream():
    movie_id = request.args.get('id', '157336')
    return jsonify({
        "success": True,
        "movie_id": movie_id,
        "provider": "NetMirror",
        "target_url": "https://netmirror.app",
        "type": "webview_ready"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
