""""
Name: Kosuke Kobayashi
Course: CS 1410
Project Payroll Part 2
"""

from abc import ABC, abstractmethod
import os

PAY_LOGFILE = "paylog.txt"
employees = []


def load_employees():
    with open("employees.csv", "r") as file_reader:
        file_reader.readline()
        while True:
            emp_info = file_reader.readline().strip().split(',')
            if len(emp_info) == 1:
                break
            emp = Employee(emp_info[0], emp_info[1], emp_info[2],
                           emp_info[3], emp_info[4], emp_info[5], emp_info[6])
            employees.append(emp)
            # 3 = hourly, 2 = Commisioned, 1 = Salary
            if emp_info[7] == "3":
                emp.make_hourly(float(emp_info[10]))
            elif emp_info[7] == "2":
                emp.make_commissioned(float(emp_info[8]), float(emp_info[9]))
            elif emp_info[7] == "1":
                emp.make_salaried(float(emp_info[8]))


def find_employee_by_id(emp_id):
    for emp in employees:
        if emp.emp_id == emp_id:
            return emp
    return None


def process_timecards():
    with open("timecards.csv", "r") as time_file:
        while True:
            timecard_info = time_file.readline().strip().split(",")
            if len(timecard_info) == 1:
                break
            emp = find_employee_by_id(timecard_info[0])
            if emp == None:
                print(f"Employee {timecard_info[0]} does not exit.")
                continue
            if not isinstance(emp.classification, Hourly):
                print(f'Employee {timecard_info[0]} is not Hourly')
            for i in range(1, len(timecard_info)):
                emp.classification.add_timecard(float(timecard_info[i]))


def process_receipts():
    with open("receipts.csv", "r") as res_file:
        while True:
            receipt_info = res_file.readline().strip().split(",")
            if len(receipt_info) == 1:
                break
            emp = find_employee_by_id(receipt_info[0])
            if emp == None:
                print(f"Employee {receipt_info[0]} does not exit.")
                continue
            if not isinstance(emp.classification, Commisioned):
                print(f"Employee {receipt_info[0]} is not Commisioned")
            for i in range(1, len(receipt_info)):
                emp.classification.add_receipt(float(receipt_info[i]))


def run_payroll():
    if os.path.exists(PAY_LOGFILE):
        os.remove(PAY_LOGFILE)
    for emp in employees:
        emp.issue_payment()


class Employee:
    def __init__(self, emp_id, first_name, last_name, address, city, state, zipcode):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.classification = None

    def make_hourly(self, hourly_rate):
        self.classification = Hourly(hourly_rate)

    def make_salaried(self, amount_salary):
        self.classification = Salaried(amount_salary)

    def make_commissioned(self, amount_salary, rate):
        self.classification = Commisioned(amount_salary, rate)

    def issue_payment(self):
        pay = self.classification.compute_pay()
        with open(PAY_LOGFILE, "a") as out_file:
            print("Mailing ", pay, "to", self.first_name,
                  self.last_name, "at", self.address, self.city, self.state, self.zipcode, file=out_file)


class Classification(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def compute_pay(self):
        pass

# Hourly


class Hourly(Classification):
    def __init__(self, hourly_rate):
        self.hourly_rate = hourly_rate
        self.hours_worked = []

    def add_timecard(self, hours):
        self.hours_worked.append(hours)

    def compute_pay(self):
        return sum(self.hours_worked) * self.hourly_rate

# Salary


class Salaried(Classification):
    def __init__(self, amount_salary):
        self.amount_salary = amount_salary

    def compute_pay(self):
        return round(self.amount_salary / 24, 2)

# Commisioned


class Commisioned(Salaried):
    def __init__(self, amount_salary, rate):
        self.amount_salary = amount_salary
        self.rate = rate
        self.reciptes = []

    def add_receipt(self, d):
        return 400.0 + d*25

    def compute_pay(self):
        return round(self.amount_salary/24+2250.0*self.rate/100.0, 2)
