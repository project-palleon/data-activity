import os
from collections import defaultdict


import cv2
import numpy as np
from palleon.data_plugin import DataPlugin, Dependency


# custom defined environment variables
value = os.environ["palleon_value"]


class ActivityDataPlugin(DataPlugin):
    def __init__(self):
        super().__init__([Dependency("activity", nr_history=5)])

        self._background_subtractors = defaultdict(lambda: cv2.createBackgroundSubtractorMOG2())

    def image_received_hook(self, data, image, input_source, other_metadata):
        current_frame = np.array(image, dtype=np.uint8)
        current_frame = cv2.cvtColor(current_frame, cv2.COLOR_RGB2GRAY)

        # blur the current_frame
        current_frame = cv2.GaussianBlur(current_frame, (5, 5), cv2.BORDER_DEFAULT)

        # get a mask of the foreground
        # => the more foreground the more "movement"
        fg_mask = self._background_subtractors[input_source].apply(current_frame)
        _, thresh_frame = cv2.threshold(fg_mask, 30, 255, cv2.THRESH_BINARY)

        activity = float(cv2.countNonZero(thresh_frame) / (thresh_frame.shape[0] * thresh_frame.shape[1]))

        return {
            "changed": activity,
        }


if __name__ == "__main__":
    ActivityDataPlugin().run()
