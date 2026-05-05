import os
import stripe
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)

# 🔐 Load from environment (Render friendly)
settings = {
    "payment": {
        "stripe_publishable_key": os.getenv("STRIPE_PUBLISHABLE_KEY", ""),
        "stripe_secret_key": os.getenv("STRIPE_SECRET_KEY", ""),
        "currency": "usd"
    }
}

# 🌍 Auto domain detect (Render or local)
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")


@app.route("/")
def home():
    return "Arvex Cloud Running ✅"


@app.route("/stripe-checkout", methods=["POST"])
def stripe_checkout():
    try:
        stripe.api_key = settings["payment"]["stripe_secret_key"]

        if not stripe.api_key:
            return "Stripe key missing ❌"

        amount = int(float(request.form.get("amount", 0)) * 100)

        if amount <= 0:
            return "Invalid amount ❌"

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": settings["payment"]["currency"],
                    "product_data": {
                        "name": "Arvex Cloud Hosting"
                    },
                    "unit_amount": amount
                },
                "quantity": 1
            }],
            mode="payment",
            success_url=f"{BASE_URL}/success",
            cancel_url=f"{BASE_URL}/cancel"
        )

        return redirect(session.url)

    except Exception as e:
        return f"Error: {str(e)}"


@app.route("/success")
def success():
    return "✅ Payment Successful! Admin will verify."


@app.route("/cancel")
def cancel():
    return "❌ Payment Cancelled."


# 🧪 Simple test form (optional but useful)
@app.route("/checkout")
def checkout_page():
    return '''
    <h2>Arvex Cloud Checkout</h2>
    <form action="/stripe-checkout" method="POST">
        <input type="number" name="amount" placeholder="Enter amount (USD)" required>
        <button type="submit">Pay Now</button>
    </form>
    '''


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
