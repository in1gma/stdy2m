#!/usr/bin/python

import os
import binascii
# xor example test
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
from pybrain.structure import TanhLayer

def test_xor_network():
    net = buildNetwork(2, 2, 1, bias=True, hiddenclass=TanhLayer)

    ds = SupervisedDataSet(2, 1)
    data = [
        [(0,0), (0,)],
        [(0,1), (1,)],
        [(1,0), (1,)],
        [(1,1), (0,)],
    ]

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

def read_files():
    result = {}
    folder = './test/'
    bytes = 3 # 2 ~ 4
    for filename in os.listdir(folder):
        file = open(folder + filename, 'r')
        signature = file.read(bytes)
        file.close()
        hex_signature = binascii.hexlify(signature)
        # print('{0} {1} {2}'.format(filename, signature, hex_signature))
        result[filename] = hex_signature
    return result

def main():
    # test_xor_network() # do smthg
    test = read_files()
    print(test)

if __name__ == '__main__':
    main()
