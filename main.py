import cv2
import pyautogui
import math
import numpy as np
import time
from core.hand_tracker import HandTracker


# ================= CONFIG ================= #

# Toggle features
USE_SMALL_LOW_FATIGUE_BOX = True   # Smaller tracking box for less hand movement
ENABLE_DOUBLE_CLICK = True         # Enable double-click via rapid pinch

# PyAutoGUI settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

# Screen + camera config
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
TARGET_WIDTH = 640
TARGET_HEIGHT = 480

# Bounding box + smoothing
if USE_SMALL_LOW_FATIGUE_BOX:
    BOX_PAD_X = 200
    BOX_TOP = 100
    BOX_BOTTOM = 280
    SMOOTHENING = 2.5
else:
    BOX_PAD_X = 130
    BOX_TOP = 50
    BOX_BOTTOM = 320
    SMOOTHENING = 1.8


# ================= MAIN ================= #

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    tracker = HandTracker(max_hands=1, detection_con=0.5, track_con=0.5)

    prev_x, prev_y = pyautogui.position()
    curr_x, curr_y = prev_x, prev_y

    # Double-click tracking
    last_click_time = 0
    DOUBLE_CLICK_THRESHOLD = 0.35

    print("Level 5 Active: Fatigue reduction and click stabilization running.")

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        display_frame = cv2.resize(frame, (TARGET_WIDTH, TARGET_HEIGHT))

        # Draw bounding box
        cv2.rectangle(
            display_frame,
            (BOX_PAD_X, BOX_TOP),
            (TARGET_WIDTH - BOX_PAD_X, BOX_BOTTOM),
            (255, 255, 0),
            2
        )

        display_frame = tracker.find_hands(display_frame, draw=True)
        landmark_list = tracker.get_position(display_frame)

        if len(landmark_list) == 0:
            cv2.putText(
                display_frame,
                "STATUS: NO HAND DETECTED",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )
        else:
            fingers = tracker.fingers_up(landmark_list)

            cv2.putText(
                display_frame,
                f"GEOFENCE: HAND ACTIVE {fingers}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            # ---------- PINCH DETECTION ----------
            is_pinching = False
            if fingers in ([0, 1, 0, 0, 0], [1, 1, 0, 0, 0]):
                x1, y1 = landmark_list[8][1], landmark_list[8][2]
                x2, y2 = landmark_list[4][1], landmark_list[4][2]

                distance = math.hypot(x2 - x1, y2 - y1)
                if distance < 25:
                    is_pinching = True

            # ---------- CLICK / DOUBLE CLICK ----------
            if is_pinching:
                current_time = time.time()
                delta = current_time - last_click_time

                if ENABLE_DOUBLE_CLICK and delta < DOUBLE_CLICK_THRESHOLD:
                    cv2.putText(display_frame, "DOUBLE CLICK!", (20, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

                    pyautogui.doubleClick()
                    last_click_time = 0
                    cv2.waitKey(400)

                else:
                    cv2.putText(display_frame, "CLICK!", (20, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                    pyautogui.click()
                    last_click_time = current_time
                    cv2.waitKey(200)

            # ---------- CURSOR MOVEMENT ----------
            elif fingers == [0, 1, 0, 0, 0]:
                x1, y1 = landmark_list[8][1], landmark_list[8][2]

                cv2.circle(display_frame, (x1, y1), 8, (0, 0, 255), cv2.FILLED)

                screen_x = np.interp(
                    x1,
                    (BOX_PAD_X, TARGET_WIDTH - BOX_PAD_X),
                    (0, SCREEN_WIDTH)
                )

                screen_y = np.interp(
                    y1,
                    (BOX_TOP, BOX_BOTTOM),
                    (0, SCREEN_HEIGHT)
                )

                curr_x = prev_x + (screen_x - prev_x) / SMOOTHENING
                curr_y = prev_y + (screen_y - prev_y) / SMOOTHENING

                pyautogui.moveTo(int(curr_x), int(curr_y))
                prev_x, prev_y = curr_x, curr_y

            # ---------- SCROLLING ----------
            elif fingers == [0, 1, 1, 0, 0]:
                y_index = landmark_list[8][2]
                center_y = int((BOX_TOP + BOX_BOTTOM) / 2)

                scroll_amount = int((center_y - y_index) * 0.7)

                if abs(scroll_amount) > 5:
                    pyautogui.scroll(scroll_amount)

        cv2.imshow("Lazy Scroller - Shifted Geofence", display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# ================= ENTRY ================= #

if __name__ == "__main__":
    main()