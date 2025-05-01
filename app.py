from flask import Flask, request, jsonify
import requests
import os
app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
    data = request.get_json()
    if data is None:
        return "No data received", 400
    print(data)
    source_currency = data['queryResult']['parameters']['unit-currency'][0]['currency']
    amount = data['queryResult']['parameters']['unit-currency'][0]['amount']
    destination_currency = data['queryResult']['parameters']['currency-name'][0]

    print(source_currency)
    print(amount)
    print(destination_currency)
    cf = fetch_conversion_factor(source_currency, amount, destination_currency)
    print(cf)
    final_amount = cf*amount
    final_amount = round(final_amount, 2)
    print(final_amount)
    response = {
        "fulfillmentText": "{} {} is {} {}".format(amount, source_currency, final_amount, destination_currency)
    }
    print(jsonify(response))
    return jsonify(response)


def fetch_conversion_factor(source_currency, amount, destination_currency):
    url = "https://api.currencyapi.com/v3/latest?apikey=cur_live_OP81yTcBVUNaIbLMrCJHtgjvsHKiYABs4G96Gzsv&currencies={}&base_currency={}".format(
    destination_currency, source_currency)
    response = requests.get(url)
    response = response.json()
    return response['data'][destination_currency]['value']


if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 14568))
    app.run(debug=True)
