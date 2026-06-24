# YOLO11m Object Detection on RDK X5 (Live Webcam)

Real-time YOLO11m object detection running **on the RDK X5 BPU** (not on a PC),
with a USB webcam as the live input. Output is observable as both annotated
images and per-detection terminal labels.

- **Board:** RDK X5 (Sunrise/Hobot SoC, BPU Platform 1.3.6)
- **Camera:** Logitech HD Pro Webcam C920 on `/dev/video0`
- **Model:** `yolo11m_detect_bayese_640x640_nv12.bin` (20 MB, COCO 80-class)
- **Runtime:** `hbm_runtime` / HBRT 3.15.55, DNN runtime 1.24.5
- **Measured throughput:** ~10 FPS, single BPU core (`--bpu-cores 0`)

Reference implementation: the `ultralytics_yolo` sample in
[`rdk_model_zoo`](rdk_model_zoo/samples/vision/ultralytics_yolo). The run shown
below is the actual on-device execution.

---

## Detection results (my run)

Detecting `person`, `chair`, `tvmonitor`, `mouse`, `diningtable` from the live
C920 feed. The green `FPS` overlay is drawn each frame.

![YOLO11m detection — frame 1](docs/yolo11_webcam/detection_01.jpg)

![YOLO11m detection — frame 2](docs/yolo11_webcam/detection_02.jpg)

Corresponding terminal output (headless run, labels + confidences per frame):

```
[BPU_PLAT]BPU Platform Version(1.3.6)! soc info(x5)
[HBRT] set log level as 0. version = 3.15.55.0
[DNN] Runtime version = 1.24.5_(3.15.55 HBRT)
[A][DNN][packed_model.cpp:247][Model] [HorizonRT] The model builder version = 1.24.3
frame 0  FPS:   1.5  6 det  [person:0.93, chair:0.52, chair:0.40, chair:0.34, chair:0.31, diningtable:0.42]
frame 1  FPS:  14.7  7 det  [person:0.95, chair:0.65, chair:0.50, chair:0.33, chair:0.32, diningtable:0.35, tvmonitor:0.60]
frame 2  FPS:  12.3  6 det  [person:0.95, chair:0.83, chair:0.53, chair:0.46, chair:0.26, tvmonitor:0.53]
frame 5  FPS:  10.0  6 det  [person:0.95, chair:0.79, chair:0.48, chair:0.34, diningtable:0.26, tvmonitor:0.48]
frame 6  FPS:   9.8  7 det  [person:0.95, chair:0.84, chair:0.44, chair:0.36, chair:0.34, tvmonitor:0.42, mouse:0.29]
Saved annotated frame to /home/sunrise/yolo11m_webcam_proof.jpg
```

The first frame is slower (~1.5 FPS) because it includes model load and first
inference warm-up; subsequent frames settle at ~10 FPS.

---

## How to reproduce

### 1. Prerequisites (already present on this image)

| Component | Check |
|-----------|-------|
| Webcam | `v4l2-ctl --list-devices` → C920 at `/dev/video0` |
| BPU runtime | `python3 -c "import hbm_runtime"` |
| OpenCV | `python3 -c "import cv2; print(cv2.__version__)"` → 4.11.0 |
| Model file | `samples/vision/ultralytics_yolo/model/yolo11m_detect_bayese_640x640_nv12.bin` |
| COCO labels | `datasets/coco/coco_classes.names` |

If the model `.bin` is missing, fetch it from the sample's `model/` directory:

```bash
cd rdk_model_zoo/samples/vision/ultralytics_yolo/model
bash download_model.sh
```

### 2. Run it

```bash
cd rdk_model_zoo/samples/vision/ultralytics_yolo/runtime/python
```

**Headless** (no monitor) — prints labels and saves an annotated frame. This is
the run captured above:

```bash
python3 webcam_detect.py --no-display --max-frames 10 \
    --save ~/yolo11m_webcam_proof.jpg
```

**Live window** (monitor / VNC attached) — press `q` to quit:

```bash
python3 webcam_detect.py --camera 0
```

### 3. Useful options

| Flag | Default | Purpose |
|------|---------|---------|
| `--camera` | `0` | `/dev/video` index |
| `--width` / `--height` | `1280` / `720` | capture resolution |
| `--score-thres` | `0.25` | min confidence to keep a detection |
| `--nms-thres` | `0.70` | NMS IoU threshold |
| `--bpu-cores` | `0` | BPU core(s) to schedule on |
| `--no-display` | off | headless mode (print labels, no window) |
| `--max-frames` | `0` | stop after N frames (`0` = run until quit) |
| `--save PATH` | — | write the last annotated frame to PATH |

---

## Notes

- `--no-display`, `--max-frames`, and `--save` were added to the stock
  `webcam_detect.py` so it can run on a headless board and leave a verifiable
  artifact (annotated image + terminal labels).
- The model is NV12 / 640×640 input; the `UltralyticsYOLODetect` wrapper in
  `ultralytics_yolo_det.py` handles letterbox pre-processing and decode/NMS
  post-processing, so live webcam frames and single-image runs use identical
  logic.
- Confirm the model runs on the **BPU** (not CPU): the `[BPU_PLAT] ... soc
  info(x5)` and `[DNN] Runtime version` banner at startup is the proof.
