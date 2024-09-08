def personal_sum(numbers):
    result = 0
    incorrect_data = 0
    for num in numbers:
        try:
            result += num
        except TypeError:
            print(f'Некорректный тип данных для подсчёта суммы - {num}')
            incorrect_data += 1
    return result, incorrect_data

def calculate_average(numbers):
    try:
        if not hasattr(numbers, '__iter__'):
            raise TypeError('В numbers записан некорректный тип данных')

        result, incorrect_data = personal_sum(numbers)
        valid_data_count = len(numbers) - incorrect_data

        if valid_data_count == 0:
            return 0
        return result / valid_data_count

    except ZeroDivisionError:
        return 0
    except TypeError as e:
        if str(e) == 'В numbers записан некорректный тип данных':
            print(e)
            return None
        else:
            raise e

print(f'Результат 1: {calculate_average("1, 2, 3")}')
print(f'Результат 2: {calculate_average([1, "Строка", 3, "Ещё Строка"])}')
print(f'Результат 3: {calculate_average(567)}')
print(f'Результат 4: {calculate_average([42, 15, 36, 13])}')