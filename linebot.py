from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('xmkJ+TQglT1hlMeUvChrmZWdj3A0+Z62n5q3IUwVHX3uqUGhNbkjSX/Ck2WhVoj1DO5acJySewlUmTBaBgFNlaUEfv72P3b057h6miyUKC/GWkOAbV4jZLL8jfpCMDvIuT3dMZ0fYU8czDZtjNTtdQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('df2c336b64a104b11c2d2670a5bf3e15')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run(debug=True, port=8000)