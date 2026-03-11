from functions.write_file import write_file

#Test Calls
result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print("Test 1")
print(result)
result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print("Test 2")
print(result)
result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print("Test 3")
print(result)