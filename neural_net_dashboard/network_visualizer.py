import theano
from theano import tensor as T
import numpy as np
from load import mnist
#from foxhound.utils.vis import grayscale_grid_vis, unit_scale
from scipy.misc import imsave
from matplotlib import pyplot as plt

def floatX(X):
    return np.asarray(X, dtype=theano.config.floatX)

def init_weights(shape):
    return theano.shared(floatX(np.random.randn(*shape) * 0.01))

def sgd(cost, params, lr=0.05):
    grads = T.grad(cost=cost, wrt=params)
    updates = []
    for p, g in zip(params, grads):
        updates.append([p, p - g * lr])
    return updates

def model(X, w_h, w_o):
    h = T.nnet.sigmoid(T.dot(X, w_h))
    pyx = T.nnet.softmax(T.dot(h, w_o))
    return pyx

trX, teX, trY, teY = mnist(onehot=True)

X = T.fmatrix()
Y = T.fmatrix()

w_h = init_weights((784, 625))
w_o = init_weights((625, 10))

py_x = model(X, w_h, w_o)
y_x = T.argmax(py_x, axis=1)

cost = T.mean(T.nnet.categorical_crossentropy(py_x, Y))
params = [w_h, w_o]
updates = sgd(cost, params)

train = theano.function(inputs=[X, Y], outputs=cost, updates=updates, allow_input_downcast=True)
predict = theano.function(inputs=[X], outputs=y_x, allow_input_downcast=True)


train_error = []
test_error = []
fig = plt.figure()

plt.ion()

for i in range(3):
    print i
    for start, end in zip(range(0, len(trX), 128), range(128, len(trX), 128)):
        cost = train(trX[start:end], trY[start:end])
    test_error.append(1-np.mean(np.argmax(teY, axis=1) == predict(teX)))
    train_error.append(1-np.mean(np.argmax(trY, axis=1) == predict(trX)))
    plt.clf()
    plt.plot(test_error)
    plt.hold('on')
    plt.plot(train_error)
    plt.xlim([0,99])
    plt.ylim([0,1])
    plt.legend(['Test Error', 'Train Error'])
    plt.draw()
    plt.show()

plt.show(block=True)