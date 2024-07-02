def find_password(n):
    result = ""
    pairs = []
    for i in range(1, n):
        for j in range(i + 1, n):
            if n % (i + j) == 0:
                pairs.append((i, j))
    for pair in pairs:
        result += str(pair[0]) + str(pair[1])
    return result
n = int(input("Введите число от 3 до 20: "))
if 3 <= n <= 20:
    print(find_password(n))
else:
    print("Число должно быть в диапазоне от 3 до 20.")
