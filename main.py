import os
import struct
from io import BytesIO

import cv2
import numpy as np
from PIL import Image

from simple_socket import SimpleSocket

# env variables that are always passed to the program
HOST = os.environ["PALLEON_HOST"]
PORT = int(os.environ["PALLEON_PORT"])

# custom defined environment variables
value = os.environ["palleon_value"]

# state tracking variables and so on to make this function
# I think they have self-explanatory names
last_frame = None
background_subtractor = cv2.createBackgroundSubtractorMOG2()


def calculate_activity(current_frame):
    global last_frame

    # blur the current_frame
    current_frame = cv2.GaussianBlur(current_frame, (5, 5), cv2.BORDER_DEFAULT)

    # cant compare with "nothing"
    if last_frame is None:
        last_frame = current_frame
        return float(0)

    # get a mask of the foreground
    # => the more foreground the more "movement"
    fg_mask = background_subtractor.apply(current_frame)
    _, thresh_frame = cv2.threshold(fg_mask, 30, 255, cv2.THRESH_BINARY)

    # update last_frame for next comparison
    last_frame = current_frame

    return float(cv2.countNonZero(thresh_frame) / (thresh_frame.shape[0] * thresh_frame.shape[1]))


def main():
    with SimpleSocket(HOST, PORT) as s:
        data = b"activity\0" + struct.pack("<i", 5)
        s.sendall(struct.pack("<i", len(data)) + data)

        while True:
            # TODO if needed use data from other plugins
            # here all data from this plugin is received but obviously
            # not needed, and therefore "_"
            _ = s.recv_bson()

            # receive image
            pil_img = Image.open(BytesIO(s.recv_based_on_32bit_integer()))
            # noinspection PyTypeChecker
            np_image = np.array(pil_img, dtype=np.uint8)
            np_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)

            # send new data
            s.send_bson({
                # calculate change / activity
                "changed": calculate_activity(np_image),
            })


if __name__ == "__main__":
    main()
