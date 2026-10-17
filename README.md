# MotionIQ: AI-Powered Human Motion Analysis & Activity Intelligence Platform

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-27%20Passed-brightgreen.svg)]()
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Tasks%20v1.1+-orange.svg)](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker/python)

MotionIQ is a modular, high-precision computer vision and biomechanical motion analysis platform. It processes monocular human video streams, estimates 33 anatomical landmarks, tracks joint trajectories over time, eliminates coordinate jitter via adaptive filtering, executes finite-state movement machines with dual-threshold hysteresis, and produces validated rep counts alongside publication-grade telemetry reports.

---

## 🌟 Key Architecture & Capabilities

```text
motioniq/
├── VideoInputManager      -> Container validation, timestamp extraction, non-destructive frame iterator
├── PoseEstimator          -> Google MediaPipe Pose Landmarker (Lite, Full, Heavy) with strictly increasing video timestamps
├── PersonTracker          -> Primary subject target locking via IoU & torso centroid proximity
├── TemporalSmoother       -> Adaptive 1-Euro Filter with dynamic velocity cutoff & short-gap interpolation
├── GeometryEngine         -> Guarded 3-point vector dot products, 2D/3D angles, angular velocity dθ/dt
├── ExerciseStateMachine   -> 5-state cyclical FSM (Squat, Push-up, Bicep Curl) with hysteresis & depth validation
├── ActivityRecognizer     -> Transparent rule-based classifier + extensible hooks for learned temporal models
├── MotionFeedbackAnalyzer -> Evidence-based form assessment with objective diagnostic reason codes
├── MotionMetricsEngine    -> Bilateral symmetry index, cadence (reps/min), range of motion (ROM), duration stats
├── VideoRenderer          -> Color-coded skeleton limbs, real-time telemetry HUD overlay, multi-codec fallback
└── ReportGenerator        -> Isolated session outputs: MP4, JSON schema, CSV telemetry, MD summary, PNG plots
```

### Supported Exercises:
1. **Squat:** `STANDING` $\to$ `DESCENDING` $\to$ `BOTTOM` $\to$ `ASCENDING` with knee depth verification ($< 95^\circ$), hysteresis guard, and shallow-depth rejection.
2. **Push-up:** `PLANK_TOP` $\to$ `DESCENDING` $\to$ `BOTTOM` $\to$ `ASCENDING` with elbow flexion tracking and chest-to-floor depth validation.
3. **Bicep Curl:** `EXTENDED` $\to$ `FLEXING` $\to$ `PEAK_CONTRACTION` $\to$ `EXTENDING` tracking full contraction ($< 55^\circ$) and complete bottom extension ($> 145^\circ$).

---

## 🚀 Quick Start & Installation

### 1. Prerequisites & Environment Setup

MotionIQ is optimized for **Python 3.11** on Windows and Linux.

#### Windows (PowerShell):
```powershell
# Create dedicated virtual environment with uv or python
python -m uv venv --python 3.11 .venv

# Activate environment
.venv\Scripts\activate

# Install dependencies and MotionIQ in editable mode
python -m uv pip install -e .
```

#### Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Download Official Pose Models (Offline Cache)
Download Google's official MediaPipe Pose Landmarker model bundles (`lite`, `full`, `heavy`):
```powershell
python scripts\download_models.py --variant all
```
Models are saved locally to `models/` (Apache 2.0 licensed).

---

## 🖥️ Running the Application

### Option A: Interactive Web UI (Gradio)
Launch the modern web dashboard with video analysis, kinematic charts, and live webcam modes:
```powershell
python app\main.py
```
Open your browser at: **`http://127.0.0.1:7860`**

### Option B: Command Line Interface (CLI)
Analyze any video file directly from the terminal without opening a browser:
```powershell
# Generate sample squat video for testing
python examples\generate_sample_video.py

# Run CLI analysis
python scripts\run_cli.py --video examples\sample_squat.mp4 --exercise squat --model full
```

