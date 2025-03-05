import cv2
import sys
import serial

"""
CHECKLIST               PLAN:
NOT DONE    1. Initialize Serial Communication
                Open a serial connection to your desired port (COMx on Windows).
                Set a baud rate (9600).
DONE        2. Load a Face Detection Model
                Use deep learning-based model, dnn.
DONE        3. Capture Video from Webcam
                Open the camera using cv2.VideoCapture(0).
                Read frames in a loop.
DONE        4. Detect Faces in Each Frame
                Convert the frame to grayscale (for Haar cascades).
                Use detectMultiScale() to find faces.
                X Get the pixel coordinates (x, y, w, h).
NOT DONE    5. Send Coordinates via Serial
                Format the data as a string (e.g., "x,y,w,h\n").
                Use serial.write() to send it over the serial port.
DONE        6. Display the Detection
                Draw rectangles around detected faces.
                Show the video feed using cv2.imshow().
DONE        7. Handle Exit Conditions
                Stop the loop when the user presses a key (cv2.waitKey()).
                Release the camera and close windows (cv2.destroyAllWindows()).
"""

# INITIALIZE VIDEO
s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]

source = cv2.VideoCapture(s)

window_name = "Camera"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# INITIALIZE SERIAL COMMUNICATION
ser = serial.Serial('COM7', 9600)  # Connect to Arduino

# LOAD DEEP NEURAL NET
net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000_fp16.caffemodel")
# Prototxt is a txt type file containing instructions to work with the "caffemodel"

# Model parameters
in_width = 300
in_height = 300
mean = [104, 117, 123]
conf_threshold = 0.7

# RUN LOOP, STOP WHEN ESC KEY PRESSED
while cv2.waitKey(1) != 27:
    # Read from Camera, flip video for viewing and set the width and height (Can be adjusted via the window that opens)
    has_frame, frame = source.read()
    if not has_frame:
        break
    frame = cv2.flip(frame, 1)
    frame_height = frame.shape[0]
    frame_width = frame.shape[1]

    # Create a 4D blob from an image frame so the model can use it.
    blob = cv2.dnn.blobFromImage(frame, 1.0, (in_width, in_height), mean, swapRB=False, crop=False)
    # Run the model
    net.setInput(blob)
    detections = net.forward()

    # DETECT FACE WITH CONFIDENCE AND THRESHOLD
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            # Detection coordinates
            x_top_left = int(detections[0, 0, i, 3] * frame_width)
            y_top_left = int(detections[0, 0, i, 4] * frame_height)
            x_bottom_right = int(detections[0, 0, i, 5] * frame_width)
            y_bottom_right = int(detections[0, 0, i, 6] * frame_height)

            # ARDUINO CODE
            # Calculate x and y middle
            x_middle = (x_bottom_right + x_top_left) // 2
            y_middle = (y_bottom_right + y_top_left) // 2

            # Map to servo parameters
            servo_x = int((x_middle / frame_width) * 180)  # Map x to 0-180°
            servo_y = int((y_middle / frame_height) * 180)  # Map Y to 0-180°
            flip_servo_y = 180 - servo_y  # Y has flipped coordinates (x is correct because of the initial flip())

            # Correct for 2D image onto a 3D space
            normal_servo_x = min(max(servo_x, 30), 150)  # Range between 30° and 150° for preventing overextension
            normal_servo_y = min(max(flip_servo_y, 0), 90)  # Range between 0° and 90° for preventing overextension

            ser.write(f"{normal_servo_x},{normal_servo_y}\n".encode())

            # Display findings to the screen
            cv2.rectangle(frame, (x_top_left, y_top_left), (x_bottom_right, y_bottom_right), (0, 255, 0))
            cv2.circle(frame, (x_middle, y_middle), 10, (255, 0, 0))
            label = "Confidence: %.4f" % confidence
            label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

            cv2.rectangle(
                frame,
                (x_top_left, y_top_left - label_size[1]),
                (x_top_left + label_size[0], y_top_left + base_line),
                (255, 255, 255),
                cv2.FILLED,
            )
            cv2.putText(frame, label, (x_top_left, y_top_left), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    # Report time it takes to calculate to the screen
    t, _ = net.getPerfProfile()
    label = "Inference time: %.2f ms" % (t * 1000.0 / cv2.getTickFrequency())
    cv2.putText(frame, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
    cv2.imshow(window_name, frame)

source.release()
cv2.destroyWindow(window_name)
ser.close()
