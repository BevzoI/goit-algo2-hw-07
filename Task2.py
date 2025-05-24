import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

# ---------------------- LRU Cache Implementation ----------------------
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# ---------------------- Splay Tree Implementation ----------------------
class SplayNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._right_rotate(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._left_rotate(root.left)
            return root if root.left is None else self._right_rotate(root)
        else:
            if root.right is None:
                return root
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._right_rotate(root.right)
            return root if root.right is None else self._left_rotate(root)

    def search(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayNode(key, value)
            return

        self.root = self._splay(self.root, key)

        if self.root.key == key:
            return

        new_node = SplayNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None

        self.root = new_node

def fibonacci_splay(n, tree):
    cached = tree.search(n)
    if cached is not None:
        return cached
    if n < 2:
        tree.insert(n, n)
        return n
    val = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, val)
    return val

# ---------------------- Timing and Results ----------------------
import numpy as np
import pandas as pd

ns = list(range(0, 1000, 50))
lru_times = []
splay_times = []

for n in ns:
    # LRU Cache timing
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=1)
    lru_times.append(lru_time)

    # Splay Tree timing
    splay_tree = SplayTree()
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, splay_tree), number=1)
    splay_times.append(splay_time)

# ---------------------- Plotting ----------------------
plt.figure(figsize=(10, 6))
plt.plot(ns, lru_times, marker='o', label='LRU Cache')
plt.plot(ns, splay_times, marker='x', label='Splay Tree')
plt.xlabel('n (Fibonacci Index)')
plt.ylabel('Average Time (seconds)')
plt.title('Performance Comparison: LRU Cache vs Splay Tree')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ---------------------- Tabular Output ----------------------
df = pd.DataFrame({
    'n': ns,
    'LRU Cache Time (s)': lru_times,
    'Splay Tree Time (s)': splay_times
})

print(df.to_string(index=False))


