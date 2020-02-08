import os, sys
import copy
lib_path = os.path.abspath(os.path.join('.'))
sys.path.append(lib_path)

import random
import numpy as np
import joblib
import time

from utils.input import WusnInput
from constructor.binary import Layer
from constructor.nrk import Nrk
from utils.logger import init_log

N_GENS = 100
POP_SIZE = 300
CXPB = 0.8
MUTPB = 0.2
TERMINATE = 30

def init_individual(num_of_relays, num_of_sensors):
    length = 2 * (num_of_sensors + num_of_relays + 1)

    individual = list(np.random.uniform(0, 1, size=(length,)))

    return individual

def run_ga(fns, flog, logger=None):
    if logger is None:
        raise Exception("Error: logger is None!")

    # logger.info("Start!")
    num_of_relays = 14
    max_hop = 8

    num_tasks = len(fns)
    inputs = []
    constructors = []
    for fn in fns:
        inputs.append(WusnInput.from_file(fn))
        if 'layer' in fn:
            constructors.append(Nrk(inputs[-1], max_relay=num_of_relays, is_hop=False, hop=1000))
        else:
            constructors.append(Nrk(inputs[-1], max_relay=num_of_relays, is_hop=True, hop=max_hop))

    num_of_relays = max([inp.num_of_relays for inp in inputs])
    num_of_sensors = max([inp.num_of_sensors for inp in inputs])

    def transform_genes(individual, task_sensors):
        first_half = individual[:1 + num_of_relays + task_sensors]
        second_half = individual[1 + num_of_relays + num_of_sensors:2 + 2*num_of_relays + num_of_sensors + task_sensors]

        return first_half + second_half

    def factorial_rank(pop):
        factorial_cost = [[constructor.get_loss(transform_genes(indi, inp.num_of_sensors)) for constructor, inp in zip(constructors, inputs)] for indi in pop]

        ranks = []
        for task in range(num_tasks):
            rank = zip(np.argsort([tmp[task] for tmp in factorial_cost]), range(len(pop)))
            rank = [tmp[-1] for tmp in sorted(rank, key=lambda x: x[0])]
            ranks.append(rank)

        return ranks

    def skill_factor(pop):
        pop_factorial_rank = factorial_rank(pop)

        pop_skill_factor = [np.argmax([pop_factorial_rank[task][i] for task in range(num_tasks)]) for i in range(len(pop))]

        pop_scalar_fitness = [1/(min([pop_factorial_rank[task][i] for task in range(num_tasks)]) + 1) for i in range(len(pop))]

        # factorial rank << -> scalar fitness >> 
        return pop_skill_factor, pop_scalar_fitness

    def crossover(ind1, ind2, indpb=0.2):
        r1, r2 = np.random.randint(0, len(ind1)), np.random.randint(0, len(ind1))
        r1, r2 = min(r1, r2), max(r1, r2)
        
        ind1[:r1], ind2[:r1] = ind2[:r1], ind1[:r1]
        ind1[r2:], ind2[r2:] = ind2[r2:], ind1[r2:]

        avg = [(tmp1 + tmp2)/2 for tmp1, tmp2 in zip(ind1[r1:r2], ind2[r1:r2])]
        ind1[r1:r2], ind2[r1:r2] = avg, avg

        return ind1, ind2

    def mutate(ind, mu=0, sigma=0.2, indpb=1):
        size = len(ind)

        for i in range(size):
            if np.random.random() < indpb:
                ind[i] += random.gauss(mu, sigma)

        return ind

    def assortive_mating(pop, pop_skill_factor):
        offsprings = []
        for _ in range(POP_SIZE//2):
            idx1, idx2 = np.random.randint(0, POP_SIZE - 1), np.random.randint(0, POP_SIZE - 1)
            p1, p2 = copy.deepcopy(pop[idx1]), copy.deepcopy(pop[idx2])

            if pop_skill_factor[idx1] == pop_skill_factor[idx2] and np.random.random() < CXPB:
                offs1, offs2 = crossover(p1, p2)
                offsprings.extend([offs1, offs2])
            else:
                offs1, offs2 = mutate(p1), mutate(p2)
                offsprings.extend([offs1, offs2])

        return offsprings

    def selection(pop, pop_skill_factor, pop_scalar_fitness):
        ranking = sorted([(idx, value) for idx, value in enumerate(pop_scalar_fitness)], key=lambda x: -x[-1])
        new_pop, new_pop_skill_factor = [], []

        for i in range(POP_SIZE):
            new_pop.append(pop[ranking[i][0]])
            new_pop_skill_factor.append(pop_skill_factor[ranking[i][0]])

        return new_pop, new_pop_skill_factor

    num_of_relays = max([inp.num_of_relays for inp in inputs])
    num_of_sensors = max([inp.num_of_sensors for inp in inputs])

    pop = [init_individual(num_of_relays, num_of_sensors) for _ in range(POP_SIZE)]

    pop_skill_factor, _ = skill_factor(pop)

    offspring_pop = assortive_mating(pop, pop_skill_factor)

    hop_individual, layer_individual = None, None


    for g in range(N_GENS):
        flog.write(f'GEN {g} time {int(time.time())}\n')

        offspring_pop = assortive_mating(pop, pop_skill_factor)
        
        immediate_pop = pop + offspring_pop
        
        pop_skill_factor, pop_scalar_fitness = skill_factor(immediate_pop)

        pop, pop_skill_factor = selection(immediate_pop, pop_skill_factor, pop_scalar_fitness)

        best_indis = [None] * num_tasks
        for i in range(num_tasks):
            for j in range(POP_SIZE):
                if pop_skill_factor[j] == i:
                    best_indis[i] = pop[j]
                    break

        best_objs = [constructor.get_loss(transform_genes(indi, inp.num_of_sensors)) \
            for indi, constructor, inp in zip(best_indis, constructors, inputs)]
        # infos = [constructor.decode_genes(transform_genes(indi, inp.num_of_sensors)) \
        #     for indi, constructor, inp in zip(best_indis, constructors, inputs)]

        for task in range(num_tasks):
            flog.write(f'{best_objs[task]}\n')

def solve(fns, pas=1, logger=None, hop_dir='./data/hop', layer_dir='./data/layer'):
    print(f'solving {fns} pas {pas}')

    # inps = [WusnInput.from_file(tmp) for tmp in fns]

    # logger.info(f"prepare input data from path {hop_path} and {layer_path}")
    # logger.info("num generation: %s" % N_GENS)
    # logger.info("population size: %s" % POP_SIZE)
    # logger.info("crossover probability: %s" % CXPB)
    # logger.info("mutation probability: %s" % MUTPB)
    # logger.info("run GA....")

    flog = open(f"results/mfea/{fns[1].split('/')[-1][:-5]}_{pas}.txt", 'w+')

    flog.write(f'{fns}\n')

    run_ga(fns, flog, logger)
    print(f'done solved {fns[1]}')
    

if __name__ == '__main__':
    logger = init_log()
    os.makedirs('results/mfea', exist_ok=True)
    hop_dir = './data/hop'
    layer_dir = './data/layer'

    # for i in range(10):
    #     joblib.Parallel(n_jobs=8)(
    #         joblib.delayed(solve)(fn, pas=i, logger=logger) for fn in sorted(os.listdir(hop_dir))
    #     )

    rerun = set([tmp.replace('\n', '') for tmp in open('mfea_tests.txt', 'r').readlines()])

    hop_dir='./data/hop'
    layer_dir='./data/layer'
    pases = []
    tests = []
    # 1 single 3 multi
    for i in range(10):
        rerun_hop = [tmp for tmp in os.listdir(hop_dir) if f'{tmp[:-5]}_{i}.txt' in rerun]
        sets = []
        for j in rerun_hop:
            single = '_'.join(j.split('_')[:-1]) + '.json'

            r = int(j.split('_')[-3][1:])
            ss = int(j.split('_')[-1][:-5])

            splt = j.split('_')
            splt[-1] = str(40-ss) + '.json'
            multi2 = '_'.join(splt)
            
            splt[-1] = str(ss) + '.json'
            splt[-3] = 'r' + str(75-r)
            multi3 = '_'.join(splt)
            
            single = os.path.join(layer_dir, single)
            multi1 = os.path.join(hop_dir, j)
            multi2 = os.path.join(hop_dir, multi2)
            multi3 = os.path.join(hop_dir, multi3)
            tests.append([single, multi1, multi2, multi3])

        pases = pases + [i] * len(rerun_hop)

    # tests = tests[:1]
    joblib.Parallel(n_jobs=8)(
        joblib.delayed(solve)(fn, pas=pas, logger=logger) for fn, pas in zip(tests, pases)
    )
