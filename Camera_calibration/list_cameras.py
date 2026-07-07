# import cv2

# def list_cameras(max_cameras=10):
#     available = []

#     print("Searching for available cameras...\n")

#     for i in range(max_cameras):
#         cap = cv2.VideoCapture(i)

#         if cap.isOpened():
#             ret, frame = cap.read()
#             if ret:
#                 h, w = frame.shape[:2]
#                 print(f"[{i}] Camera found ({w}x{h})")
#                 available.append(i)

#         cap.release()

#     if not available:
#         print("No cameras found.")
#         return

#     print("\nAvailable camera indices:")
#     print(available)


# if __name__ == "__main__":
#     list_cameras()


import cv2
import numpy as np
import math

MAX_CAMERAS = 10
FRAME_WIDTH = 320
FRAME_HEIGHT = 240

caps = []
indices = []

print("Searching for cameras...")

for i in range(MAX_CAMERAS):
    cap = cv2.VideoCapture(i, cv2.CAP_V4L2)

    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            caps.append(cap)
            indices.append(i)
            print(f"Camera {i} detected")
        else:
            cap.release()
    else:
        cap.release()

if len(caps) == 0:
    print("No cameras found.")
    exit()

print("\nPress the camera number to select it.")
print("Press q to quit.\n")

while True:

    frames = []

    for cap, idx in zip(caps, indices):

        ret, frame = cap.read()

        if not ret:
            frame = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
            cv2.putText(frame,
                        "No Signal",
                        (50,120),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0,0,255),
                        2)
        else:
            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

        cv2.putText(frame,
                    f"Camera {idx}",
                    (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,255,0),
                    2)

        frames.append(frame)

    cols = math.ceil(math.sqrt(len(frames)))
    rows = math.ceil(len(frames)/cols)

    blank = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)

    while len(frames) < rows * cols:
        frames.append(blank.copy())

    grid_rows = []

    for r in range(rows):
        row = np.hstack(frames[r*cols:(r+1)*cols])
        grid_rows.append(row)

    grid = np.vstack(grid_rows)

    cv2.imshow("Available Cameras", grid)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    if ord('0') <= key <= ord('9'):
        cam = key - ord('0')

        if cam in indices:
            print(f"\nSelected camera: {cam}")
            break

for cap in caps:
    cap.release()

cv2.destroyAllWindows()