# Evaluation-of-Packet-Wash-for-Game-Streaming

This repository contains resources to evaluate the Packet Wash technique for scalable video streaming, especially in gaming scenarios.
Requirements

To use this repository, please ensure the following dependencies are installed:
1. JSVM (Joint Scalable Video Model)

Scalable H.264 reference software provided by Fraunhofer HHI.

    Download version 9_19_15 from the official JVET Git repository:
    🔗 https://vcgit.hhi.fraunhofer.de/jvet/jsvm

2. FFmpeg

FFmpeg is required for video processing and visual quality assessments.

    Download FFmpeg from:
    🔗 https://ffmpeg.org/download.html

Ensure your FFmpeg build includes the following filters:

    PSNR (Peak Signal-to-Noise Ratio)

    SSIM (Structural Similarity Index)

    VMAF (Video Multi-Method Assessment Fusion)

Alternatively, you can use the standalone VMAF tool from Netflix:

    🔗 https://github.com/Netflix/vmaf

3. Packet Wash Implementation

This project uses the Packet Wash implementation developed by Stuart Clayman.

    Repository:
    🔗 https://github.com/stuartclayman/h264_over_bpp/
