import random
import time

# Реалізація LRU-кешу
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.list.move_to_front(node)
            return node.data[1]
        return -1

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.data = (key, value)
            self.list.move_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                last = self.list.remove_last()
                if last:
                    del self.cache[last.data[0]]
            new_node = self.list.push(key, value)
            self.cache[key] = new_node


# Функції без кешу
def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value


# Функції з кешем
class CachedArray:
    def __init__(self, array, cache_size):
        self.array = array
        self.cache = LRUCache(cache_size)

    def range_sum_with_cache(self, L, R):
        key = (L, R)
        cached_result = self.cache.get(key)
        if cached_result is not None:
            return cached_result

        # Обчислюємо суму та додаємо в кеш
        result = sum(self.array[L:R+1])
        self.cache.put(key, result)
        return result

    def update_with_cache(self, index, value):
        self.array[index] = value
        # Видаляємо всі записи в кеші, оскільки вони можуть бути неактуальними
        keys_to_remove = [key for key in self.cache.cache if key[0] <= index <= key[1]]
        for key in keys_to_remove:
            del self.cache.cache[key]


# Тестування
if __name__ == "__main__":
    N = 100_000
    Q = 50_000
    K = 1000

    # Генеруємо масив та список запитів
    array = [random.randint(1, 100) for _ in range(N)]
    queries = []
    for _ in range(Q):
        if random.random() < 0.7:  # 70% запитів - Range, 30% - Update
            L = random.randint(0, N - 1)
            R = random.randint(L, N - 1)
            queries.append(("Range", L, R))
        else:
            index = random.randint(0, N - 1)
            value = random.randint(1, 100)
            queries.append(("Update", index, value))

    # Тестування без кешу
    start_time = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_no_cache(array, query[1], query[2])
        elif query[0] == "Update":
            update_no_cache(array, query[1], query[2])
    no_cache_time = time.time() - start_time

    # Тестування з кешем
    cached_array = CachedArray(array, K)
    start_time = time.time()
    for query in queries:
        if query[0] == "Range":
            cached_array.range_sum_with_cache(query[1], query[2])
        elif query[0] == "Update":
            cached_array.update_with_cache(query[1], query[2])
    cache_time = time.time() - start_time

    # Результати
    print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")
    print(f"Час виконання з LRU-кешем: {cache_time:.2f} секунд")