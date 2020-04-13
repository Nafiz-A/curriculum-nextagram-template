from flask import Blueprint, render_template, request, redirect, url_for, session
from config import *
import braintree
import requests
payment_blueprint = Blueprint(
    'payment', __name__, template_folder='templates'
)

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=MERCHANT_ID,
        public_key=PUBLIC_KEY,
        private_key=PRIVATE_KEY
    )
)


def send_simple_message():
    print("cooool")
    return requests.post(
        f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
        auth=("api", f"{mailgun_api_key}"),
        data={"from": f"Email from COOL<mailgun@{mailgun_domain}>",
              "to": ["nafizashraf6@gmail.com"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomeness!Fake payment of successful"})


@payment_blueprint.route('/new', methods=['GET'])
def new():
    client_token = gateway.client_token.generate()
    return render_template('payment/new.html', client_token=client_token)


@payment_blueprint.route("/checkout", methods=["POST"])
def checkout():

    nonce_from_the_client = request.form['paymentMethodNonce']
    print(str(request.form['amount']))
    result = gateway.transaction.sale({
        "amount": str(request.form['amount']),
        "payment_method_nonce": nonce_from_the_client,
        # "device_data": device_data_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })
    res = send_simple_message()
    print(res)

    return f"{res}---------------{result}"