Output files will be saved under `outputs/session_<id>/`:
- `annotated_video.mp4` (Annotated with skeleton lines, angle meters, and HUD overlay)
- `pose_data.json` (Structured JSON containing all 33 keypoints per frame)
- `motion_metrics.csv` (Time-series CSV with frame index, timestamp, angles, and states)
- `session_report.json` (Complete audit file with settings, metadata, and performance stats)
- `session_summary.md` (Markdown executive report with repetition and symmetry tables)
- `joint_angle_plot.png` (Kinematic trajectory curve showing repetition peaks)

---

## 🧪 Testing & Verification

MotionIQ features a comprehensive test suite covering mathematical corner cases, synthetic repetition sequences, glitch rejection, and end-to-end integration:

```powershell
# Run all tests
pytest -v
```

### Test Coverage Highlights:
- **GeometryEngine:** Tests 90°, 180°, 45°, collinear points, zero-length vector singularity guards, and NaN handling.
- **TemporalSmoother:** Verifies jitter reduction variance reduction $> 60\%$ on noisy signals and step response latency bounds.
- **Exercise State Machines:** Verifies clean 5-state transitions, rejection of shallow squats, and strict prevention of double-counting.
- **Video & File Security:** Verifies corrupt file handling, unsupported formats, and non-destructive input guarantees.
- **Evaluation Benchmarks:** Standardized ground-truth temporal tolerance window matching for precision, recall, and F1 score.

---

## 📐 Mathematical Formulation

### 1. Joint Angle Calculation
For any joint $B$ flanked by adjacent limbs $A$ and $C$:
$$\mathbf{u} = A - B, \quad \mathbf{v} = C - B$$
$$\cos(\theta) = \text{clip}\left(\frac{\mathbf{u} \cdot \mathbf{v}}{\max(\|\mathbf{u}\|_2 \cdot \|\mathbf{v}\|_2, \epsilon)}, -1.0, 1.0\right)$$
$$\theta = \arccos(\cos(\theta)) \times \frac{180}{\pi}$$

### 2. Adaptive 1-Euro Smoothing
Dynamic cutoff frequency adapts to instantaneous joint speed to suppress static jitter while eliminating lag during explosive movement:
$$f_c = f_{c,\text{min}} + \beta |\dot{x}|$$
$$\alpha = \frac{1}{1 + \frac{1}{2\pi f_c \Delta t}}$$
$$\hat{x}_t = \alpha x_t + (1 - \alpha) \hat{x}_{t-1}$$

---

## ➕ How to Add a New Exercise

Adding a new exercise is modular and straightforward:

1. Create a new subclass of `BaseExerciseStateMachine` in `motioniq/exercises/<name>.py`.
2. Define target states (e.g., `START`, `INFLECTION`, `END`).
3. Define hysteresis thresholds for your primary joint (e.g., knee, elbow, or hip).
4. Implement the `update(angles, timestamp_s, frame_idx)` method.
5. Register your new exercise in `motioniq/exercises/state_machine.py`.

Example:
```python
from motioniq.exercises.base import BaseExerciseStateMachine, StateMachineResult

class CustomExerciseStateMachine(BaseExerciseStateMachine):
    def __init__(self):
        super().__init__(exercise_name="custom")
        self.current_state = "IDLE"

    def update(self, angles, timestamp_s, frame_idx, is_tracking_quality_ok=True):
        # Your custom state transition logic here
        ...
```

---

## ⚠️ Measurement Limitations & Disclaimers

> [!NOTE]
> 1. **Perspective Distortion:** All computed angles are 2D image-plane projected angles. When the subject is rotated diagonally relative to the optical axis, perspective foreshortening may cause slight deviations from true 3D anatomical angles.
> 2. **3D Approximations:** MediaPipe's estimated 3D world landmarks from a monocular camera are synthetic metric estimates, not calibrated laser physical measurements.
> 3. **Non-Clinical Use:** MotionIQ is an engineering and athletic biomechanics analysis tool. Feedback reason codes and rep counts are empirical and do not constitute medical advice or orthopedic diagnosis.

---

## 📄 License & Attribution
- Core MotionIQ source code is licensed under the **Apache License 2.0**.
- Google MediaPipe models are licensed under the **Apache License 2.0**.
- See [MODEL_LICENSES.md](MODEL_LICENSES.md), [DATA_LICENSES.md](DATA_LICENSES.md), and [SECURITY.md](SECURITY.md) for full terms.
