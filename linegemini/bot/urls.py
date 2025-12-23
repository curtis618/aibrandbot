from django.urls import path
from .views import webhook, liff_entry, liff_trigger, generate_image_api, send_generated_image

urlpatterns = [
    path("webhook/", webhook, name="line_webhook"),
    path("liff/", liff_entry, name="liff_entry"),
    path("liff/trigger/", liff_trigger, name="liff_trigger"),
    path("liff/generate/", generate_image_api, name="generate_image"),
    path("liff/send/", send_generated_image, name="send_image"),
]
