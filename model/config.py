import tensorflow as tf


CKPT = "ckpt.weights.h5"

tf.config.threading.set_intra_op_parallelism_threads(8)
tf.config.threading.set_inter_op_parallelism_threads(8)

# 96.46
# tf.keras.layers.Input(shape=(50, 50, 1)),

# tf.keras.layers.Conv2D(32, 3, activation='relu'),
# tf.keras.layers.MaxPooling2D(),

# tf.keras.layers.Conv2D(64, 3, activation='relu'),
# tf.keras.layers.MaxPooling2D(),

# tf.keras.layers.Conv2D(128, 3, activation='relu'),
# tf.keras.layers.MaxPooling2D(),

# tf.keras.layers.Dropout(0.3),

# tf.keras.layers.Conv2D(256, 3, activation='relu'),

# tf.keras.layers.Flatten(),
# tf.keras.layers.Dense(256, activation='relu'),
# tf.keras.layers.Dropout(0.5),
# tf.keras.layers.Dense(36)


# tf.keras.layers.Conv2D(32, 3, padding="same", use_bias=False),
# tf.keras.layers.BatchNormalization(),
# tf.keras.layers.Activation("relu"),
# tf.keras.layers.MaxPooling2D(),
# tf.keras.layers.Dropout(0.2),

# tf.keras.layers.Conv2D(64, 3, padding="same", use_bias=False),
# tf.keras.layers.BatchNormalization(),
# tf.keras.layers.Activation("relu"),
# tf.keras.layers.MaxPooling2D(),
# tf.keras.layers.Dropout(0.3),
# 
# tf.keras.layers.Conv2D(128, 3, padding="same", use_bias=False),
# tf.keras.layers.BatchNormalization(),
# tf.keras.layers.Activation("relu"),
# tf.keras.layers.MaxPooling2D(),
# tf.keras.layers.Dropout(0.4),

# # tf.keras.layers.Conv2D(256, 3, padding="same"),
# 
# tf.keras.layers.Flatten(),

# tf.keras.layers.Dense(256, use_bias=False),
# tf.keras.layers.BatchNormalization(),
# tf.keras.layers.Activation("relu"),
# tf.keras.layers.Dropout(0.5),
# tf.keras.layers.Dense(36)

# 0.2 0.2 0.2 0.2 0.5 - 0.97

augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomRotation(.15),
    tf.keras.layers.RandomZoom(.15)
])


model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(50, 50, 1)),

    # augmentation,

    tf.keras.layers.Conv2D(32, 3, padding="same", use_bias=False),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Activation("relu"),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(0.2),

    tf.keras.layers.Conv2D(64, 3, padding="same", use_bias=False),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Activation("relu"),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(0.2),

    tf.keras.layers.Conv2D(128, 3, padding="same", use_bias=False),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Activation("relu"),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(0.2),
    
    tf.keras.layers.Conv2D(256, 3, padding="same", use_bias=False),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Activation("relu"),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Dropout(0.2),
    
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256, use_bias=False),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Activation("relu"),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(36)
])



model.compile(
    optimizer="adam", # tf.keras.optimizers.SGD(learning_rate=.03, momentum=.9, nesterov=True),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)


def load(dataset, extra=None):
    ds = dataset.batch(32)
    if extra:
        ds = ds.map(lambda x, y: (extra(x)[0], y),
                    num_parallel_calls=tf.data.AUTOTUNE)
    return ds.cache().prefetch(tf.data.AUTOTUNE)


if __name__ == "__main__":
    print(model.summary())
