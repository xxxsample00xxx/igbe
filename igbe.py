from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import mysql.connector
import bcrypt

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MySQL Configuration
db_config = {
    "host": "centerbeam.proxy.rlwy.net",
    "user": "root",
    "password": "pvLTyCYCgBbJoQdskITQclfRZZEYGhww",
    "database": "railway",
    "port": 10996
}

# Connect to MySQL
def connect_db():
    return mysql.connector.connect(**db_config)

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400

        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insert into database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
