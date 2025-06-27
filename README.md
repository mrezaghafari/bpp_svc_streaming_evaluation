# Evaluation-of-Packet-Wash-for-Game-Streaming

Requirements

To use this repository, please ensure the following dependencies are installed:
1. JSVM (Joint Scalable Video Model)

Scalable H.264 reference software provided by Fraunhofer HHI.
Download version 9_19_15 from the official JVET Git repository:
🔗 https://vcgit.hhi.fraunhofer.de/jvet/jsvm
2. FFmpeg

FFmpeg is required for processing video and evaluating quality metrics.
Download it from:
🔗 https://ffmpeg.org/download.html

Ensure that the following filters are enabled during FFmpeg build (or available in your version):

    PSNR (Peak Signal-to-Noise Ratio)

    SSIM (Structural Similarity Index)

    VMAF (Video Multi-Method Assessment Fusion)

Alternatively, you can use VMAF directly from Netflix’s original repository:
🔗 https://github.com/Netflix/vmaf
3. Packet Wash Implementation

This project uses the Packet Wash implementation by Stuart Clayman, available at:
🔗 https://github.com/stuartclayman/h264_over_bpp/
