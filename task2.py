import timeit
from functools import lru_cache
import matplotlib.pyplot as plt

# Реалізація Splay Tree
class Node:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left_node = None
        self.right_node = None

class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        """Вставка нового елемента у дерево."""
        if self.root is None:
            self.root = Node(key, value)
        else:
            self._insert_node(key, value, self.root)

    def _insert_node(self, key, value, current_node):
        """Рекурсивна вставка елемента в дерево."""
        if key < current_node.key:
            if current_node.left_node:
                self._insert_node(key, value, current_node.left_node)
            else:
                current_node.left_node = Node(key, value, current_node)
        else:
            if current_node.right_node:
                self._insert_node(key, value, current_node.right_node)
            else:
                current_node.right_node = Node(key, value, current_node)

    def search(self, key):
        """Пошук значення за ключем у дереві."""
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left_node
            elif key > node.key:
                node = node.right_node
            else:
                self._splay(node)
                return node.value  # Повертаємо знайдене значення
        return None  # Якщо елемент не знайдено

    def _splay(self, node):
        """Сплаювання вузла."""
        while node.parent is not None:
            if node.parent.parent is None:  # Zig
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node == node.parent.left_node and node.parent == node.parent.parent.left_node:  # Zig-Zig
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.right_node and node.parent == node.parent.parent.right_node:  # Zig-Zig
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            else:  # Zig-Zag
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                    self._rotate_left(node.parent)
                else:
                    self._rotate_left(node.parent)
                    self._rotate_right(node.parent)

    def _rotate_right(self, node):
        """Права ротація вузла."""
        left_child = node.left_node
        if left_child is None:
            return
        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child
        left_child.right_node = node
        node.parent = left_child

    def _rotate_left(self, node):
        """Ліва ротація вузла."""
        right_child = node.right_node
        if right_child is None:
            return
        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child
        right_child.left_node = node
        node.parent = right_child


# Реалізація функції з використанням Splay Tree
def fibonacci_splay(n, tree):
    cached = tree.search(n)
    if cached is not None:
        return cached
    if n <= 1:
        result = n
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result


# Реалізація функції з використанням LRU-кешу
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


# Вимірювання часу виконання
n_values = list(range(0, 951, 50))
lru_times = []
splay_times = []

for n in n_values:
    # Час для LRU-кешу
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=10) / 10
    lru_times.append(lru_time)

    # Час для Splay Tree
    splay_tree = SplayTree()
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, splay_tree), number=10) / 10
    splay_times.append(splay_time)

# Побудова графіка
plt.figure(figsize=(10, 6))
plt.plot(n_values, lru_times, label='LRU Cache', marker='o')
plt.plot(n_values, splay_times, label='Splay Tree', marker='s')
plt.xlabel('n (Fibonacci Number Index)')
plt.ylabel('Execution Time (s)')
plt.title('Performance Comparison: LRU Cache vs Splay Tree')
plt.legend()
plt.grid(True)
plt.show()

# Виведення таблиці
print(f"{'n':<10}{'LRU Cache Time (s)':<20}{'Splay Tree Time (s)'}")
print("-" * 50)
for n, lru, splay in zip(n_values, lru_times, splay_times):
    print(f"{n:<10}{lru:<20.10f}{splay:.10f}")