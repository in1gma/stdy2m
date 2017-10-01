#!/usr/bin/python

# xor example test
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet
from pybrain.structure import TanhLayer

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

