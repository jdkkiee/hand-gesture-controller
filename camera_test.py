import cv2

camera = cv2.VideoCapture(1)

if not camera.isOpened():
    print("Kamera gagal dibuka")
    exit()

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    success, frame = camera.read()

    if not success:
        print("Frame gagal dibaca")
        break

    print(
        "Min:", frame.min(),
        "| Max:", frame.max(),
        "| Mean:", frame.mean()
    )

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()