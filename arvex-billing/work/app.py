
import os, stripe
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)

settings = {
    "payment":{
        "razorpay_key_id":"",
        "razorpay_key_secret":"",
        "stripe_publishable_key":"",
        "stripe_secret_key":"",
        "currency":"USD"
    }
}

@app.route("/stripe-checkout", methods=["POST"])
def stripe_checkout():
    stripe.api_key = settings["payment"]["stripe_secret_key"]
    amount = int(float(request.form.get("amount",0))*100)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data":{
                "currency":"usd",
                "product_data":{"name":"Arvex Cloud Hosting"},
                "unit_amount":amount
            },
            "quantity":1
        }],
        mode="payment",
        success_url="http://localhost:5000/success",
        cancel_url="http://localhost:5000/cancel"
    )

    return redirect(session.url)

@app.route("/success")
def success():
    return "Payment Successful. Admin will verify."

@app.route("/cancel")
def cancel():
    return "Payment cancelled."

@app.route("/"
           def home():
               return "Arvex Cloud Running"
app.run(host="0.0.0.0", port=5000)
