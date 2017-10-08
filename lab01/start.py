#!/usr/bin/python

import os
#import binascii

#import itertools

from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import ClassificationDataSet #SupervisedDataSet
from pybrain.structure import LinearLayer #TanhLayer

import magic # for teach

def network():
    net = buildNetwork(2, 3, hiddenclass=LinerLayer)

    ds = SupervisedDataSet(2, 1)
    classificationDataSet(2, nb_classes=3, class_labels=['A', 'B', 'C', 'D', 'Z'])

    for input, target in data:
        ds.addSample(input, target)

    trainer = BackpropTrainer(net, ds) #, learningrate = 0.001, momentum = 0.99)
    # trainer.trainUntilConvergence()

    for i in xrange(500):
        trainer.train()

    test = [[0, 0], [0, 1], [1, 0], [1, 1]]
    for e in test:
        res = net.activate(e)
        print(res)

def build_net2(learn_data):
    learn_data = sorted(learn_data, key=lambda x: x[1])
    keys = []
    groups = []
    for key, group in itertools.groupby(learn_data, lambda x: x[0]):
        print(key)
        keys.append(key)
        groups.append(list(group))

    #print(keys)

def build_net(nbytes, learn_data):
    #learn_data = sorted(learn_data, key=lambda x: x[1])
    #data_group = dict((key, list(group)) for key, group in itertools.groupby(learn_data, lambda x: x[0]))
    #keys = [key for key, group in data_group] #BUG ~ list comprehenson remove elements!!!
    #keys = map(lambda (key, group): key, data_group) # this TOO!!!

    #keys = data_group.keys()
    keys = []
    for item in learn_data:
        if item[0] not in keys:
            keys.append(item[0])

    net = buildNetwork(nbytes, len(keys), hiddenclass=LinearLayer)

    ds = ClassificationDataSet(nbytes, nb_classes=len(keys), class_labels=keys)

    for item in learn_data:
        #print([keys.index(item[0])])
        #ds.appendLinked([item[1]], [keys.index(item[0])])
        print(item[1])
        ds.appendLinked(item[1], [keys.index(item[0])])

    ds.calculateStatistics()
    ds._convertToOneOfMany(bounds=[0, 1])

    trainer = BackpropTrainer(net, verbose=True)
    trainer.setData(ds)

    #trainer.trainUntilConvergence(maxEpochs=1000)
    for i in xrange(4):
        trainer.train()

    return net

    #for key in data_group:
     #   print(key + ' ' + str(len(data_group[key])))
      #  for value in data_group[key]:
       #     print()
        #    #ds.appendLinked(value[0], [keys.index(value[1])])

def brain(net, data):
    keys = []
    for item in data:
        if item[0] not in keys:
            keys.append(item[0])

    for item in data:
        result = list(net.activate(item[1]))
        m = max(result)
        i = result.index(m)
        print('out: {0} is {1}, {2}'.format(m, keys[i], item[0]))

def read_file(nbytes, filename):
    buf = open(filename, 'r').read(nbytes)
    known_type = magic.from_buffer(buf, mime=True)
    #return known_type, buf
    return known_type, [ord(x) for x in buf]

def read_files(nbytes, folder):
    return map(lambda f: read_file(nbytes, folder + f), os.listdir(folder))

def main():
    nbytes = 128
    # test_xor_network() # do smthg
    learn_data = read_files(nbytes, './learn/')
    test_data = read_files(nbytes, './test/')
    net = build_net(nbytes, learn_data)

    brain(net, learn_data)
    #brain(net, test_data)

if __name__ == '__main__':
    main()
