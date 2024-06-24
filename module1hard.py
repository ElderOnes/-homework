grades = [[5, 3, 3, 5, 4], [2, 2, 2, 3], [4, 5, 5, 2], [4, 4, 3], [5, 5, 5, 4, 5]]
students = {'Johnny', 'Bilbo', 'Steve', 'Khendrik', 'Aaron'}
list_student = sorted(students)
average_grades = {name: sum(grades[i]) / len(grades[i]) for i, name in enumerate(list_student)}
input_names = input("Введите имена учеников через запятую или введите 'все' для получения списка всех учеников: ").split(',')
input_names = [name.strip() for name in input_names]
if 'все' in input_names:
    for name, average in average_grades.items():
        print(f"{name}: {average}")
else:
    for name in input_names:
        proper_name = name.capitalize()
        if proper_name in average_grades:
            print(f"{proper_name}: {average_grades[proper_name]}")
        else:
            print(f"{name}: Ученик не найден")