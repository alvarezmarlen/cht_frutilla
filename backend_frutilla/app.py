from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return {"status": "ok", "message": "API cht_frutilla funcionando perfectamente!"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)