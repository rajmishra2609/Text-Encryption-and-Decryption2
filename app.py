from flask import Flask, render_template, request
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = b'secret_key_for_flask'

def generate_key():
    return Fernet.generate_key()

def load_key():
    try:
        return open("secret.key", "rb").read()
    except:
        return generate_key()

key = load_key()
fernet = Fernet(key)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        action = request.form['action']
        
        if action == 'Encrypt':
            encrypted_text = fernet.encrypt(text.encode()).decode()
            return render_template('index.html', encrypted_text=encrypted_text)
        elif action == 'Decrypt':
            try:
                decrypted_text = fernet.decrypt(text.encode()).decode()
                return render_template('index.html', decrypted_text=decrypted_text)
            except Exception as e:
                error_message = str(e)
                return render_template('index.html', error_message=error_message)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
