import matplotlib.pyplot as plt
import tensorflow as tf

from config import model, load, CKPT, augmentation


ds = tf.data.TextLineDataset("train.csv").skip(1)


def parse(line):
    fields = tf.io.decode_csv(line, [int()] + [float()] * 2500)
    return tf.reshape(fields[1:], shape=(50, 50)) > 79, fields[0] - 1


ds = ds.map(parse) #.shuffle(10000)
train_size = 68000

i = 0
for image, label in ds:
    if i == 64:
        break
    img = tf.cast(tf.expand_dims(image, 0), tf.float32)
    augmented = augmentation(img)
    i += 1
    plt.subplot(8, 8, i)
    plt.imshow(image)
    i += 1
    plt.subplot(8, 8, i)
    plt.imshow(augmented[0])
plt.show()
exit()

# reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
#     factor=.5,
#     patience=2,
#     min_lr=0.001
# )

train_ds = load(ds.take(train_size).shuffle(10000))

valid_ds = load(ds.skip(train_size))

history = model.fit(
    train_ds,
    validation_data=valid_ds,
    epochs=15,
    # callbacks=[reduce_lr]
)

model.save_weights(CKPT)

fig, axs = plt.subplots(2)
axs[0].plot(history.history['accuracy'], label='accuracy')
axs[0].plot(history.history['val_accuracy'], label = 'val_accuracy')

axs[1].plot(history.history['loss'], label = 'loss')
axs[1].plot(history.history['val_loss'], label = 'val_loss')

plt.show()
