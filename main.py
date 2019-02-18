from MyClass import *
from mytools import word_space

d = 10
kms = KMS(d)
broker = Broker()
requester = kms.KeyGen(broker, "100", False)
worker = kms.KeyGen(broker, str(id))

f_index = []

for i,w in enumerate(word_space):
    worker.IntEnc(w)
    print('index {}'.format(i))
    broker.IntTran(worker.id, worker.I_star)
    f_index.append(broker.I_tilde)

print('index construction complete')

while(True):
    q = input()
    Q = [q]
    requester.TdGen(Q)
    broker.TdTran(requester.id, requester.T)
    result = []
    for doc_id, I_tilde in enumerate(f_index):
        broker.I_tilde = I_tilde
        if broker.Match() == 1:
            result.append(doc_id)
            print(doc_id)
    print('len:{}'.format(len(result)))

