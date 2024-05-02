import sys

def main():
    while True:
        user_input = input("Enter an expression to evaluate (or 'exit' to quit): ")
        
        if user_input.lower() == 'exit':
            print("Exiting the calculator.")
            break
        
        try:
            result = eval(user_input)
            print("Result: ", result)
        except Exception as e:
            print("Error: ", str(e))

if __name__ == "__main__":
    main()
