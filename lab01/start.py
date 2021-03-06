#!/usr/bin/python

import os
import sys

from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import ClassificationDataSet
from pybrain.structure.modules import SigmoidLayer

import magic

def _get_keys(dic, i):
    keys = []
    for item in dic:
        if item[i] not in keys:
            keys.append(item[i])
    return keys


def build_net(nbytes, learn_data):
    keys = _get_keys(learn_data, 0)

    net = buildNetwork(nbytes, nbytes/len(keys), len(keys), hiddenclass=SigmoidLayer) #nbytes/len(keys/3)
    ds = ClassificationDataSet(nbytes, nb_classes=len(keys), class_labels=keys)

    for item in learn_data:
        ds.appendLinked(item[1], [keys.index(item[0])])

    ds.calculateStatistics()
    ds._convertToOneOfMany(bounds=[0, 1])

    trainer = BackpropTrainer(net, momentum=0.1, learningrate=0.01, weightdecay=0.01, verbose=True)
    trainer.setData(ds)

    trainer.trainUntilConvergence(maxEpochs=1000)

    return net

def brain(net, data):
    keys = _get_keys(data, 0)

    for item in data:
        result = list(net.activate(item[1]))
        m = max(result)
        i = result.index(m)
        print('out: {0} is {1}, {2} ({3})'.format(m, keys[i], item[0], item[2]))

def read_file(nbytes, filename):
    buf = open(filename, 'r').read(nbytes)
    known_type = magic.from_buffer(buf, mime=True)
    return known_type, [ord(x) for x in buf], filename

def read_files(nbytes, folder):
    return map(lambda f: read_file(nbytes, folder + f), os.listdir(folder))

def main():
    nbytes = int(sys.argv[1])
    learn_data = read_files(nbytes, sys.argv[2])
    test_data = read_files(nbytes, sys.argv[3])
    net = build_net(nbytes, learn_data)

    print('repeat learn data:')
    brain(net, learn_data)
    print('now test data:')
    brain(net, test_data)

if __name__ == '__main__':
    main()
