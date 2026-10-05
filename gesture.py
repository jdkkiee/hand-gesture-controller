def recognize_gesture(fingers):
    """
    fingers:
    [thumb, index, middle, ring, pinky]

    1 = jari terbuka
    0 = jari tertutup
    """

    # 👊 Fist
    if fingers == [0, 0, 0, 0, 0]:
        return "FIST"

    # ☝️ One
    if fingers == [0, 1, 0, 0, 0]:
        return "ONE"

    # ✌️ Two
    if fingers == [0, 1, 1, 0, 0]:
        return "TWO"

    # 🤟 Three
    if fingers == [0, 1, 1, 1, 0]:
        return "THREE"

    # 🖖 Four
    if fingers == [0, 1, 1, 1, 1]:
        return "FOUR"

    # 🖐️ Open Hand
    if fingers == [1, 1, 1, 1, 1]:
        return "OPEN HAND"

    # 👍 Thumb
    if fingers == [1, 0, 0, 0, 0]:
        return "THUMB"

    return "UNKNOWN"