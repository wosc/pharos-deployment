#!/home/neckharmonics/webhook/bin/python
# Mounted as https://neckharmonics.de/_update

from flask import Flask, request
import hashlib
import hmac
import os
import wsgiref.handlers


app = Flask('webhook')


@app.route('/', methods=['POST'])
def update_view():
    if not verify_signature(
            request.get_data(),
            os.environ['WEBHOOK_TOKEN'],
            request.headers.get('x-hub-signature-256', '')):
        return 'Invalid signature', 400

    with open(os.environ['WEBHOOK_MARKER'], 'w'):
        pass
    return 'OK'


# https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
def verify_signature(payload, secret, signature):
    expected = hmac.new(secret.encode('utf-8'), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest('sha256=' + expected, signature)


@app.errorhandler(Exception)
def handle_error(error):
    return str(error), 500


if __name__ == '__main__':
    os.environ['PATH_INFO'] = '/'
    wsgiref.handlers.CGIHandler().run(app.wsgi_app)
