import random
import time
from collections import OrderedDict

# LRU-кеш на основі OrderedDict
class LRUCache:
    def __init__(self, capacity=1000):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            # Move to end to mark as recently used
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

# --- Функції без кешу ---
def range_sum_no_cache(array, left, right):
    return sum(array[left:right+1])

def update_no_cache(array, index, value):
    array[index] = value

# --- Функції з кешем ---
def range_sum_with_cache(array, left, right, cache):
    key = (left, right)
    result = cache.get(key)
    if result != -1:
        return result
    result = sum(array[left:right+1])
    cache.put(key, result)
    return result

def update_with_cache(array, index, value, cache):
    array[index] = value
    keys_to_delete = [key for key in cache.cache if key[0] <= index <= key[1]]
    for key in keys_to_delete:
        del cache.cache[key]

# --- Генерація запитів ---
def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, n//2), random.randint(n//2, n-1)) for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        if random.random() < p_update:
            idx = random.randint(0, n-1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:
            if random.random() < p_hot:
                left, right = random.choice(hot)
            else:
                left = random.randint(0, n-1)
                right = random.randint(left, n-1)
            queries.append(("Range", left, right))
    return queries

# --- Основна функція для вимірювання часу ---
def run_benchmark():
    n = 100_000
    q = 50_000
    array1 = [random.randint(1, 100) for _ in range(n)]
    array2 = list(array1)  # Копія для кешованої версії
    queries = make_queries(n, q)

    # --- Без кешу ---
    start = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_no_cache(array1, query[1], query[2])
        else:
            update_no_cache(array1, query[1], query[2])
    time_no_cache = time.time() - start

    # --- З кешем ---
    cache = LRUCache(capacity=1000)
    start = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_with_cache(array2, query[1], query[2], cache)
        else:
            update_with_cache(array2, query[1], query[2], cache)
    time_with_cache = time.time() - start

    # --- Результат ---
    speedup = time_no_cache / time_with_cache
    print(f"Без кешу : {time_no_cache:.2f} c")
    print(f"LRU-кеш  : {time_with_cache:.2f} c  (прискорення ×{speedup:.1f})")

# --- Запуск ---
if __name__ == "__main__":
    run_benchmark()
