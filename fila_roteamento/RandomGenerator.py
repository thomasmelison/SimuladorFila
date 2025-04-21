class RandomGenerator:

    def __init__(self, numero_inicial, a, c, M, limit):
        self.last_random = numero_inicial
        self.a  = a
        self.c = c
        self.M = M
        self.counter = limit
        
    
    def generate_next_random(self) -> float:

        self.counter -= 1

        self.last_random  = ( ( self.a * self.last_random  ) + self.c) % self.M
        self.last_random = self.last_random  / self.M
        return self.last_random
    
    def get_counter(self):
        return self.counter
    
    def is_next_random_less_than(self, number: float):
        self.last_random = self.generate_next_random()

        return self.last_random < number

