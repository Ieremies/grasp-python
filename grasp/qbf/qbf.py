from grasp.evaluator import Evaluator
from grasp.solution import Solution

class QBF(Evaluator):
    def __init__(self, filename: str):
        self.size = self.read_input(filename)
        self.variables = [0.0 for _ in range(self.size)]

    def set_variables(self, sol: Solution):
        self.reset_variables()

        for elem in sol:
            self.variables[elem] = 1.0

    def get_domain_size(self) -> int:
        return self.size

    def evaluate(self, sol: Solution) -> float:
        self.set_variables(sol)
        sol.cost = self.evaluate_qbf()
        return sol.cost

    def evaluate_qbf(self,) -> float:
        result = 0
        for i in range(self.size):
            aux = 0
            for j in range(self.size):
                aux += self.variables[j] * self.coef_a[i][j]
            result += aux * self.variables[i]
        return result

    def evaluate_insertion_cost(self, elem, sol: Solution) -> float:
        self.set_variables(sol)
        return self.evaluate_insertion_qbf(elem)

    def evaluate_insertion_qbf(self, elem: int) -> float:
        if self.variables[elem] == 1:
            return 0
        return self.evaluate_contribution_qbf(elem)

    def evaluate_removal_cost(self, elem, sol: Solution) -> float:
        self.set_variables(sol)
        return self.evaluate_removal_qbf(elem)

    def evaluate_removal_qbf(self, elem: int) -> float:
        if self.variables[elem] == 1:
            return 0

        return -self.evaluate_contribution_qbf(elem)

    def evaluate_exchange_cost(self, elem_in, elem_out, sol: Solution) -> float:
        self.set_variables(sol)
        return self.evaluate_exchange_qbf(elem_in, elem_out)

    def evaluate_exchange_qbf(self, elem_in: int, elem_out: int) -> float:
        if elem_in == elem_out:
            return 0.0
        if self.variables[elem_in] == 1:
            return self.evaluate_removal_qbf(elem_out)
        if self.variables[elem_out] == 0:
            return self.evaluate_insertion_qbf(elem_in)

        result = self.evaluate_contribution_qbf(elem_in)
        result -= self.evaluate_contribution_qbf(elem_out)
        result -= (self.coef_a[elem_in][elem_out] + self.coef_a[elem_out][elem_in])

        return result

    def evaluate_contribution_qbf(self, i: int) -> float:
        result = 0
        for j in range(self.size):
            if j != i:
                result += self.variables[j] * (self.coef_a[i][j] + self.coef_a[j][i])
        result += self.coef_a[i][i]
        return result

    def read_input(self, file_name: str) -> int:
        with open(file_name, "r", encoding="utf-8") as fd:
            size = int(fd.readline())
            self.coef_a = []
            for i in range(size):
                line = [0 for j in range(i)]
                line += [int(x) for x in fd.readline().split()]
                self.coef_a.append(line)
        return size

    def reset_variables(self):
        self.variables = [0.0 for _ in range(self.size)]

    def print_matrix(self):
        for i in range(len(self.coef_a)):
            for j in range(len(self.coef_a)):
                print(self.coef_a[i][j], end=" ")
            print()
