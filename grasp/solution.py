from math import inf

class Solution(list):
    def __init__(self):
        super().__init__()
        self.cost = inf

    def __str__(self):
        return (f"Solution: cost=[{self.cost}], size=[{len(self)}], elements="
                + super().__str__())

    def copy(self,):
        new = super().copy()
        new.cost = self.cost
        return new
