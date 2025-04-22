from pathlib import Path

import matplotlib.pyplot as plt
import tensorflow as tf


model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(50, 50, 1)),

    tf.keras.layers.Conv2D(32, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(0.2),

    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(0.2),

    tf.keras.layers.Conv2D(64, 3, activation='relu'),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(36)
])

# aug = tf.keras.Sequential([
#     tf.keras.layers.RandomRotation(0.05),
#     tf.keras.layers.RandomZoom(0.05),
#     tf.keras.layers.RandomTranslation(0.05, 0.05),
#     tf.keras.layers.RandomContrast(0.1)
# ])

model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

ds = tf.data.TextLineDataset("train.csv").skip(1)

def parse(line):
    fields = tf.io.decode_csv(line, [int()] + [float()] * 2500)
    return tf.reshape(fields[1:], shape=(50, 50)) / 255., fields[0] - 1

ds = ds.map(parse)

n = 70000

train = (ds.take(n)
    .shuffle(10000)
    .batch(64)
    # .map(lambda x, y: (aug(x), y), num_parallel_calls=tf.data.AUTOTUNE)
    .cache()
    .prefetch(tf.data.AUTOTUNE)
)
valid = ds.skip(n).batch(64).cache().prefetch(tf.data.AUTOTUNE)

history = model.fit(train, validation_data=valid, epochs=10)

plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.2, 1])
plt.legend(loc='lower right')
plt.show()

