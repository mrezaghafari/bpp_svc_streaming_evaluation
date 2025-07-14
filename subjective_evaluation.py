import os
import cv2
import numpy as np
import argparse

def ensure_dirs(output_dirs):
    for path in output_dirs.values():
        os.makedirs(path, exist_ok=True)

def read_yuv420_frame(file, width, height):
    y_size = width * height
    uv_size = y_size // 4

    y = np.frombuffer(file.read(y_size), dtype=np.uint8).reshape((height, width))
    u = np.frombuffer(file.read(uv_size), dtype=np.uint8).reshape((height // 2, width // 2))
    v = np.frombuffer(file.read(uv_size), dtype=np.uint8).reshape((height // 2, width // 2))

    u_up = cv2.resize(u, (width, height), interpolation=cv2.INTER_LINEAR)
    v_up = cv2.resize(v, (width, height), interpolation=cv2.INTER_LINEAR)

    yuv = cv2.merge((y, u_up, v_up))
    bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
    return bgr

def save_frames_from_yuv(yuv_path, folder, width, height, num_frames):
    with open(yuv_path, 'rb') as f:
        for i in range(num_frames):
            frame = read_yuv420_frame(f, width, height)
            cv2.imwrite(os.path.join(folder, f"frame_{i:04d}.png"), frame)

def create_colored_diff_frames(original_dir, target1_dir, target2_dir, diff_dir, num_frames, threshold=10):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # Larger = more blobby

    for i in range(num_frames):
        orig_path = os.path.join(original_dir, f"frame_{i:04d}.png")
        targ1_path = os.path.join(target1_dir, f"frame_{i:04d}.png")
        targ2_path = os.path.join(target2_dir, f"frame_{i:04d}.png")

        original = cv2.imread(orig_path)
        target1 = cv2.imread(targ1_path)
        target2 = cv2.imread(targ2_path)

        # Compute grayscale absolute differences
        diff1 = cv2.absdiff(original, target1)
        diff2 = cv2.absdiff(original, target2)
        diff1_gray = cv2.cvtColor(diff1, cv2.COLOR_BGR2GRAY)
        diff2_gray = cv2.cvtColor(diff2, cv2.COLOR_BGR2GRAY)

        # Threshold to binary
        _, mask1 = cv2.threshold(diff1_gray, threshold, 255, cv2.THRESH_BINARY)
        _, mask2 = cv2.threshold(diff2_gray, threshold, 255, cv2.THRESH_BINARY)

        # Morphological dilation to make blobs
        mask1_dilated = cv2.dilate(mask1, kernel, iterations=2)
        mask2_dilated = cv2.dilate(mask2, kernel, iterations=2)

        # Optionally blur to smooth edges (comment out if too soft)
        mask1_blurred = cv2.GaussianBlur(mask1_dilated, (5, 5), 0)
        mask2_blurred = cv2.GaussianBlur(mask2_dilated, (5, 5), 0)

        # Generate red and blue highlights
        red_highlight = np.zeros_like(original)
        red_highlight[:, :] = [0, 0, 255]  # Red in BGR

        blue_highlight = np.zeros_like(original)
        blue_highlight[:, :] = [255, 0, 0]  # Blue in BGR

        # Apply masks as alpha channels for blending
        red_masked = cv2.bitwise_and(red_highlight, red_highlight, mask=mask1_blurred)
        blue_masked = cv2.bitwise_and(blue_highlight, blue_highlight, mask=mask2_blurred)

        # Combine and overlay on black background
        final_diff = cv2.add(red_masked, blue_masked)

        out_path = os.path.join(diff_dir, f"frame_{i:04d}.png")
        cv2.imwrite(out_path, final_diff)


def main():
    parser = argparse.ArgumentParser(description='Generate colored diff between two YUV videos.')
    parser.add_argument('original_yuv', help='Path to original YUV file')
    parser.add_argument('target1_yuv', help='Path to target 1 (YUV) file')
    parser.add_argument('target2_yuv', help='Path to target 2 (YUV) file')
    parser.add_argument('width', type=int, help='Frame width')
    parser.add_argument('height', type=int, help='Frame height')
    parser.add_argument('num_frames', type=int, help='Number of frames')

    args = parser.parse_args()

    output_dirs = {
        'original': 'original_frames',
        'target1': 'target1_frames',
        'target2': 'target2_frames',
        'diff': 'diff_frames'
    }

    ensure_dirs(output_dirs)

    print("Extracting original frames...")
    save_frames_from_yuv(args.original_yuv, output_dirs['original'], args.width, args.height, args.num_frames)

    print("Extracting target 1 frames...")
    save_frames_from_yuv(args.target1_yuv, output_dirs['target1'], args.width, args.height, args.num_frames)

    print("Extracting target 2 frames...")
    save_frames_from_yuv(args.target2_yuv, output_dirs['target2'], args.width, args.height, args.num_frames)

    print("Generating colored difference frames...")
    create_colored_diff_frames(output_dirs['original'], output_dirs['target1'], output_dirs['target2'], output_dirs['diff'], args.num_frames)

    print("Done! Check the folders 'original_frames', 'target1_frames', 'target2_frames', and 'diff_frames'.")

if __name__ == "__main__":
    main()
