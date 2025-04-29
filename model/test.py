import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from config import model, CKPT, load


model.load_weights(CKPT)

predictor = tf.keras.Sequential([
    model,
    tf.keras.layers.Softmax()
])

ds = tf.data.TextLineDataset("test.csv").skip(1)


def parse(line):
    fields = tf.io.decode_csv(line, [str()] + [float()] * 2500)
    return fields[0], tf.reshape(fields[1:], shape=(50, 50)) / 255.


ds = load(ds.map(parse))

with open("result.csv", "w") as file:
    file.write("id,label\n")
    for labels, images in ds:
        predict = predictor.predict(images)
        for i, j in enumerate(labels):
            id = j.numpy().decode()
            result = np.argmax(predict[i]) + 1
            file.write(f"{id},{result}\n")
