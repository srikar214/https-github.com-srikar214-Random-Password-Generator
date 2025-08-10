from flask import Flask, render_template, request, jsonify
import string
import secrets

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_password():
    try:
        data = request.get_json()
        length = int(data.get('length', 12))
        
        # Ensure minimum length of 8
        if length < 8:
            return jsonify({
                'error': 'Password length cannot be less than 8 characters'
            }), 400
        
        if length > 128:
            return jsonify({
                'error': 'Password length cannot exceed 128 characters'
            }), 400
        
        # Define character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Combine all characters
        all_characters = lowercase + uppercase + digits + symbols
        
        # Ensure password contains at least one character from each type
        password = [
            secrets.choice(lowercase),
            secrets.choice(uppercase),
            secrets.choice(digits),
            secrets.choice(symbols)
        ]
        
        # Fill the rest of the password length with random characters
        for _ in range(length - 4):
            password.append(secrets.choice(all_characters))
        
        # Shuffle the password list to randomize positions
        secrets.SystemRandom().shuffle(password)
        
        # Convert to string
        generated_password = ''.join(password)
        
        return jsonify({
            'password': generated_password,
            'length': length
        })
        
    except (ValueError, TypeError):
        return jsonify({
            'error': 'Invalid request data'
        }), 400

if __name__ == '__main__':
    app.run(debug=True)