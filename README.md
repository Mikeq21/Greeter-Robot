# Greeter-Robot
This project will involve using OpenCV's deep neural network (cv2.dnn) and servo motors to create a robot that greets you when it detects your face. The system captures video, detects faces, calculates their position, and adjusts servo motors to align a camera with the detected face. This creates an interactive system capable of following a person's movement.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Main Script (main.py)](#mainpy)
- [Arduino Code (Face_Tracker.ino)](#face_trackerino)
- [Hardware Requirements](#hardware-requirements)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/Greeter-Robot.git
   cd Greeter-Robot
   ```
2. **Install dependencies:**
   ```sh
   pip install opencv-python pyserial
   ```
3. **Upload the Arduino code:**
   - Open `Face_Tracker.ino` in the Arduino IDE.
   - Select the correct board and port.
   - Upload the sketch.

## Usage
Simply connect the Arduino to power and run the Python script to start face detection and servo movement:
```sh
python main.py
```

# main.py
The `main.py` script is responsible for face tracking and communication with the Arduino.

### Functionality
- Initializes video capture and loads the deep neural network model.
- Detects faces in the video stream and calculates their central coordinates.
- Maps coordinates to servo angles and sends them via serial communication.
- Displays real-time feedback, including bounding boxes around detected faces.

### Dependencies
- OpenCV for image processing and face detection.
- PySerial for communication with the Arduino.

# Face_Tracker.ino
The `Face_Tracker.ino` script handles servo control based on data received from the Python script.

### Functionality
- Initializes servo motors and serial communication.
- Reads incoming serial data and extracts X and Y servo angles.
- Adjusts servo positions to align the camera with the detected face.
- Implements limits to prevent servo overextension.

### Hardware Requirements
- Microcontroller that supports PWM (In my case: Arduino Uno R4 Wifi)
- 2 Servo motors
- 1 pan-tilt servo mounting kit
- 1 USB cable for communication
- 6 male-to-male jumper wires
- 1 Power source for Arduino (Optional)
- 1 Breadboard (Optional, recommended for performance)

## Future Enhancements
- Add speech to robot when detecting speech (Maybe a Chat-GPT based communication).
- Improve face tracking accuracy with depth perception.
- Implement object recognition for additional interactions.

## Contributing
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes.
4. Push your branch: `git push origin feature-name`.
5. Create a pull request.

## License
This project is licensed under [MIT License](LICENSE)

---
**Author:** Michael Quiroga
**GitHub:** [Your GitHub Profile](https://github.com/Mikeq21)

For questions or contributions, feel free to open an issue or pull request!

