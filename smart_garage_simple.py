import time, imutils
import cv2
import pytesseract
import serial

# ✅ Tell pytesseract exactly where Tesseract OCR is located
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# --- connect to Arduino (check COM port) ---
arduino = serial.Serial('COM9', 9600, timeout=1)
time.sleep(2)

# --- load plate detector ---
plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

# --- authorized numbers ---
authorized = ["KA18EQ0001", "DL01CD5678"]

# (set path only on Windows)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def open_gate():
    print("✅ Authorized Vehicle — Opening Gate")
    arduino.write(b'O')
    time.sleep(1)

# --- start webcam ---
cap = cv2.VideoCapture(0)
print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=700)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in plates:
        roi = frame[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi, config='--psm 8')
        text = ''.join(filter(str.isalnum, text))
        if len(text) >= 6:
            print("Detected:", text)
            if text in authorized:
                open_gate()
            else:
                print("❌ Unauthorized Vehicle")

        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    cv2.imshow("Smart Garage", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
