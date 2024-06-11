first = int(input("Enter first number: "))
second = int(input("Enter second number: "))
third = int(input("Enter third number: "))
if first == second == third:
    print("3")
elif first == second or second == third or first == third:
    print("2")
else:
    print("0")
