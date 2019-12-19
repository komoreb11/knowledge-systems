import condabin.numpy as np
from pip._vendor.distlib.compat import raw_input


# Activation function


def tanh(x, deriv=False):
    if (deriv):
        return 1.0 - x ** 2
    x = (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))
    return x


def softmax(x, deriv=False):
    if (deriv):
        return sft1(x) * (1 - sft1(x))
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)


def sft1(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)


class NeuralNetwork:
    def __init__(self, x):
        self.input = x
        self.weights1 = np.array([[0.23556518, 0.80521703, -0.28971042, -0.67995189, -0.48688482,
                                   -0.26440022, -0.87632231, -0.31096518],
                                  [-0.12089921, 0.32494253, -0.68341555, 0.24339296, 0.06166721,
                                   -0.75765378, 0.09553982, 0.07559536],
                                  [-0.83208289, -0.14894517, -0.61907216, -0.88387715, 0.61586818,
                                   -0.25202303, -0.33550021, -0.84173294],
                                  [0.59125894, 0.28025633, -0.46163711, 1.52950997, -1.11124881,
                                   -0.51783961, -0.22791007, 0.01500646],
                                  [-0.69952792, -0.14187593, 0.49575943, 0.85363185, 0.71711286,
                                   -0.23800173, -0.73878018, -0.68123654],
                                  [0.54677218, 0.5261382, -0.68057551, -0.64403965, 0.79198803,
                                   -0.39591843, 0.0795971, -0.10092175],
                                  [1.04668741, -0.35749225, -0.47932837, 0.26433265, 0.73146445,
                                   0.01738951, 0.00231316, -0.41891027],
                                  [-0.03737221, 0.20014172, 0.03477527, 0.61237706, -0.38313868,
                                   -0.39354901, -0.70692312, 0.79764411],
                                  [-0.50021338, 0.6511965, -0.85122963, -0.26760447, -0.47037537,
                                   -0.758329, -1.08634094, -0.85698199],
                                  [-0.37466693, -1.14502956, -0.79824017, 0.91586794, 0.55096913,
                                   0.01271699, -1.05859305, -0.45239589],
                                  [-0.23080001, -0.92319842, 0.33693458, -0.83846834, -0.64652209,
                                   0.06951108, 0.66792173, -0.11701283],
                                  [1.06254317, -0.51958093, 0.28062235, -0.20996614, 0.19403119,
                                   -0.51342757, 1.02154503, 1.04611798],
                                  [-0.29562659, 0.33956952, -0.37722035, 0.27653717, 0.10215048,
                                   0.76256054, -0.68899951, 0.35753194],
                                  [0.23803624, -0.41381133, -0.4745151, 0.53731409, 0.11464867,
                                   0.52081832, 0.24758254, 0.25541631],
                                  [-0.81059097, 1.19445517, 0.02996238, 0.05466618, 0.85278757,
                                   0.73691802, 0.4892346, -0.38519036],
                                  [-1.04644068, -0.96057088, -0.12883296, -1.15721048, -0.29148701,
                                   0.68282709, -1.05250161, -1.13238851]])
        self.weights2 = np.array([[0.50968767, 0.63222487],
                                  [-1.45136138, -1.67107257],
                                  [0.90182914, -0.01348864],
                                  [0.67274524, 2.39786487],
                                  [-0.63254398, -0.79444244],
                                  [0.04059063, -0.34379334],
                                  [1.61585243, 0.76711352],
                                  [0.41277576, 0.86221053]])
        self.sft = np.array([[-1.84997505],
                             [1.85089163]])

    def feedforward(self):
        self.layer1 = tanh(np.dot(self.input, self.weights1))
        self.layer2 = tanh(np.dot(self.layer1, self.weights2))
        self.eval = tanh(np.dot(self.layer2, self.sft))
        return self.eval


class Inference():
    def __init__(self, x):
        self.ss = x
    def delej(self):
        if self.ss[3] > 0.5 and self.ss[10] and self.ss[7] <= 0.5 and self.ss[2] > 0.5:
            print(1)
        elif self.ss[3] > 0.5 and self.ss[10] > 0.5 and self.ss[14] <= 0.5 and self.ss[9] > 0.5:
            print(0)
        elif self.ss[3] > 0.5 and self.ss[10] <= 0.5 and self.ss[9] <= 0.5 and self.ss[0] <= 0.5 and self.ss[2] <= 0.5:
            print(0)
        elif self.ss[3] > 0.5 and self.ss[10] <= 0.5 and self.ss[9] <= 0.5 and self.ss[0] <= 0.5 and self.ss[2] > 0.5 and self.ss[11] > 0.5:
            print(0)
        elif self.ss[3] > 0.5 and self.ss[10] <= 0.5 and self.ss[9] <= 0.5 and self.ss[0] > 0.5 and self.ss[11] > 0.5:
            print(0)
        elif self.ss[3] > 0.5 and self.ss[10] <= 0.5 and self.ss[9] <= 0.5 and self.ss[0] > 0.5 and self.ss[11] <= 0.5 and self.ss[13] > 0.5:
            print(0)
        else:
            if(self.ss[0] <= 0.5):
                print(1)
            else:
                print(0)



def main():
    print("input 16 values")
    ss = []
    for i in range(16):
        ss.append(float(input("Element:")))
    ss = np.array(ss)
    g = int(raw_input("Choose the way, put 1 for inference, 2 for neural network"))
    if (g == 1):
        print("inference selected")
        Inference(ss)
    else:
        print("Creating neural network 16-8-2-1")


        NN = NeuralNetwork(ss)
        kk = []
        for i in NN.feedforward():
            kk.append(np.round(i).astype(int))
        ll = []
        for j in kk:
            ll.append(j[0])
        print(ll)
    return True

if __name__ == "__main__":
  main()