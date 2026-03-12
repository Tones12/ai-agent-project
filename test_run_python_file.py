from functions.run_python_file import run_python_file


result = run_python_file("calculator", "main.py") # (should print the calculator's usage instructions)
print("Test 1: main.py")
print(result)

result = run_python_file("calculator", "main.py", ["3 + 5"]) # (should run the calculator... which gives a kinda nasty rendered result)
print("Test 2: main.py and calculation")
print(result)

result = run_python_file("calculator", "tests.py") # (should run the calculator's tests successfully)
print("Test 3: tests.py")
print(result)

result = run_python_file("calculator", "../main.py") # (this should return an error)
print("Test 4: ../main.py - should return error")
print(result)

result = run_python_file("calculator", "nonexistent.py") # (this should return an error)
print("Test 5: nonexistent.py - should return error")
print(result)

result = run_python_file("calculator", "lorem.txt") # (this should return an error)
print("Test 6: lorem.txt - should return error")
print(result)