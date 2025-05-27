import cv2

# Open the video file
cap = cv2.VideoCapture('rename.mp4')

# /home/innocent/Videos/Elevator Pitch.mp4

# Get video properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Create VideoWriter for output (rotate 90° clockwise)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_rotated.mp4', fourcc, fps, (height, width))  # Note swapped width/height

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Rotate frame 90° clockwise
    rotated = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    
    out.write(rotated)

cap.release()
out.release()