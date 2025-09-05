import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

class AirCursorTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.screen_width, self.screen_height = pyautogui.size()
        self.cam_width = 640
        self.cam_height = 480
        self.prev_x, self.prev_y = 0, 0
        self.smoothing = 0.3
        self.click_threshold = 30
        self.is_clicking = False
        self.click_cooldown = 0.3
        self.last_click_time = 0
        self.gesture_cooldown = 1.0
        self.last_gesture_time = 0
        self.drawing_mode = False
        self.draw_points = []
        
    def get_finger_positions(self, landmarks):
        index_tip = landmarks[8]
        thumb_tip = landmarks[4]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        return {
            'index': (index_tip.x, index_tip.y),
            'thumb': (thumb_tip.x, thumb_tip.y), 
            'middle': (middle_tip.x, middle_tip.y),
            'ring': (ring_tip.x, ring_tip.y),
            'pinky': (pinky_tip.x, pinky_tip.y)
        }
    
    def calculate_distance(self, point1, point2):
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def detect_gesture(self, finger_positions):
        index = finger_positions['index']
        thumb = finger_positions['thumb']
        middle = finger_positions['middle']
        ring = finger_positions['ring']
        pinky = finger_positions['pinky']
        thumb_distance = self.calculate_distance(index, thumb)
        middle_distance = self.calculate_distance(index, middle)
        if thumb_distance < 0.05:
            return "click"
        elif thumb_distance < 0.06 and middle_distance < 0.06:
            return "right_click"
        elif middle_distance > 0.1 and thumb_distance > 0.1:
            return "scroll"
        elif all(pos[1] < 0.7 for pos in [index, middle, ring, pinky]):
            return "draw"
        return "move"
    
    def move_cursor(self, x, y):
        screen_x = x * self.screen_width
        screen_y = y * self.screen_height
        smooth_x = self.prev_x + (screen_x - self.prev_x) * self.smoothing
        smooth_y = self.prev_y + (screen_y - self.prev_y) * self.smoothing
        pyautogui.moveTo(smooth_x, smooth_y)
        self.prev_x, self.prev_y = smooth_x, smooth_y
        return int(smooth_x), int(smooth_y)
    
    def perform_click(self, gesture):
        current_time = time.time()
        if current_time - self.last_click_time < self.click_cooldown:
            return False
        if gesture == "click":
            pyautogui.click()
            self.last_click_time = current_time
            return True
        elif gesture == "right_click":
            pyautogui.rightClick()
            self.last_click_time = current_time
            return True
        return False
    
    def handle_scroll(self, current_y, gesture):
        if not hasattr(self, 'scroll_start_y'):
            self.scroll_start_y = current_y
            return
        scroll_diff = self.scroll_start_y - current_y
        if abs(scroll_diff) > 5:
            if scroll_diff > 0:
                pyautogui.scroll(250)
            else:
                pyautogui.scroll(-250)
            self.scroll_start_y = current_y
    
    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cam_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cam_height)
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.001
        print("Air Cursor Started!")
        print("- Point: Move cursor")
        print("- Index + Thumb together: Right click")
        print("- Index finger only (others down): Scroll by moving up/down")
        print("- All fingers up: Start MOVING CURSO")
        print("- Press 'q' to quit")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )
                    finger_positions = self.get_finger_positions(hand_landmarks.landmark)
                    cursor_x, cursor_y = finger_positions['index']
                    screen_x, screen_y = self.move_cursor(cursor_x, cursor_y)
                    gesture = self.detect_gesture(finger_positions)
                    if gesture == "click":
                        if self.perform_click("click"):
                            cv2.putText(frame, "LEFT CLICK!", (10, 100), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    elif gesture == "right_click":
                        if self.perform_click("right_click"):
                            cv2.putText(frame, "RIGhT CLICK!", (10, 100), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                    elif gesture == "scroll":
                        self.handle_scroll(cursor_y * self.cam_height, gesture)
                        cv2.putText(frame, "SCROLL MODE", (10, 100), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    elif gesture == "draw":
                        cv2.putText(frame, "AIR CURSOR MODE", (10, 100), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                    cursor_screen_x = int(cursor_x * frame.shape[1])
                    cursor_screen_y = int(cursor_y * frame.shape[0])
                    cv2.circle(frame, (cursor_screen_x, cursor_screen_y), 15, (0, 255, 255), -1)
                    cv2.circle(frame, (cursor_screen_x, cursor_screen_y), 20, (255, 255, 0), 3)
                    cv2.putText(frame, f"Cursor: ({screen_x}, {screen_y})", (10, 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.putText(frame, f"Gesture: {gesture.upper()}", (10, 60), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Show your hand to control cursor", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.imshow('Air Cursor Control', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    tracker = AirCursorTracker()
    tracker.run()