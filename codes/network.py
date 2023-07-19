import tensorflow as tf
from tensorflow.keras.layers import Input, Conv1D, Dense, Flatten, Dropout
from tensorflow.keras.layers import Activation, BatchNormalization
from tensorflow.keras.models import Model, Sequential
from tensorflow.python.keras.layers import ReLU


def model():

    inputs = Input(shape=(386*2, 1))
    x = Conv1D(256, kernel_size=3, padding='same')(inputs)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    x = Conv1D(128, kernel_size=3, padding='same')(x)
    x = BatchNormalization()(x)
    x = ReLU()(x)

    x = Conv1D(2, kernel_size=3, padding='same')(x)
    x = ReLU()(x)

    x = Flatten()(x)

    output1 = Dense(512, activation='relu')(x)
    output1 = Dense(256, activation=tf.nn.leaky_relu)(output1)
    output1 = Dense(128, activation='relu')(output1)
    output1 = Dense(17, activation='relu')(output1)

    m_model = Model(inputs=inputs, outputs=output1)
    return m_model


def model_178():

    inputs = Input(shape=(178, 2))

    x = Conv1D(256, kernel_size=3, padding='same')(inputs)
    x = ReLU()(x)
    # # x = Conv1D(128, kernel_size=3, padding='same')(inputs)
    # # x = ReLU()(x)
    # # x = Conv1D(256, kernel_size=3, padding='same')(inputs)
    # # x = ReLU()(x)
    # # x = Conv1D(512, kernel_size=3, padding='same')(x)

    x = Flatten()(x)

    # x = Dense(512, activation='relu')(x)
    x = Dense(256, activation='relu')(x)
    x = Dense(512, activation='relu')(x)
    x = Dense(256, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    x = Dense(64, activation='relu')(x)
    x = Dense(32, activation='relu')(x)
    x = Dense(16, activation='relu')(x)
    # x = Dropout(0.1)(x)
    x = Dense(12)(x)

    m_model = Model(inputs=inputs, outputs=x)
    return m_model


def model_178_3():

    inputs = Input(shape=(178, 3))

    x = Conv1D(256, kernel_size=3, padding='same')(inputs)
    x = ReLU()(x)

    x = Flatten()(x)

    x = Dense(256, activation='relu')(x)
    x = Dense(512, activation='relu')(x)
    x = Dense(256, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    x = Dense(64, activation='relu')(x)
    x = Dense(32, activation='relu')(x)
    x = Dense(16, activation='relu')(x)
    x = Dense(12)(x)

    m_model = Model(inputs=inputs, outputs=x)
    return m_model