from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# GoldAPI endpoint and your API key
GOLD_API_URL = "https://www.goldapi.io/api/XAU/SAR"
API_KEY = "goldapi-3t0f5sm7noc0dp-io"  # Replace with your GoldAPI key

# Karat types
karat_types = ["24K", "22K","21K", "18K","16K", "14K", "10K"]

def get_live_gold_prices():
    """Fetch live gold prices for each karat type from GoldAPI."""
    headers = {
        "x-access-token": API_KEY,
    }
    prices = {}
    
    response = requests.get(GOLD_API_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        prices["24K"] = data["price_gram_24k"]        # Price per gram for the specific karat
        prices["22K"] = data["price_gram_22k"]
        prices["21K"] = data["price_gram_21k"]
        prices["20K"] = data["price_gram_20k"]
        prices["18K"] = data["price_gram_18k"]
        prices["16K"] = data["price_gram_16k"]


    else:
        raise Exception(f"Failed to fetch live gold price for {karat}")
    return prices

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        data = request.get_json()
        weight = float(data["weight"])
        karat = data["karat"]
        total_price = float(data["total_price"])

        # Fetch live gold prices for all karat types
        gold_prices = get_live_gold_prices()

        # Get the price per gram for the selected karat
        gold_price_per_gram = gold_prices[karat]

        # Calculate gold value
        gold_value = weight * gold_price_per_gram

        # Calculate labor charge
        labor_charge = total_price - gold_value

        # Percentage breakdown
        gold_percentage = (gold_value / total_price) * 100
        labor_percentage = (labor_charge / total_price) * 100

        # Return results as JSON
        return jsonify({
            "gold_value": round(gold_value, 2),
            "labor_charge": round(labor_charge, 2),
            "gold_percentage": round(gold_percentage, 2),
            "labor_percentage": round(labor_percentage, 2),
            "gold_price_per_gram": gold_price_per_gram,  # Send price per gram for the selected karat
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)