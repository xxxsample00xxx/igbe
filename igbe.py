from flask import Flask, request, jsonify
import mysql.connector
import bcrypt

app = Flask(__name__)

# MySQL Configuration
db_config = {
    "host": "centerbeam.proxy.rlwy.net",
    "user": "root",
    "password": "pvLTyCYCgBbJoQdskITQclfRZZEYGhww",
    "database": "railway",
    "port": 10996  # Remove quotes to make it an integer
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
    app.run(debug=True)
