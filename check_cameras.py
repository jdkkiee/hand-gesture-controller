import cv2

for camera_id in range(3):

    print(f"\n=== Kamera {camera_id} ===")

    camera = cv2.VideoCapture(camera_id)

    if not camera.isOpened():
        print("Tidak bisa dibuka")
        continue

    success, frame = camera.read()

    if success:
        print("Berhasil membaca frame")
        print("Ukuran:", frame.shape)
        print("Min:", frame.min())
        print("Max:", frame.max())
        print("Mean:", frame.mean())
    else:
        print("Gagal membaca frame")

    camera.release()
    