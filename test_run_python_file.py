from functions.run_python_file import run_python_file
def test():
    result = run_python_file("calculator", "main.py")
    print("Result for calculator file:")
    print(result)
    print("")

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Result for calculator 3 + 5:")
    print(result)
    print("")

    result = run_python_file("calculator", "tests.py")
    print("Result for calculator tests:")
    print(result)
    print("")

    result = run_python_file("calculator", "../main.py")
    print("Result for running main.py:")
    print(result)
    print("")

    result = run_python_file("calculator", "nonexistent.py")
    print("result for nonexistent .py:")
    print(result)
    print("")

    result = run_python_file("calculator", "lorem.txt")
    print("result for lorem.txt:")
    print(result)

if __name__ == "__main__":
    test()