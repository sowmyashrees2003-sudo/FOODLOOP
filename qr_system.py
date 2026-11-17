import qrcode
from io import BytesIO


def generate_qr_code(donation_id):

    qr_data = f"FOODLOOP-DONATION-{donation_id}"

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    qr_image = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    buffer = BytesIO()
    qr_image.save(buffer, format="PNG")

    return buffer.getvalue()