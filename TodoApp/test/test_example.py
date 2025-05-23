import pytest




def test_equal_or_not_equal():
    assert type(10 is int)
    assert 3 != 1


def test_is_instance():
    num_list = [1,2,3,4,5]
    assert 1 in num_list 



#user object test

class Student:
    def __init__(self,first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    return Student('John', 'Doe', 'Computer Science', 3)


def test_person_initialization(default_employee):
    assert default_employee.first_name == 'John', 'First name should be John'
    assert default_employee.last_name == 'Doe', 'Last name should be Doe'
    assert default_employee.major == "Computer Science"
    assert default_employee.years == 3        