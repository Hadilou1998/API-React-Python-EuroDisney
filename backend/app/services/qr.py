import qrcode
from io import BytesIO
import base64

def generate_qr_base64(data: str) -> str:
    img = qrcode.make(data)
    buff = BytesIO()
    img.save(buff, format='PNG')
    img_str = base64.b64encode(buff.getvalue()).decode('utf-8')