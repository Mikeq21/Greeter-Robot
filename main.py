import sys
import cv2
import matplotlib.pyplot as plt


def drawRectangle(frame, bbox):
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)


def displayRectangle(frame, bbox):
    plt.figure(figsize=(20, 10))
    frameCopy = frame.copy()
    drawRectangle(frameCopy, bbox)
    frameCopy = cv2.cvtColor(frameCopy, cv2.COLOR_RGB2BGR)
    plt.imshow(frameCopy)
    plt.axis("off")


def drawText(frame, txt, location, color=(50, 170, 50)):
    cv2.putText(frame, txt, location, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)


def set_Tracker():
    print("Select a Tracker model: \n")

    tracker_types = [
        "BOOSTING",
        "MIL",
        "KCF",
        "CSRT",
        "TLD",
        "MEDIANFLOW",
        "GOTURN",
        "MOSSE",
    ]
    count = 0
    for types in tracker_types:

        print(count, ":", types)
        count += 1

    tracker_select = input("Tracker #: ")
    tracker_type = tracker_types[int(tracker_select)]

    if tracker_type == "BOOSTING":
        tracker = cv2.legacy.TrackerBoosting.create()
    elif tracker_type == "MIL":
        tracker = cv2.legacy.TrackerMIL.create()
    elif tracker_type == "KCF":
        tracker = cv2.TrackerKCF.create()
    elif tracker_type == "CSRT":
        tracker = cv2.TrackerCSRT.create()
    elif tracker_type == "TLD":
        tracker = cv2.legacy.TrackerTLD.create()
    elif tracker_type == "MEDIANFLOW":
        tracker = cv2.legacy.TrackerMedianFlow.create()
    elif tracker_type == "GOTURN":
        tracker = cv2.TrackerGOTURN.create()
    else:
        tracker = cv2.legacy.TrackerMOSSE.create()

    return tracker


def camera_on(tracker):
    camera = 0

    if len(sys.argv) > 1:
        camera = sys.argv[1]

    source = cv2.VideoCapture(camera)

    window_name = 'Camera'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while cv2.waitKey(1) != 27:  # Escape
        has_frame, frame = source.read()
        if not has_frame:
            break
        cv2.imshow(window_name, frame)

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # Draw bounding box
        if ok:
            drawRectangle(frame, bbox)
        else:
            drawText(frame, "Tracking failure detected", (80, 140), (0, 0, 255))

        # Display Info
        drawText(frame, tracker + " Tracker", (80, 60))
        drawText(frame, "FPS : " + str(int(fps)), (80, 100))

    source.release()
    cv2.destroyWindow(window_name)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tracker_selection = set_Tracker()
    camera_on(tracker_selection)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
