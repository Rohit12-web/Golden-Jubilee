from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

# File paths
COUNT_FILE = "rsvp_count.txt"
WISHES_FILE = "wishes.txt"

def get_count():
    if not os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, "w") as f:
            f.write("0")
        return 0
    with open(COUNT_FILE, "r") as f:
        content = f.read().strip()
        return int(content) if content else 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/accept', methods=['POST'])
def accept():
    count = get_count() + 1
    with open(COUNT_FILE, "w") as f:
        f.write(str(count))
    return jsonify({"success": True})

@app.route('/post-wish', methods=['POST'])
def post_wish():
    data = request.get_json()
    name = data.get('guestName')
    message = data.get('guestMessage')

    if name and message:
        # Save to file: Name | Message
        with open(WISHES_FILE, "a", encoding="utf-8") as f:
            f.write(f"{name} | {message}\n")
        return jsonify({"success": True})
    
    return jsonify({"success": False, "error": "Missing fields"}), 400

# Consolidated Admin Dashboard
@app.route('/check')
def admin_dashboard():
    total = get_count()
    wishes = []
    if os.path.exists(WISHES_FILE):
        with open(WISHES_FILE, "r", encoding="utf-8") as f:
            wishes = f.readlines()
            
    # Generate table rows for wishes
    wishes_html = ""
    for w in wishes:
        if "|" in w:
            parts = w.split('|')
            name = parts[0].strip()
            msg = parts[1].strip()
            wishes_html += f"<tr><td style='border:1px solid #ddd; padding:12px;'>{name}</td><td style='border:1px solid #ddd; padding:12px;'>{msg}</td></tr>"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Poppins', sans-serif;
                background-color: #FFF5E1;
                margin: 0;
                padding: 0;
            }}
            .container {{
                text-align: center;
                padding: 40px;
                min-height: 100vh;
            }}
            .card {{
                background: white;
                max-width: 800px;
                margin: auto;
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                text-align: left;
                font-family: 'Poppins', sans-serif;
            }}
            th {{
                background: #1A374D;
                color: white;
                padding: 12px;
            }}
            td {{
                border: 1px solid #ddd;
                padding: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1 style="color: #1A374D; margin-bottom: 10px;">RSVP Dashboard</h1>
                <p style="font-size: 28px; color: #D4AF37; margin-top: 0; font-weight: 600;">Total Guests: {total}</p>
                
                <hr style="border: 0; border-top: 1px solid #eee; margin: 30px 0;">
                
                <h2 style="color: #1A374D;">Guest Wishes & Blessings</h2>
                <table>
                    <thead>
                        <tr>
                            <th style="border-radius: 10px 0 0 0;">Name</th>
                            <th style="border-radius: 0 10px 0 0;">Wish</th>
                        </tr>
                    </thead>
                    <tbody>
                        {wishes_html if wishes_html else "<tr><td colspan='2' style='text-align:center; padding:20px;'>No wishes yet.</td></tr>"}
                    </tbody>
                </table>
                
                <br><br>
                <a href="/" style="display: inline-block; padding: 12px 25px; background-color: #1A374D; color: white; text-decoration: none; border-radius: 30px; font-weight: 600; transition: 0.3s;">Back to Website</a>
            </div>
        </div>
    </body>
    </html>
    """
if __name__ == '__main__':
    app.run(debug=True)