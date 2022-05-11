from abc import ABC, abstractmethod

from grasp.solution import Solution


class Evaluator(ABC):

    @abstractmethod
    def get_domain_size(self,) -> int:
        ...

    @abstractmethod
    def evaluate(self,) -> float:
        ...

    @abstractmethod
    def evaluate_insertion_cost(self, elem, sol: Solution) -> float:
        ...

    @abstractmethod
    def evaluate_removal_cost(self, elem, sol: Solution) -> float:
        ...

    @abstractmethod
    def evaluate_exchange_cost(self, elem_in, elem_out, sol: Solution) -> float:
        ...


