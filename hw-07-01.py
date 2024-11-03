import re
from collections import UserDict
from datetime import datetime as dt
from datetime import timedelta as tdelta

################# homework 06 below
# Validation for correct number made with own exception in class Phone
#
# all the classes has their methods with realisation and all works fine
#
# mainly prints copied from the task, added a couple other for better visualisation
# of result
#
################# UPDATE for homework 07 below
#
# class Birthday added with ValueError exception detection
#
# function ADD_BIRTHDAY added without checking for existing data, so each execution
# for existing contact will update his birthday date, i think it's OK
#
# __str__ function for class Record now print info with birthday
#
# class AddressBook now has a GET_UPCOMING_BIRTHDAYS function adopted from HW-03-04
# and re-mastered for classes structure.
# Return list of dicts with keys: 'name' and 'congratulation_date'. Tested, working GOOD
# BUT
# it is too long, so it's a good idea to export it an external file in future


class PhoneNumberDoesNotExist(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        pattern = re.compile(r"\d{10}")
        if re.search(pattern, phone):
            super().__init__(phone)
        else:
            raise PhoneNumberDoesNotExist


class Birthday(Field):
    def __init__(self, bday: str):
        try:
            bd = dt.strptime(bday, "%d.%m.%Y")
            super().__init__(bd)
        except ValueError:
            raise ValueError(
                "Invalid date format fo Birthday value, please use format: DD.MM.YYYY"
            )


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
        except PhoneNumberDoesNotExist:
            pass

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value

    def remove_phone(self, phone):
        i = 0
        for p in self.phones:
            if p.value == phone:
                self.phones.pop(i)
            i += 1

    def edit_phone(self, old, new):
        for p in self.phones:
            p.value = new if p.value == old else p.value

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, bday: {dt.strftime(self.birthday.value, "%d.%m.%Y")}"


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[str(record.name)] = record

    def find(self, name):
        return self.data[name]

    def delete(self, name):
        self.data.pop(name, None)

    def get_upcoming_birthdays(self):

        notifications = []

        # get today values: date, year, number of the current day in year and total days is year

        # use next two lines to check fuctionality
        # today_date = dt.(2024, 12, 30).date()
        today_date = dt.today().date()

        today_year = today_date.year
        today_number_in_year = today_date.timetuple().tm_yday
        ny_number_in_year = dt(today_year, 12, 31).timetuple().tm_yday

        for name, record in self.data.items():

            # for current user found
            # his original birth date
            # his birthday this year
            # day number of birthday in year
            user_bd_original = record.birthday.value
            user_bd_this_year = dt(
                year=today_year, month=user_bd_original.month, day=user_bd_original.day
            ).date()
            user_bd_this_year_number = user_bd_this_year.timetuple().tm_yday

            # simple situation if birthday within a week from now
            if 0 <= user_bd_this_year_number - today_number_in_year <= 7:

                congratulation_date = user_bd_this_year

                # weekend days check and move date to monday if true
                if congratulation_date.isoweekday() >= 6:
                    congratulation_date += tdelta(8 - congratulation_date.isoweekday())

                # create and append dict to result list
                user_to_congratulate = {}
                user_to_congratulate["name"] = name
                user_to_congratulate["congratulation_date"] = (
                    congratulation_date.strftime("%d.%m.%Y")
                )
                notifications.append(user_to_congratulate)

            # situation at the end of year and birthday on january begin
            elif (
                ny_number_in_year - today_number_in_year + user_bd_this_year_number <= 7
            ):

                # congratulation_date must be set to next year
                congratulation_date = dt(
                    year=today_year + 1,
                    month=user_bd_original.month,
                    day=user_bd_original.day,
                )

                # weekend days check and move date to monday if true
                if congratulation_date.isoweekday() >= 6:
                    congratulation_date += tdelta(8 - congratulation_date.isoweekday())

                # create and append dict to result list
                user_to_congratulate = {}
                user_to_congratulate["name"] = name
                user_to_congratulate["congratulation_date"] = (
                    congratulation_date.strftime("%d.%m.%Y")
                )
                notifications.append(user_to_congratulate)

        return notifications


# test


def main():

    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John та Додавання запису John до адресної книги
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_phone("7777777__7")
    john_record.add_birthday("07.11.1984")
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("03.11.2024")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for _, record in book.data.items():
        print(record)

    # Пошук конкретного телефону у записі John
    john = book.find("John")
    found_phone = john.find_phone("5555555555")
    print(f"\n{john.name}: {found_phone}")

    # Знаходження та редагування телефону для John
    john = book.find("John")
    print(f"\nEDIT phone before and after:\n{john}")
    john.edit_phone("1234567890", "1112223333")
    print(f"{john}")

    # Видалення телефону у у записі John
    print(f"\nREMOVE phone before and after:\n{john}")
    john.remove_phone("1112223333")
    print(f"{john}")

    # Вивід списку зі словниками на привітання з ДН
    print(f"\nПривітати з ДН:")
    for r in book.get_upcoming_birthdays():
        print(f"{r["name"]} = {r["congratulation_date"]}")


if __name__ == "__main__":
    main()
