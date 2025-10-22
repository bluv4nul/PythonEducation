import timeit
import matplotlib.pyplot as plt
import numpy as np

def fact_recoursion(n):
    if n == 1: return 1
    else: return n*fact_recoursion(n-1)

def fact_iteration(n):
    res = 1
    while n > 1: 
        res *= n
        n-=1
    return res

numbers = list(range(10, 910, 50))
times_rec = []
times_iter = []

for number in numbers:
    times_iter.append(min(timeit.repeat(lambda: fact_iteration(number), number=1000, repeat=5)))
    times_rec.append(min(timeit.repeat(lambda: fact_recoursion(number), number=1000, repeat=5)))

times_iter = [round(t,3) for t in times_iter]
times_rec = [round(t,3) for t in times_rec]

X = numbers
Y1 = times_rec
Y2 = times_iter

plt.figure(figsize=(12, 8))
plt.plot(X, Y1, label="Рекурсия", color="blue", marker="o")
plt.plot(X, Y2, label="Итерация", color="red", marker="x")

plt.xlabel("N")
plt.ylabel("t")

plt.xticks(np.arange(10, 910, 50))
plt.yticks(np.arange(0, 0.3, 0.01))

plt.title("Зависимость t от N")
plt.legend()
plt.grid(True)

plt.show()
