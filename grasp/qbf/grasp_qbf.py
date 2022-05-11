from datetime import datetime
from math import inf
from sys import argv

from qbf_inverse import QBFInverse

from grasp.abstract_grasp import GRASP
from grasp.solution import Solution


class GRASP_QBF(GRASP):
    def __init__(self, alpha: float, iterations: int, filename: str):
        super().__init__(QBFInverse(filename), alpha, iterations)


    def make_cl(self,) -> list[int]:
        cl = []
        for i in range(self.obj_function.get_domain_size()):
            cl.append(i)
        return cl

    def make_rcl(self,) -> list[int]:
        rcl = []
        return rcl

    def update_cl(self,):
        pass

    def create_empty_sol(self,) -> Solution:
        return Solution()

    def local_search(self,):
        #print("sol >>", self.sol)
        cl = self.make_cl()
        best_cand_in = None
        best_cand_out = None
        while True:
            min_delta_cost = inf
            self.update_cl()

            # Evaluate insertions
            for cand_in in cl:
                delta_cost = self.obj_function.evaluate_insertion_cost(cand_in, self.sol)
                if delta_cost < min_delta_cost:
                    #print(f"inserti; ( ,{cand_in}); {delta_cost}")
                    min_delta_cost = delta_cost
                    best_cand_in = cand_in
                    best_cand_out = None

            # Evaluate removals
            for cand_out in self.sol:
                delta_cost = self.obj_function.evaluate_removal_cost(cand_out, self.sol)
                if delta_cost < min_delta_cost:
                    #print(f"removal; ( ,{cand_out}); {delta_cost}")
                    min_delta_cost = delta_cost
                    best_cand_in = None
                    best_cand_out = cand_out

            # Evaluate exchanges
            for cand_in in cl:
                for cand_out in self.sol:
                    #delta_cost = self.obj_function.evaluate_exchange_cost(cand_in, cand_out, self.sol)
                    if delta_cost < min_delta_cost:
                        print(f"exchange; ({cand_in},{cand_out}); {delta_cost}")
                        min_delta_cost = delta_cost
                        best_cand_in = cand_in
                        best_cand_out = cand_out

            # Implement the best move, if it reduces the solution cost
            # Otherwise, we are done.
            if min_delta_cost != -inf:
                #print(f"local >{cl}, in: {best_cand_in}, out: {best_cand_out}, delta: {min_delta_cost}")
                if best_cand_out is not None:
                    self.sol.remove(best_cand_out)
                    cl.append(best_cand_out)
                if best_cand_in is not None:
                    self.sol.append(best_cand_in)
                    cl.remove(best_cand_in)
                self.obj_function.evaluate(self.sol)
            if min_delta_cost == 0:
                break

if __name__ == "__main__":
    start_time = datetime.now()
    grasp = GRASP_QBF(alpha=float(argv[1]), iterations=int(argv[2]), filename=argv[3])
    best_sol = grasp.solve()
    print(f"maxVal = {best_sol}")
    end_time = datetime.now()
    print(f"time = {(end_time - start_time)} seg.")
