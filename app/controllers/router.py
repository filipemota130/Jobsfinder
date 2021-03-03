from app import app, render_template, request


@app.route('/')
def index():
    return render_template('index.html')
