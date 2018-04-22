import random as rand
import numpy as np
import HoppingBird
import random
import sys # only for sys.maxsize

GENE_NUM = 4
INDIVISUAL_NUM = 20
GENERATION_NUM = 100

MUTATION_CHANCE = 0.02

class Gene():
    def __init__(self, val = None):
        self.val = val
        if val is None:
            self._rand()

    def _rand(self):
        self.val = [Gene.randGene() for g in range(GENE_NUM)]

    def evaluate(self, randSeed = None):
        random.seed(randSeed)
        show = False
        randSeed1 = random.randint(-sys.maxsize - 1, sys.maxsize)
        randSeed2 = random.randint(-sys.maxsize - 1, sys.maxsize)
        randSeed3 = random.randint(-sys.maxsize - 1, sys.maxsize)
        score1 = HoppingBird.main(randSeed1, self.calc, self.val, show)
        score2 = HoppingBird.main(randSeed2, self.calc, self.val, show)
        score3 = HoppingBird.main(randSeed3, self.calc, self.val, show)
        self.evaluationValue = (score1 + score2 + score3) / 3
        return self.evaluationValue

    def show(self, randSeed = None):
        random.seed(randSeed)
        randSeed1 = random.randint(-sys.maxsize - 1, sys.maxsize)
        HoppingBird.main(randSeed1, self.calc, self.val, True)

    def calc(self, environments, internals, show):
        envir = np.array(environments)
        inter = np.array(internals[:GENE_NUM:])

        if show:
            print(inter, ".", environments, "T =", inter.dot(envir))

        return inter.dot(envir) >= 0

    def randGene():
        return random.uniform(-1, 1)

    def __eq__(self, other):
        for i in range(GENE_NUM):
            if self.val[i] != other.val[i]:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

def printAll(generation, deme, toFile = True, toTerminal = True):
    if toFile:
        if generation == 0:
            f = open('out.txt', 'w')
        else:
            f = open('out.txt', 'a')
    if toTerminal:
        print(generation, "th generation")
    if toFile:
        f.write(str(generation) + "th generation\n")
    for i in range(INDIVISUAL_NUM):
        for g in range(GENE_NUM):
            if toTerminal:
                print('%04.4f' % deme[i].val[g], end = " ")
            if toFile:
                f.write('%04.4f' % deme[i].val[g])
                f.write(" ")
        if toTerminal:
            print('(%1.4f)' % deme[i].evaluationValue)
        if toFile:
            f.write('(%1.4f)\n' % deme[i].evaluationValue)
    if toTerminal:
        print()
    if toFile:
        f.write("\n")
        f.close()

def main():

    deme = [Gene() for i in range(INDIVISUAL_NUM)]

    randSeed = random.randint(-sys.maxsize - 1, sys.maxsize)
    for i in range(INDIVISUAL_NUM):
        deme[i].evaluate(randSeed)

    deme.sort(key = lambda x : x.evaluationValue, reverse = True)

    printAll(0, deme, toFile = True)

    for generation in range(1, GENERATION_NUM + 1):
        new_deme = []

        # step 1  choose 2 parents
        parents = deme[:2:]

        if parents[0] == parents[1]:
            for i in range(INDIVISUAL_NUM):
                if deme[i] != parents[0]:
                    parents[1] = deme[i]
                    break

        for i in range(2):
            new_deme.append(parents[i])

        # step 2  generate 8 children
        for i in range(INDIVISUAL_NUM - 2):
            new_genes = []
            for g in range(GENE_NUM):
                # step 2-1  crossover
                ratio = random.uniform(-0.3, 1.3)
                new_gene = parents[0].val[g] * ratio + parents[1].val[g] * (1.0 - ratio)
                # step 2-2  mutation
                if rand.random() < MUTATION_CHANCE:
                    ratio = random.uniform(-4.0, 5.0)
                    new_gene = parents[0].val[g] * ratio + parents[1].val[g] * (1.0 - ratio)

                new_genes.append(new_gene)
            new_indivisual = Gene(new_genes)

            new_deme.append(new_indivisual)

        # step 3  evaluate
        randSeed = random.randint(-sys.maxsize - 1, sys.maxsize)
        for i in range(INDIVISUAL_NUM):
            new_deme[i].evaluate(randSeed)

        random.shuffle(new_deme)
        new_deme.sort(key = lambda x : x.evaluationValue, reverse = True)

        # step 4  update
        deme = new_deme[::]
        
        # (step 5  print) 
        printAll(generation, deme, toFile = True)

        # (step 6  show)
        deme[0].show(randSeed)


    printAll(generation, deme, toFile = True)


if __name__ == '__main__':
    main()