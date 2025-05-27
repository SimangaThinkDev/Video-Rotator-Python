import cv2
from moviepy.editor import VideoFileClip, AudioFileClip
import os

def rotate_video(input_path, output_path, rotation=90):
    """Rotate video while preserving audio"""
    
    # Validate rotation angle
    if rotation not in [90, 180, 270]:
        raise ValueError("Only 90, 180, or 270 degree rotations supported")
    
    # Create temp file path
    temp_path = "temp_no_audio.mp4"
    
    # OpenCV rotation
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Swap dimensions for 90/270 degree rotations
    if rotation in [90, 270]:
        width, height = height, width
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_path, fourcc, fps, (width, height))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Apply rotation
        if rotation == 90:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        elif rotation == 180:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
        elif rotation == 270:
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        out.write(frame)
    
    cap.release()
    out.release()
    
    # Merge audio using MoviePy
    try:
        video_clip = VideoFileClip(temp_path)
        audio_clip = AudioFileClip(input_path)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input video file")
    parser.add_argument("output", help="Output video file")
    parser.add_argument("--rotation", type=int, choices=[90, 180, 270], default=90,
                      help="Rotation angle (90, 180, or 270 degrees)")
    args = parser.parse_args()
    
    rotate_video(args.input, args.output, args.rotation)