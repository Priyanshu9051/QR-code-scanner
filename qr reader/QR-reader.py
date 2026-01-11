import cv2
from pyzbar import pyzbar
import webbrowser

opened_links = set()   # to avoid opening same link multiple times

def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')

        cv2.rectangle(frame, (x, y), (x + w, y + h),
                      (0, 255, 0), 2)

        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info,
                    (x, y - 10),
                    font, 0.8,
                    (255, 255, 255), 2)

        # Save result
        with open("barcode_result.txt", "w") as file:
            file.write("Recognized Barcode: " + barcode_info)

        # 🔗 OPEN LINK IN BROWSER
        if barcode_info.startswith(("http://", "https://")):
            if barcode_info not in opened_links:
                webbrowser.open(barcode_info)
                opened_links.add(barcode_info)

    return frame


def main():
    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        frame = read_barcodes(frame)
        cv2.imshow("QR / Barcode Reader", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
