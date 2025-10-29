import timeit
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.setrecursionlimit(2000)

def fact_recursion(n):
    if n == 1 or n == 0: return 1
    else: return n*fact_recursion(n-1)

def fact_iteration(n):
    res = 1
    while n > 1: 
        res *= n
        n-=1
    return res

def memoize(func):
    cache = {}
    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]
    return wrapper

@memoize
def fact_recursion_memoize(n):
    if n == 1 or n == 0: return 1
    else: return n*fact_recursion_memoize(n-1)

@memoize
def fact_iteration_memoize(n):
    res = 1
    while n > 1: 
        res *= n
        n-=1
    return res

numbers = list(range(10, 500, 20))

times_rec = []
times_iter = []

times_rec_memoize = []
times_iter_memoize = []

for number in numbers:
    times_iter.append(min(timeit.repeat(lambda: fact_iteration(number), number=1000, repeat=5)))
    times_rec.append(min(timeit.repeat(lambda: fact_recursion(number), number=1000, repeat=5)))

for number in numbers:
    times_iter_memoize.append(min(timeit.repeat(lambda: fact_iteration_memoize(number), number=1000, repeat=5)))
    times_rec_memoize.append(min(timeit.repeat(lambda: fact_recursion_memoize(number), number=1000, repeat=5)))

times_iter = [round(t,3) for t in times_iter]
times_rec = [round(t,3) for t in times_rec]

times_iter_memoize = [round(t,7) for t in times_iter_memoize]
times_rec_memoize = [round(t,7) for t in times_rec_memoize]

X = numbers

Y1_1 = times_rec
Y1_2 = times_rec_memoize

Y2_1 = times_iter
Y2_2 = times_iter_memoize

plt.figure(figsize=(12, 8))
plt.plot(X, Y2_1, label="Итерация", color="blue", marker="o")
plt.plot(X, Y2_2, label="Итерация с мемоизацией", color="red", marker="p")
plt.plot(X, Y1_1, label="Рекурсия", color="pink", marker="o")
plt.plot(X, Y1_2, label="Рекурсия с мемоизацией", color="orange", marker="d")

plt.xlabel("n")
plt.ylabel("t")

plt.xticks(np.arange(10, 500+20, 20))
plt.yticks(np.arange(0, max(Y1_1)+0.01, 0.01))
plt.title("Зависимость t от n")
plt.legend()
plt.grid(True)

plt.figure(figsize=(12, 8))
plt.plot(X, Y2_2, label="Итерация с мемоизацией", color="red", marker="p")
plt.plot(X, Y1_2, label="Рекурсия с мемоизацией", color="orange", marker="d")

plt.xlabel("n")
plt.ylabel("t")

plt.xticks(np.arange(10, 500+20, 20))
plt.yticks(np.arange(min(Y1_2), max(Y2_2)+0.00002, 0.000005))
plt.title("Зависимость t от n (с мемоизацией)")
plt.legend()
plt.grid(True)

plt.show()


