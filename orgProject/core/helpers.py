def get_positive_integer_input( prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("\nValue must be a positive number.")
            else:
                return value
        except ValueError:
            print("\nInvalid input. Please enter a valid number.") 

