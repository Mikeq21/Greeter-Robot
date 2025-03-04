import cv2
import sys


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def camera_on():
    camera = 0
    if len(sys.argv) > 1:
        camera = sys.argv[1]

    source = cv2.VideoCapture(camera)

    window_name = 'Camera Preview'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while cv2.waitKey(1) != 27:  # Escape
        has_frame, frame = source.read()
        if not has_frame:
            break
        cv2.imshow(window_name, frame)

    source.release()
    cv2.destroyWindow(window_name)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    camera_on()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
