import multiprocessing
import time
import math


class Bacteria:
    def __init__(self, x, y, energy=100):
        self.x = x
        self.y = y
        self.energy = energy

    def update(self, target):
        distance = math.dist((self.x, self.y), target)
        time.sleep(1/60)
        self.energy -= 1
        return distance  # Возвращаем расстояние


def process_bacteria(bacteria, target):
    return bacteria.update(target)

def multi():
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        distances = pool.starmap(process_bacteria, [(b, target) for b in bacteria_list])
        
def single():
    return [x.update(target) for x in bacteria_list]

if __name__ == "__main__":
    num_bacteria = 200
    target = (100000, 100000)
    bacteria_list = [Bacteria(0,0) for _ in range(num_bacteria)]

    start_time = time.perf_counter()

    #g = multi()
    g = single()

    end_time = time.perf_counter()

    print(f"Время выполнения: {end_time - start_time:.4f} секунд")

