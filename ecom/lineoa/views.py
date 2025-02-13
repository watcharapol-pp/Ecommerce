from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from linebot import LineBotApi, WebhookHandler

from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, PostbackEvent, FlexSendMessage
)

from store.models import Product
from . models import Line
from payment.models import Order, OrderItem, ShippingAddress 


# ตั้งค่า LINE Bot API
line_bot_api = LineBotApi('N/QblGki5ripPpDUdWQe4w8qBFAJB44BQEOfbeNZmHa0Te9tZ5sVLRr7SM5Rxe1x/C90Jn1/IhHauU7WpjaQVJAPkDqEMtnCn1yHr5U7rk5iPNpLrNOLk8JOa+m8rUMZZ2isaWbsP7cHPLV6GtMZGAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f639a068ccb2545ffed936c2fad7f4bd')


@csrf_exempt
def callback(request):
    signature = request.headers.get('X-Line-Signature')

    body = request.body.decode('utf-8')

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return HttpResponse(status=400)

    return HttpResponse('OK')


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower().strip()

    if user_message in ['menu', 'เมนู', 'Menu', 'MENU', 'เมณู' , 'meNu', 'MeNu' , 'mENU', 'MenU']:
        send_flex_menu(event)  # ใช้ Flex Message แทน ButtonsTemplate


def send_flex_menu(event):
    flex_message = FlexSendMessage(
        alt_text="เมนูตัวเลือก",
        contents={
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://digitorystyle.com/wp-content/uploads/2023/03/%E0%B8%A1%E0%B8%B5%E0%B8%A1-%E0%B8%A0%E0%B8%B2%E0%B8%9E%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%81%E0%B8%AD%E0%B8%9A%E0%B8%9A%E0%B8%97%E0%B8%84%E0%B8%A7%E0%B8%B2%E0%B8%A1-3-1536x1222.jpg" ,
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {"type": "text", "text": "📋 กรุณาเลือกข้อมูล", "weight": "bold", "size": "xl", "align": "center"},
                    {"type": "separator"},
                    {
                        "type": "button",
                        "action": {"type": "postback", "label": "👤 ข้อมูลผู้ใช้", "data": "action=get_user"},
                        "style": "primary",
                        "height": "md",
                        "color": "#007AFF"
                    },
                    {
                        "type": "button",
                        "action": {"type": "postback", "label": "📍 ที่อยู่จัดส่ง", "data": "action=get_shipping"},
                        "style": "primary",
                        "height": "md",
                        "color": "#34C759"
                    },
                    {
                        "type": "button",
                        "action": {"type": "postback", "label": "📦 คำสั่งซื้อ", "data": "action=get_order"},
                        "style": "primary",
                        "height": "md",
                        "color": "#FF9500"
                    },
                    {
                        "type": "button",
                        "action": {"type": "postback", "label": "🛒 สินค้า & รายการสินค้า", "data": "action=get_product_items"},
                        "style": "primary",
                        "height": "md",
                        "color": "#5856D6"
                    }
                ]
            }
        }
    )
    line_bot_api.reply_message(event.reply_token, flex_message)
    


@handler.add(PostbackEvent)  # ใช้ PostbackEvent ให้ถูกต้อง
def handle_postback(event):
    user_id = event.source.user_id
    action = event.postback.data
    print(f"Received action: {action}")  # Debug ค่า action

    if action == 'action=get_user':
        data = User.objects.values('username', 'email')[:5]
        response_message = "\n".join([f"👤 {user['username']} ({user['email']})" for user in data])
        record_user_request(user_id, 'User Data')

    elif action == 'action=get_shipping':
        data = ShippingAddress.objects.values('full_name', 'address1', 'city')[:5]
        response_message = "\n".join([f"📍 {address['full_name']} - {address['address1']}, {address['city']}" for address in data])
        record_user_request(user_id, 'Shipping Address')

    elif action == 'action=get_order':
        data = Order.objects.values('id', 'date_ordered', 'amount_paid')[:5]
        response_message = "\n".join([f"🛆 Order #{order['id']}: วันที่ {order['date_ordered']} - ชำระเงิน {order['amount_paid']} บาท" for order in data])
        record_user_request(user_id, 'Order Data')

    elif action == 'action=get_product_items':  # รวมสินค้าและรายการสินค้า
        product_data = Product.objects.values('title', 'price', 'brand')[:3]
        order_item_data = OrderItem.objects.select_related('product').values('product__title', 'quantity', 'price')[:3]

        response_message = "🔹 สินค้า:\n"
        response_message += "\n".join([f"📦 {product['title']} ({product['brand']}): {product['price']} บาท" for product in product_data])

        response_message += "\n\n🛍️ รายการสินค้า:\n"
        response_message += "\n".join([f"🛍️ {item['product__title']} x {item['quantity']} - {item['price']} บาท" for item in order_item_data])

        record_user_request(user_id, 'Product & Order Items')

    else:
        response_message = "❌ ไม่พบคำสั่งที่รองรับ"

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_message))


def record_user_request(user_id, data_type):
    """ บันทึกข้อมูลว่าผู้ใช้ร้องขอข้อมูลอะไรบ้าง """
    Line.objects.create(column1=user_id, column2=data_type)