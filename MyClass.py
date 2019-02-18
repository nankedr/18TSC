import itertools
from sympy import *
import random
from mytools import hs, P
import numpy as np

class Worker:
    def __init__(self, id, A1, B1, d, S):
        self.id = id
        self.d = d
        self.S = S
        self.A1 = A1
        self.B1 = B1
        self.I_star = []
        self.I_ab = []
        self.I = []

    def IntEnc(self, I):
        self.I = []
        self.I_ab = []
        self.I_star = []

        for w in I:
            templist = []
            for i in range(0, self.d + 1):
                templist.append((hs(w) ** i))
            self.I.append(templist)
            I_a = Matrix(np.ones((self.d + 1, 1)))
            I_b = Matrix(np.ones((self.d + 1, 1)))
            for i in range(0, self.d + 1):
                if self.S[i] == 0:
                    I_a[i] = templist[i]
                    I_b[i] = templist[i]
                else:
                    I_a[i] = random.randint(*sorted([0, templist[i]]))
                    #I_a[i] = random.uniform(*sorted([0, templist[i]]))
                    I_b[i] = templist[i] - I_a[i]
            self.I_ab.append([I_a, I_b])
            self.I_star.append([self.A1.T*I_a, self.B1.T*I_b])


class Broker:
    def __init__(self):
        self.rk = dict()

    def addRK(self, id, rk):
        self.rk[id] = rk

    def IntTran(self, id, I_star):
        A2, B2 = self.rk[id]
        self.I_tilde = [[A2.T * item1, B2.T * item2] for item1, item2 in I_star]

    def TdTran(self, id, T):
        A2, B2 = self.rk[id]
        self.T_tilde =  [(A2**-1) * T[0], (B2**-1) * T[1]]

    def Match(self):
        for I_j in self.I_tilde:
            temp = self.T_tilde[0].T*I_j[0] + self.T_tilde[1].T*I_j[1]
            # print(temp)
            if temp[0,0] == 0:
                return 1
        return 0


class Requester:
    def __init__(self, id, A1, B1, d, S):
        self.d = d
        self.S = S
        self.id = id
        self.A1 = A1
        self.B1 = B1
        self.T = None
        self.Q_vector = None
        self.Q_ab = []

    def TdGen(self, Q):
        l = self.d-len(Q)
        Q = Q + ['eeee']*l
        H_Q_list = [-hs(i) for i in Q]
        Q_vector = [self.coff(H_Q_list, i) for i in range(self.d, 0, -1)]+[1]
        self.Q_vector = Q_vector
        Q_vector_a = Matrix(np.ones((self.d + 1, 1)))
        Q_vector_b = Matrix(np.ones((self.d + 1, 1)))
        for k,i in enumerate(self.S):
            if i == 0:
                Q_vector_a[k] = random.randint(*sorted([0, Q_vector[k]]))
                #Q_vector_a[k] = random.uniform(*sorted([0, Q_vector[k]]))
                Q_vector_b[k] = Q_vector[k] - Q_vector_a[k]
            else:
                Q_vector_a[k] = Q_vector[k]
                Q_vector_b[k] = Q_vector[k]
        self.T = [(self.A1**-1)*Q_vector_a, (self.B1**-1)*Q_vector_b]
        self.Q_ab = [Q_vector_a, Q_vector_b]

    def coff(self, list, i):
        result = 0
        for item in itertools.combinations(list, i):
            temp = 1
            for i_item in item:
                temp *= i_item
            result += temp
        return result


class KMS:
    def __init__(self, d):
        # Setup
        self.d = d
        self.S = np.random.randint(0, 2, size=d+1)
        self.M1 = Matrix(np.random.randint(0, 100, (d + 1, d + 1)))
        self.M2 = Matrix(np.random.randint(0, 100, (d + 1, d + 1)))

    def KeyGen(self, broker, id, worker=True):
        A1 = Matrix(np.random.randint(0, 100, (self.d + 1, self.d + 1)))
        B1 = Matrix(np.random.randint(0, 100, (self.d + 1, self.d + 1)))
        A2 = (A1**-1) * self.M1
        B2 = (B1**-1) * self.M2
        broker.addRK(id, [A2, B2])

        if worker:
            return Worker(id, A1, B1, self.d, self.S)
        else:
            return Requester(id, A1, B1, self.d, self.S)


if __name__ == '__main__':
    kms = KMS(6)
    print(kms.S)
