"""
Deep learning of a simple coin example.
"""
import os
import _thread
import time

import numpy as np

from fujitsu.data_management.data_loader import load_dataset
from fujitsu.models.standard_classifier import ConvnetClassifier
from fujitsu.utils.log import setup_logger
log = setup_logger("main")

n_classes = 2
img_width = img_height = 200
n_channels = 3

# visualization
grid_shape = (4, 4)


def inspect_hidden_weights(model, test_sample, all_samples, all_labels):
    from fujitsu.utils.visualize import visualize_activations, visualize_separation, visualize_roc

    while 1:
        # visualize activations of first hidden layer
        visualize_activations(model, test_sample, 'activations.jpg', grid_shape)

        # visualize data before the softmax
        visualize_separation(model, all_samples, all_labels, 'separation.jpg')

        # create an ROC curve
        visualize_roc(model, all_samples, all_labels)
        time.sleep(10)


if __name__ == '__main__':
    # load the data
    data, mean = load_dataset(os.path.join(os.path.dirname(__file__), "data"))
    np.save('data/data_mean.npy', mean)

    log.debug("Train data shape: {}".format(data['X_train'].shape))

    # initialize the model
    classifier = ConvnetClassifier(name="standard_convnet", n_classes=n_classes,
                                   n_channels=n_channels,
                                   img_width=img_width, img_height=img_height,
                                   dropout=0.5, learning_rate=0.001)

    # continuously inspect the hidden weights in the first layer
    # a quick hack to get a positive example (with a coin in it)
    test_sample = data['X_test'][[np.argmax(data['y_test'][:, 1])]]
    all_samples = data['X_test']
    all_labels = data['y_test']
    try:
        _thread.start_new_thread(inspect_hidden_weights, (classifier, test_sample,
                                                          all_samples, all_labels))
    except:
        log.error("unable to start thread for hidden activation inspection")

    # start the training
    classifier.train(train_samples=data['X_train'], train_labels=data['y_train'],
                     batch_size=32)
