# MotionIQ — Data Licenses & Usage Terms

## 1. Local Processing Guarantee
MotionIQ operates **strictly local-first**. No video streams, decoded frames, or skeletal landmarks are uploaded, broadcast, or transmitted to any third-party cloud infrastructure or external server.

## 2. Synthetic Test Datasets
- Synthetic videos generated via `examples/generate_sample_video.py` and procedural test cases in `tests/` are generated dynamically via mathematical waveforms (sine/cosine trajectory generators).
- They are licensed under Apache License, Version 2.0.

## 3. User-Provided Data
All videos provided by users remain their sole property. MotionIQ writes analysis outputs to the `outputs/` directory within the user workspace without altering or overwriting source videos.
