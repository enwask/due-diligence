from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lists')
def lists():
    return render_template('lists.html')


@app.route('/history')
def history():
    return render_template('history.html')


if __name__ == '__main__':
    app.run()
