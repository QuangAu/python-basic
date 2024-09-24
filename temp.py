from contextlib import ContextDecorator


class ContextManagement:
    def __init__(self, input_number):
        self.value = input_number

    def print_something(self) -> None:
        """
        Increment the value by 1 and print the updated value.
        """
        if hasattr(self, 'value'):
            self.value += 1
            print(f"ID of self in print_something: {id(self)}")
            print(f"Run print_something with value {self.value}")

    def __enter__(self):
        print(f"ID of self in enter: {id(self)}")
        print(f"Run enter with value {self.value}")
        return self

    def __exit__(self, *args):
        print(f"ID of self in exit: {id(self)}")
        print(f"Run exit with value {self.value}")


class Session:
    def __init__(self, a: int, b: int):
        self.num1 = a
        self.num2 = b

    def total(self):
        return self.num1 + self.num2


class DatabaseSessionManager(ContextDecorator):
    def __init__(self):
        self.session = Session(1, 2)

    def __enter__(self):
        print("Create session")
        return self.session

    def __exit__(self, *args):
        print("Close session")

@DatabaseSessionManager()
def play_session():
    print("Something")

with DatabaseSessionManager() as conn:
    print("Something")
    print(f"Count = {conn.total()}")
