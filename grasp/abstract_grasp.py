from abc import ABC, abstractmethod
from math import inf
from random import choice
from typing import Iterable
from datetime import datetime

from grasp.evaluator import Evaluator
from grasp.solution import Solution


class GRASP(ABC):
    verbose = True
    rng = choice
    sol = Solution()

    @abstractmethod
    def make_cl(self,) -> Iterable:
        ...

    @abstractmethod
    def make_rcl(self,) -> Iterable:
        ...

    @abstractmethod
    def update_cl(self,):
        ...

    @abstractmethod
    def create_empty_sol(self,) -> Solution:
        ...

    @abstractmethod
    def local_search(self,) -> Solution:
        ...

    def __init__(self, obj_function: Evaluator, alpha: float, iterations: int):
        self.obj_function = obj_function
        self.alpha = alpha
        self.iterations = iterations


    def contructive_heuristic(self,) -> Solution:
        cl = self.make_cl()
        rcl = self.make_rcl()
        sol = self.create_empty_sol()
        cost = inf

        while cost >= sol.cost:
            max_cost = -inf
            min_cost = inf
            cost = self.obj_function.evaluate(sol)
            self.update_cl()

            # Explore all candidate elements to enter the solution, saving the
            # highest and lowest cost variation achieved by the candidates.
            def eva(k):
                return self.obj_function.evaluate_insertion_cost(k, sol)
            min_cost = min(cl, key=eva)
            max_cost = max(cl, key=eva)

            # Among all candidates, insert into the RCL those with the highest
            # performance using parameter alpha as threshold.

            threshold = min_cost + self.alpha * (max_cost - min_cost)
            rcl = [cand for cand in cl if eva(cand) <= threshold ]

            # Choose a candidate randomly from the RCL
            in_cand = self.rng(rcl) # fix random
            cl.remove(in_cand)
            sol.append(in_cand)
            self.obj_function.evaluate(sol)
            rcl.clear()
        return sol

    def solve(self,) -> Solution:
        best_sol = self.create_empty_sol()
        for i in range(self.iterations):
            start = datetime.now()
            self.sol = self.contructive_heuristic()
            #print(f"{i} heu -> {round((datetime.now() - start).total_seconds(),3)}")
            start = datetime.now()
            self.local_search()
            #print(f"{i} loc -> {round((datetime.now() - start).total_seconds(),3)}")
            if best_sol.cost > self.sol.cost:
                best_sol = self.sol
                if self.verbose:
                    print(f"(Iter. {i}) BestSol =", best_sol)

        return best_sol
