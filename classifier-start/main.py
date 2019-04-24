# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import lib.gstreamer as gstreamer
import lib.utils as utils

def init_engine(model):
    """Returns an Edge TPU classifier for the model"""
    # TODO: Instantiate a ClassificationEngine for the given model

def input_size(engine):
    """Returns the required input size for the model"""
    # TODO: Return the proper input size for the given model
    return 16, 9

def inference_time(engine):
    """Returns the time taken to run inference"""
    # TODO: Return the inference time from the ClassificationEngine

def classify_image(tensor, engine, labels):
    """Runs inference on the provided input tensor and
    returns an overlay to display the inference results
    """
    # TODO: Run inference on the provided input tensor

def main(args):
    input_source = "{0}:YUY2:{1}:{2}/1".format(args.source, args.resolution, args.frames)
    labels = utils.load_labels(args.labels)
    engine = init_engine(args.model)
    inference_size = input_size(engine)

    def frame_callback(tensor, layout, command):
        results = classify_image(tensor, engine, labels)
        time = inference_time(engine)
        if results and time:
            return utils.overlay('Edge TPU Image Classifier', results, time, layout)

    gstreamer.run(inference_size, frame_callback,
        source=input_source,
        loop=False,
        display=gstreamer.Display.FULLSCREEN)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--source',
                    help='camera device (e.g. /dev/video0)',
                    default='/dev/video0')
    parser.add_argument('--resolution',
                    help='camera capture resolution',
                    default='1280x720')
    parser.add_argument('--frames',
                    help='camera capture frame rate',
                    default='30')
    parser.add_argument('--model', required=True,
                    help='.tflite model path')
    parser.add_argument('--labels', required=True,
                    help='label file path')
    args = parser.parse_args()

    main(args)
