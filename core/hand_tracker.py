import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, mode=False, max_hands=1, detection_con=0.7, track_con=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=mode,
            max_num_hands=max_hands,
            min_detection_confidence=detection_con,
            min_tracking_confidence=track_con
        )
        self.mp_draw = mp.solutions.drawing_utils
        # Tip IDs for Thumb, Index, Middle, Ring, Pinky
        self.tip_ids = [4, 8, 12, 16, 20]

    def find_hands(self, frame, draw=True):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        frame, 
                        hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS
                    )
        return frame

    def get_position(self, frame, hand_no=0):
        landmark_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, landmark in enumerate(my_hand.landmark):
                h, w, c = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                landmark_list.append([id, cx, cy])
        return landmark_list

    def fingers_up(self, landmark_list):
        """
        Determines which fingers are open.
        Returns a list of 5 binary elements: [Thumb, Index, Middle, Ring, Pinky]
        1 = Finger Up, 0 = Finger Down
        """
        if len(landmark_list) == 0:
            return [0, 0, 0, 0, 0]

        fingers = []

        # 1. Thumb Logic (Horizontal check)
        # If the tip is to the right of the inner joint, it's open (adjusted for mirror view)
        if landmark_list[self.tip_ids[0]][1] > landmark_list[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 2. Rest of the 4 Fingers Logic (Vertical check)
        # On screens, Y decreases as you go UP. If Tip Y < PIP joint Y, the finger is extended.
        for id in range(1, 5):
            if landmark_list[self.tip_ids[id]][2] < landmark_list[self.tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers