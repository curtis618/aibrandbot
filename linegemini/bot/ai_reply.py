import os
import google.generativeai as genai
from .models import Activity

# 從環境變數讀取 API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 設定 Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_activity_card(activity_name: str):
    """
    取得特定活動的詳細資訊。當使用者詢問活動內容、時間或地點時呼叫。
    
    Args:
        activity_name: 活動名稱 (例如: 台北馬拉松, 跨年晚會, 科技展)
    """
    print(f"🔍 [Tool Calling] 正在查詢活動: {activity_name}")
    
    # 從資料庫搜尋活動
    # 使用 icontains 進行模糊搜尋
    activity = Activity.objects.filter(name__icontains=activity_name).first()
            
    if not activity:
        return "找不到相關活動資訊。"

    # 回傳 LINE Flex Message 格式
    return {
        "type": "flex",
        "altText": f"{activity.name} 活動資訊",
        "contents": {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": activity.image_url if activity.image_url else "https://via.placeholder.com/1024x768",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": activity.name, "weight": "bold", "size": "xl"},
                    {"type": "box", "layout": "vertical", "margin": "lg", "spacing": "sm", "contents": [
                        {"type": "box", "layout": "baseline", "spacing": "sm", "contents": [
                            {"type": "text", "text": "結束日期", "color": "#aaaaaa", "size": "sm", "flex": 2},
                            {"type": "text", "text": str(activity.end_date), "wrap": True, "color": "#666666", "size": "sm", "flex": 5}
                        ]},
                        {"type": "box", "layout": "baseline", "spacing": "sm", "contents": [
                            {"type": "text", "text": "地點", "color": "#aaaaaa", "size": "sm", "flex": 2},
                            {"type": "text", "text": activity.location, "wrap": True, "color": "#666666", "size": "sm", "flex": 5}
                        ]}
                    ]},
                    {"type": "text", "text": activity.description, "wrap": True, "margin": "md", "color": "#666666"}
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {"type": "button", "style": "link", "height": "sm", "action": {"type": "uri", "label": "活動詳情", "uri": activity.activity_link if activity.activity_link else "https://line.me/"}}
                ],
                "flex": 0
            }
        }
    }

def get_recent_activities():
    """
    取得最近的所有活動列表。當使用者詢問「最近有什麼活動」、「有哪些活動」時呼叫。
    """
    print(f"🔍 [Tool Calling] 正在查詢最近活動列表")
    
    # 從資料庫取得所有活動 (依日期排序)
    activities = Activity.objects.all().order_by('end_date')[:5]

    if not activities:
        return "目前沒有任何活動資訊。"

    bubbles = []
    for data in activities:
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": data.image_url if data.image_url else "https://via.placeholder.com/1024x768",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": data.name, "weight": "bold", "size": "xl"},
                    {"type": "box", "layout": "vertical", "margin": "lg", "spacing": "sm", "contents": [
                        {"type": "box", "layout": "baseline", "spacing": "sm", "contents": [
                            {"type": "text", "text": "結束日期", "color": "#aaaaaa", "size": "sm", "flex": 2},
                            {"type": "text", "text": str(data.end_date), "wrap": True, "color": "#666666", "size": "sm", "flex": 5}
                        ]},
                        {"type": "box", "layout": "baseline", "spacing": "sm", "contents": [
                            {"type": "text", "text": "地點", "color": "#aaaaaa", "size": "sm", "flex": 2},
                            {"type": "text", "text": data.location, "wrap": True, "color": "#666666", "size": "sm", "flex": 5}
                        ]}
                    ]},
                    {"type": "text", "text": data.description, "wrap": True, "margin": "md", "color": "#666666"}
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {"type": "button", "style": "link", "height": "sm", "action": {"type": "uri", "label": "活動詳情", "uri": data.activity_link if data.activity_link else "https://line.me/"}}
                ],
                "flex": 0
            }
        }
        bubbles.append(bubble)

    return {
        "type": "flex",
        "altText": "最近活動列表",
        "contents": {
            "type": "carousel",
            "contents": bubbles
        }
    }

def get_studio_introduction():
    """
    介紹工作室資訊。當使用者詢問「介紹工作室」、「關於我們」、「你們是誰」時呼叫。
    """
    print(f"🔍 [Tool Calling] 正在取得工作室介紹影片")
    
    # 這裡使用範例影片與圖片，請替換成您實際的 HTTPS 網址
    # 注意：影片與預覽圖的長寬比必須一致，且符合 aspectRatio 設定
    video_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
    preview_url = "https://www.nups.ntnu.edu.tw/upfiles/univ-expo/%E4%B8%AD%E9%83%A8/%E5%8D%97%E6%8A%95%E7%B8%A3/%E6%9A%A8%E5%8D%97/%E6%9A%A8%E5%8D%97-pic06.jpg"
    aspect_ratio = "16:9"

    return {
        "type": "flex",
        "altText": "工作室介紹影片",
        "contents": {
            "type": "bubble",
            "hero": {
                "type": "video",
                "url": video_url,
                "previewUrl": preview_url,
                "altContent": {
                    "type": "image",
                    "size": "full",
                    "aspectRatio": aspect_ratio,
                    "aspectMode": "cover",
                    "url": preview_url
                },
                "aspectRatio": aspect_ratio
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "關於我們",
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "text",
                        "text": "我們是 AI Brand Bot 工作室，致力於將人工智慧技術應用於品牌行銷與客戶服務。",
                        "wrap": True,
                        "margin": "md",
                        "color": "#666666"
                    }
                ]
            }
        }
    }

my_tools = [get_activity_card, get_recent_activities, get_studio_introduction]

def get_gemini_response(user_text: str):
    """
    將使用者的訊息傳送給 Gemini API 並取得回應 (支援 Function Calling 回傳 Flex Message)
    """
    if not GEMINI_API_KEY:
        return "系統設定錯誤：找不到 GEMINI_API_KEY，請檢查 .env 檔案。"

    try:
        # 初始化模型
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash', 
            tools=my_tools
        )
        
        # 啟動 Chat (不使用自動 Function Calling，我們要自己處理回傳值)
        chat = model.start_chat(enable_automatic_function_calling=False)
        
        # 發送訊息
        response = chat.send_message(user_text)
        
        # 檢查是否有 Function Call
        if response.candidates and response.candidates[0].content.parts:
            part = response.candidates[0].content.parts[0]
            if part.function_call:
                fc = part.function_call
                if fc.name == 'get_activity_card':
                    # 直接執行並回傳 Flex Message (Dict)
                    return get_activity_card(fc.args['activity_name'])
                elif fc.name == 'get_recent_activities':
                    return get_recent_activities()
                elif fc.name == 'get_studio_introduction':
                    return get_studio_introduction()
        
        # 正常文字回應
        if response and response.text:
            return response.text
        else:
            return "Gemini 沒有回應任何內容。"
            
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "抱歉，我現在有點忙不過來，請稍後再試一次。"
