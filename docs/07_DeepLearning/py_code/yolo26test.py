import cv2
from ultralytics import YOLO

model = YOLO("yolo26n.pt")  # 또는 학습한 모델

cap = cv2.VideoCapture(0)   # 기본 웹캠

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # stream=True 대신 단일 프레임 추론 (메모리 효율)
    results = model(frame, conf=0.5, verbose=False)
    annotated = results[0].plot()

    cv2.imshow("YOLO26 실시간 탐지", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # q키로 종료
        break

cap.release()
cv2.destroyAllWindows()
