import jetson.inference
import jetson.utils
from jetbot import Robot
import time
import cv2
import numpy as np

# initialize robot object
robot = Robot()


def main():
    # load the SSD Mobilenet model from jetson inference library
    net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.7)
    # define the camera variable
    camera = jetson.utils.gstCamera(1280, 720, "0")  # 'csi://0' for V4L2
    # display variable
    display = jetson.utils.glDisplay()
    # variable to write the output to a file
    writerX = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'MJPG'), 30.0, (1280, 720))

    # capture display object
    while display.IsOpen():
        # read the frame
        img, width, height = camera.CaptureRGBA(zeroCopy=1)

        # find humans in the frame
        detections = net.Detect(img, width, height)
        max_conf = 0
        owner_attr = None

        # iterate through all the humans in the frame
        for detection in detections:
            if detection.ClassID == 1:
                curr_conf = detection.Confidence
                # get the human with highest confidence
                if curr_conf >= max_conf:
                    max_conf = curr_conf
                    owner_attr = detection
        # if there is human in frame
        if owner_attr:
            # make the bot move according to the position of human
            make_move(owner_attr)
        # render the display
        display.RenderOnce(img, width, height)
        display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

        # convert image back to BGR format
        numpy_frame = jetson.utils.cudaToNumpy(img, width, height, 4)
        uint_frame = cv2.cvtColor(numpy_frame, cv2.COLOR_RGBA2RGB).astype(np.uint8)
        bgr_frame = cv2.cvtColor(uint_frame, cv2.COLOR_RGB2BGR)

        # write the frame in BGR format to the output file
        writerX.write(bgr_frame)


def make_move(owner_attr):
    '''
        This function is used to move the bot around
        and follow the human.
    :param owner_attr: position of owner in the frame
    :return: None
    '''

    # get minimum x value
    left = owner_attr.Left

    # get maximum x value
    right = owner_attr.Right

    # get maximum y value
    top = owner_attr.Top

    # get minimum y value
    bottom = owner_attr.Bottom

    # get the center of the bounding box
    center = owner_attr.Center

    # get total area of bounding box
    area = owner_attr.Area
    # print('Area of Bounding box: ',area)

    if not (600 < center[0] < 680):
        # if the human is in the left, move the bot towards left
        if center[0] > 680:
            # print('left', center[0], area)
            robot.right(0.5)
            time.sleep(0.5 * (center[0] - 680) / 680)
            robot.stop()
            return
        # if the human is in the right, move the bot towards right
        if center[0] < 600:
            # print('right', center[0], area)
            robot.left(0.5)
            time.sleep(0.5 * (600 - center[0]) / 600)
            robot.stop()
            return

    # if the human is far, move forward
    if area < 325000:
        # print('forward', center[0], area)
        robot.forward(0.75)
        time.sleep((325000 - area) / 325000)
        robot.stop()

    # if the human is close, move backward
    if area > 350000:
        # print('backward', center[0], area)
        robot.backward(0.75)
        time.sleep((area - 350000) / area)
        robot.stop()


if __name__ == '__main__':
    main()