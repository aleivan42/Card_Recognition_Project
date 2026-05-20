import cv2
from card_detection import detect_card
from card_recognition import recognize_card, display_result
from config import CARD_H, CARD_W

def run_webcam_demo(ann_index, metadata):
    print("\n" + "="*60)
    print("WEBCAM DEMO - LIVE PRICING")
    print("="*60)
    print("Controls:\n  SPACE - Recognize card\n  Q     - Quit")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        display_frame = frame.copy()
        warped, contour = detect_card(frame)
        
        if contour is not None:
            cv2.drawContours(display_frame, [contour], -1, (0, 255, 0), 3)
            status_color = (0, 255, 0)
            status_text = "CARD READY - PRESS SPACE"
        else:
            status_color = (0, 0, 255)
            status_text = "SCANNING..."

        cv2.rectangle(display_frame, (0,0), (450, 50), (0,0,0), -1)
        cv2.putText(display_frame, status_text, (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
        
        cv2.imshow('MTG Real-Time Scanner', display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '):
            if warped is not None:
                results = recognize_card(warped, ann_index, metadata)
                display_result(results, warped)
                cv2.waitKey(0)
                cv2.destroyWindow('Result - Press any key')
            else:
                print("Capture failed: No card in focus")
    
    cap.release()
    cv2.destroyAllWindows()