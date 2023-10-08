from flask import Flask, render_template, request, Response
from api.comparison import fetch_products, compare_products

app = Flask(__name__)


@app.route('/')
@app.route('/search')
def index():
    return render_template('index.html')


@app.route('/lists')
def lists():
    return render_template('lists.html')


@app.route('/history')
def history():
    return render_template('history.html')


@app.route('/compare/<query>')
def compare(query: str):
    if request.method != "GET" or query.isspace() or query == "":
        return "Bad request", 400

    # Run the product search and comparison
    products = fetch_products(query)
    ctx = compare_products(products)

    # Return a JSON response
    json = ctx.result
    return Response(json, mimetype='application/json')


if __name__ == '__main__':
    app.run()
