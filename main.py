from calculator import Calculator


def main() -> None:
    calculator = Calculator()
    first_number = 10
    second_number = 4

    print(f"{first_number} + {second_number} = {calculator.add(first_number, second_number)}")
    print(f"{first_number} - {second_number} = {calculator.subtract(first_number, second_number)}")
    print(f"{first_number} * {second_number} = {calculator.multiply(first_number, second_number)}")


if __name__ == "__main__":
    main()