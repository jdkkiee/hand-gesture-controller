import cv2
import mediapipe as mp
import time
import pyautogui

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from gesture import recognize_gesture


# =========================================================
# DETECT FINGERS
# =========================================================

def detect_fingers(hand_landmarks, handedness):

    fingers = []

    # =====================================================
    # THUMB
    # =====================================================

    thumb_tip = hand_landmarks[4]
    thumb_ip = hand_landmarks[3]

    if handedness == "Right":

        if thumb_tip.x < thumb_ip.x:
            fingers.append(1)
        else:
            fingers.append(0)

    else:

        if thumb_tip.x > thumb_ip.x:
            fingers.append(1)
        else:
            fingers.append(0)

    # =====================================================
    # INDEX
    # =====================================================

    if hand_landmarks[8].y < hand_landmarks[6].y:
        fingers.append(1)
    else:
        fingers.append(0)

    # =====================================================
    # MIDDLE
    # =====================================================

    if hand_landmarks[12].y < hand_landmarks[10].y:
        fingers.append(1)
    else:
        fingers.append(0)

    # =====================================================
    # RING
    # =====================================================

    if hand_landmarks[16].y < hand_landmarks[14].y:
        fingers.append(1)
    else:
        fingers.append(0)

    # =====================================================
    # PINKY
    # =====================================================

    if hand_landmarks[20].y < hand_landmarks[18].y:
        fingers.append(1)
    else:
        fingers.append(0)

    return fingers


# =========================================================
# COMPUTER ACTION
# =========================================================

def perform_action(gesture):

    if gesture == "ONE":

        print("ACTION: NEXT TRACK")

        pyautogui.press("nexttrack")


    elif gesture == "TWO":

        print("ACTION: PLAY / PAUSE")

        pyautogui.press("playpause")


    elif gesture == "THUMB":

        print("ACTION: VOLUME UP")

        pyautogui.press("volumeup")


    elif gesture == "FIST":

        print("ACTION: STOP")

        pyautogui.press("stop")


    elif gesture == "OPEN HAND":

        print("ACTION: MUTE")

        pyautogui.press("volumemute")


    elif gesture == "THREE":

        print("ACTION: THREE")


    elif gesture == "FOUR":

        print("ACTION: FOUR")


# =========================================================
# MEDIAPIPE MODEL
# =========================================================

MODEL_PATH = "models/hand_landmarker.task"


base_options = python.BaseOptions(
    model_asset_path=MODEL_PATH
)


options = vision.HandLandmarkerOptions(

    base_options=base_options,

    running_mode=vision.RunningMode.VIDEO,

    num_hands=2,

    min_hand_detection_confidence=0.5,

    min_hand_presence_confidence=0.5,

    min_tracking_confidence=0.5

)


detector = vision.HandLandmarker.create_from_options(
    options
)


# =========================================================
# CAMERA
# =========================================================

camera = cv2.VideoCapture(1)


if not camera.isOpened():

    print("Kamera tidak dapat dibuka.")

    exit()


# =========================================================
# CAMERA SIZE
# =========================================================

camera.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    1280
)

camera.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    720
)


# =========================================================
# START INFORMATION
# =========================================================

print()
print("==========================================")
print("       HAND GESTURE CONTROLLER")
print("==========================================")
print()
print("Kamera berhasil dibuka!")
print()
print("Gesture:")
print("👊 FIST       → STOP")
print("☝️ ONE        → NEXT TRACK")
print("✌️ TWO        → PLAY / PAUSE")
print("🤟 THREE      → -")
print("🖖 FOUR       → -")
print("🖐️ OPEN HAND  → MUTE")
print("👍 THUMB      → VOLUME UP")
print()
print("Tekan Q untuk keluar.")
print("==========================================")
print()


# =========================================================
# VARIABLES
# =========================================================

frame_timestamp = 0

last_gesture = None

last_action_time = 0

action_cooldown = 1.0


# =========================================================
# MAIN LOOP
# =========================================================

