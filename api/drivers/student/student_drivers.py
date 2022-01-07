from abc import ABC, abstractmethod
from typing import final, Dict


class Student(ABC):
    """Student database driver.
        Responsible for various student related
        tasks.
    """

    @abstractmethod
    def add_student():
        pass

    @abstractmethod
    def update_student():
        pass

    @abstractmethod
    def get_student():
        pass

    @abstractmethod
    def ban_student():
        pass

    @abstractmethod
    def delete_student():
        pass


@final
class CurrentStudent(Student):
    """Current student database driver.
        Performes all tasks related to current student
    """

    def add_student(student_details):
        pass

    def update_student(student_id: str, fields_to_update: Dict[str, str]):
        pass

    def get_student(search_fields: dict):
        pass

    def ban_student(student_rollno: str):
        pass

    def delete_student(student_rollno: str):
        pass


@final
class FormerStudent(Student):
    """Former student database driver.
        Performes all tasks related to current student
    """

    def add_student(student_details):
        #NOTE: not sure if this functionality is required for alumnis
        
        pass

    def update_student(student_id: str, fields_to_update: dict):
        pass

    def get_student(search_fields: dict):
        pass

    def ban_student(student_rollno: str):
        pass

    def delete_student(student_rollno: str):
        pass
