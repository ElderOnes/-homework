# Requests — Запрос данных с сайта:

import requests

url = 'https://jsonplaceholder.typicode.com/todos/1'

response = requests.get(url)

if response.status_code == 200:
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(response.json())
else:
    print(f"Failed to retrieve data, Status Code: {response.status_code}")

# Numpy — Математические операции с массивом:

import numpy as np

arr = np.array([1, 2, 3, 4, 5])

mean_value = np.mean(arr)

sum_value = np.sum(arr)

print(f"\nМассив чисел: {arr}")
print(f"Среднее значение массива: {mean_value}")
print(f"Сумма элементов массива: {sum_value}")

squared_array = np.square(arr)
print(f"Массив, возведённый в квадрат: {squared_array}")

# Matplotlib

import matplotlib.pyplot as plt
import numpy as np

#
x = np.linspace(0, 10, 100)
y = np.sin(x)
noise = np.random.normal(0, 0.1, size=x.shape)

plt.figure(figsize=(8, 6))
plt.plot(x, y, label='Sine wave', color='b', linestyle='-', marker='o')
plt.title('График синуса')
plt.xlabel('X-ось')
plt.ylabel('Y-ось')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 6))
plt.hist(noise, bins=20, color='g', alpha=0.7)
plt.title('Гистограмма случайного шума')
plt.xlabel('Значения')
plt.ylabel('Частота')
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 6))
plt.scatter(x, y + noise, label='Noisy Sine', color='r')
plt.title('Точечный график с шумом')
plt.xlabel('X-ось')
plt.ylabel('Y-ось')
plt.legend()
plt.grid(True)
plt.show()