while True:

    # =====================================================
    # READ CAMERA
    # =====================================================

    success, frame = camera.read()


    if not success:

        print("Gagal membaca frame.")

        break


    # =====================================================
    # MIRROR CAMERA
    # =====================================================

    frame = cv2.flip(frame, 1)


    height, width, _ = frame.shape


    # =====================================================
    # BGR → RGB
    # =====================================================

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # =====================================================
    # MEDIAPIPE IMAGE
    # =====================================================

    mp_image = mp.Image(

        image_format=mp.ImageFormat.SRGB,

        data=rgb_frame

    )


    frame_timestamp += 1


    # =====================================================
    # HAND DETECTION
    # =====================================================

    result = detector.detect_for_video(

        mp_image,

        frame_timestamp

    )


    hand_count = len(
        result.hand_landmarks
    )


    # =====================================================
    # IF HAND DETECTED
    # =====================================================

    if result.hand_landmarks:

        for hand_index, hand in enumerate(
            result.hand_landmarks
        ):

            # =================================================
            # HANDEDNESS
            # =================================================

            handedness = (
                result
                .handedness[hand_index][0]
                .category_name
            )


            # =================================================
            # FINGER DETECTION
            # =================================================

            fingers = detect_fingers(
                hand,
                handedness
            )


            # =================================================
            # COUNT FINGERS
            # =================================================

            finger_count = sum(fingers)


            # =================================================
            # RECOGNIZE GESTURE
            # =================================================

            gesture = recognize_gesture(
                fingers
            )


            # =================================================
            # ACTION COOLDOWN
            # =================================================

            current_time = time.time()


            if gesture != "UNKNOWN":

                if (
                    gesture != last_gesture
                    and
                    current_time - last_action_time
                    > action_cooldown
                ):

                    perform_action(
                        gesture
                    )

                    last_gesture = gesture

                    last_action_time = current_time


            # =================================================
            # LANDMARK POINTS
            # =================================================

            points = []


            for landmark in hand:

                x = int(
                    landmark.x * width
                )

                y = int(
                    landmark.y * height
                )


                points.append(
                    (x, y)
                )


                # Draw landmark

                cv2.circle(

                    frame,

                    (x, y),

                    6,

                    (0, 255, 0),

                    -1

                )


            # =================================================
            # HAND CONNECTIONS
            # =================================================

            connections = [

                # Thumb
                (0, 1),
                (1, 2),
                (2, 3),
                (3, 4),

                # Index
                (0, 5),
                (5, 6),
                (6, 7),
                (7, 8),

                # Middle
                (0, 9),
                (9, 10),
                (10, 11),
                (11, 12),

                # Ring
                (0, 13),
                (13, 14),
                (14, 15),
                (15, 16),

                # Pinky
                (0, 17),
                (17, 18),
                (18, 19),
                (19, 20),

                # Palm
                (5, 9),
                (9, 13),
                (13, 17)

            ]


            # =================================================
            # DRAW CONNECTIONS
            # =================================================

            for start, end in connections:

                cv2.line(

                    frame,

                    points[start],

                    points[end],

                    (0, 255, 0),

                    2

                )


            # =================================================
            # DISPLAY HAND
            # =================================================

            cv2.putText(

                frame,

                f"Hand: {handedness}",

                (20, 40),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.8,

                (255, 255, 255),

                2

            )


            # =================================================
            # DISPLAY FINGERS
            # =================================================

            cv2.putText(

                frame,

                f"Fingers: {finger_count}",

                (20, 75),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.8,

                (255, 255, 255),

                2

            )


            # =================================================
            # DISPLAY GESTURE
            # =================================================

            cv2.putText(

                frame,

                f"Gesture: {gesture}",

                (20, 110),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.8,

                (255, 255, 255),

                2

            )


            # =================================================
            # DISPLAY PATTERN
            # =================================================

            cv2.putText(

                frame,

                f"Pattern: {fingers}",

                (20, 145),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.6,

                (255, 255, 255),

                2

            )


    # =====================================================
    # DISPLAY HAND COUNT
    # =====================================================

    cv2.putText(

        frame,

        f"Hands: {hand_count}",

        (20, 185),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.8,

        (255, 255, 255),

        2

    )


    # =====================================================
    # DISPLAY WINDOW
    # =====================================================

    cv2.imshow(

        "Hand Gesture Controller",

        frame

    )


    # =====================================================
    # PRESS Q TO EXIT
    # =====================================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# =========================================================
# CLEANUP
# =========================================================

camera.release()

cv2.destroyAllWindows()

detector.close()


print()
print("Program selesai.")