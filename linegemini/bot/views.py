import base64
import hashlib
import hmac
import json
import os
import requests

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .ai_reply import get_gemini_response

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def verify_line_signature(body: bytes, signature: str) -> bool:
    if not LINE_CHANNEL_SECRET:
        print("Error: LINE_CHANNEL_SECRET is not set.")
        return False
    mac = hmac.new(LINE_CHANNEL_SECRET.encode("utf-8"), body, hashlib.sha256).digest()
    expected = base64.b64encode(mac).decode("utf-8")
    res = hmac.compare_digest(expected, signature)
    if not res:
        print(f"Signature verification failed. Expected: {expected}, Got: {signature}")
    return res

def line_reply(reply_token: str, message):
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    if not token:
        print("CRITICAL ERROR: LINE_CHANNEL_ACCESS_TOKEN is not set in environment variables!")
    else:
        print(f"Using LINE_CHANNEL_ACCESS_TOKEN starting with: {token[:5]}...")

    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    # 判斷是 Flex Message (dict) 還是純文字 (str)
    if isinstance(message, dict) and message.get("type") == "flex":
        payload = {
            "replyToken": reply_token,
            "messages": [message],
        }
    else:
        payload = {
            "replyToken": reply_token,
            "messages": [{"type": "text", "text": str(message)[:4900]}],
        }

    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()

def send_loading_animation(chat_id: str, loading_seconds: int = 20):
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    url = "https://api.line.me/v2/bot/chat/loading/start"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "chatId": chat_id,
        "loadingSeconds": loading_seconds,
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"Failed to send loading animation: {e}")

@csrf_exempt
def webhook(request):
    if request.method != "POST":
        return HttpResponse("OK")

    body = request.body
    signature = request.headers.get("X-Line-Signature", "")

    if not verify_line_signature(body, signature):
        return JsonResponse({"error": "Invalid signature"}, status=400)

    payload = json.loads(body.decode("utf-8"))
    events = payload.get("events", [])

    for event in events:
        if event.get("type") != "message":
            continue
        msg = event.get("message", {})
        if msg.get("type") != "text":
            continue

        user_text = msg.get("text", "")
        reply_token = event.get("replyToken")
        user_id = event.get("source", {}).get("userId")
        print(user_text, reply_token)

        if user_id:
            send_loading_animation(user_id)

        # 使用 Gemini AI 生成回應
        ai_text = get_gemini_response(user_text)
        line_reply(reply_token, ai_text)

    return HttpResponse("OK")
