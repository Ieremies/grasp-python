from qbf import QBF

class QBFInverse(QBF):

    def evaluate_qbf(self,) -> float:
        return -super().evaluate_qbf()

    def evaluate_insertion_qbf(self, elem: int) -> float:
        return -super().evaluate_insertion_qbf(elem)

    def evaluate_removal_qbf(self, elem: int) -> float:
        return -super().evaluate_removal_qbf(elem)

    def evaluate_exchange_qbf(self, elem_in: int, elem_out: int) -> float:
        return -super().evaluate_exchange_qbf(elem_in, elem_out)
