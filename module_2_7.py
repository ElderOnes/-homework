def print_params(a=1, b="пустая", c=True):
    print(a, b, c)
print_params(b = 25)
print_params(c = [1,2,3])
values_list = [1, "Два", True]
values_dict = {"a": "Один", "b": True, "c": 3}
print_params(*values_list)
print_params(**values_dict)
values_list2 = [2, True]
print_params(*values_list2, 42)