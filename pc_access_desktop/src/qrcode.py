import qrcode as qrc
import io
import base64


def make_qrcode(str_text):
    img = qrc.make(str_text, box_size=4)
    output = io.BytesIO()
    img.save(output, "GIF")
    output.seek(0)
    output_s = output.read()
    image_b64 = base64.b64encode(output_s).decode()
    output.close()
    return image_b64