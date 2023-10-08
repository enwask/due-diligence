from flask import Flask, render_template, request, Response
from api.comparison import fetch_products, compare_products
import json

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
    products = fetch_products(query, max_desc_len=400)
    ctx = compare_products(products)


    # Return a JSON response
    print("STRING:")
    print(ctx.result)
    print("END STRING")
    res = json.loads(ctx.result)

    i = 0
    for key, value in res.items():
        res[key]["url"] = products[i]["url"]
        res[key]["price"] = products[i]["price"]
        res[key]["thumbnail"] = products[i]["thumbnail"]
        i += 1

    return Response(json.dumps(res), mimetype='application/json')


if __name__ == '__main__':
    app.run(processes=4, threaded=True)
