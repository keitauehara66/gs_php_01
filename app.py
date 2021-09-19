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

import settings

TOKEN = settings.TOKEN
SECRET = settings.SECRET

line_bot_api = LineBotApi(TOKEN)
handler = WebhookHandler(SECRET)

@app.route("/")
def test():
    return "OK"

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
    import sqlite3
    dbname = 'faqlist.db'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    reply_message = "ごめんなさい、わかりません"
    for c in cur.execute('SELECT * FROM faq'):
        index = event.message.text.find(c[0])
        if index != -1:
            reply_message = f"{c[0]}ですか？{c[0]}は、{c[1]}"
    cur.close()
    conn.close()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))


if __name__ == "__main__":
    app.run()

# https://www.youtube.com/watch?v=jBsvdgFMZtg&t=881s




