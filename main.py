from enum import Enum
from typing import Callable, Dict, Tuple
from collections import UserDict
import re

class Command(Enum):
    HELLO = 1
    ADD = 2
    CHANGE = 3
    PHONE = 4
    ALL = 5
    CLOSE = 6
    EXIT = 7

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "" if self.value is None else str(self.value)
    
class Name(Field):
		pass

class Phone(Field):
    MATCH_PATTERN = re.compile(r'^\d{10}$')

    def __init__(self, value: str):
        super().__init__(None)
        if value is not None:
            self.value = value 

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, new_value: str) -> None:
        if new_value is None:
            self._value = None
            return

        if not isinstance(new_value, str):
            raise TypeError("The telephone number must be a string")
        if not self.MATCH_PATTERN.fullmatch(new_value):
            raise ValueError("The telephone number must contain exactly 10 digits")
        self._value = new_value



class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, value):
         self.phones.append(Phone(value))

    def remove_phone(self, value):
         self.phones.remove(value)

    def edit_phone(self, old_value, new_value):
        for i, p in enumerate(self.phones):
                cur = p.value
                if cur == old_value:
                    self.phones[i] = Phone(new_value)
                    return True
        return False
    
    def find_phone(self, value):
        for phone in self.phones:
            if phone.value == value:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    
    def add_record(self, record):
        key = record.name.value.strip().lower()
        self.data[key] = record

    def find(self, name: str):
        return self.data.get(name.strip().lower())
    
    def delete(self, name):
         normalized_name = name.strip().lower()
         del self.data[normalized_name]


def main() -> None:
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}") 

    book.delete("Jane")


if __name__ == "__main__":
    main()