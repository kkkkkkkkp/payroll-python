from payroll import *
import os
import shutil


employees = []
pay_log_file = "paylog.txt"


def load_employees():
    '''load all employees into memory'''
    with open("employees.csv", 'r') as f:
        data = [i.split(',') for i in f.read().split('\n')[1:]]

        for i in data[:-1]:
            emp = Employee(i[0], i[1], i[2], i[3], i[4], i[5])
            if i[6] == str(2):
                emp.make_salaried(i[8])
            elif i[6] == str(1):
                emp.make_hourly(i[9])
            elif i[6] == str(3):
                emp.make_commissioned(i[8], i[10])

            if (i[7] == str(1)):
                emp.direct_method(i[11], i[12])
            elif (i[7] == str(2)):
                emp.mail_method()

            employees.append(emp)


def find_employee_by_id(emp_id):
    '''return the emmployee with the correct id'''
    for i in employees:
        if i.emp_id == emp_id:
            return i


def process_timecards():
    '''load timecard data'''
    with open("timecards.txt", 'r') as f:
        timeCards = [i.split(',') for i in f.read().split('\n')]

        emp_id_list = [i[0] for i in timeCards]
        timeCards = [i[1:] for i in timeCards]

        timeDict = dict(zip(emp_id_list, timeCards))

        for key, value in timeDict.items():
            emp = find_employee_by_id(key)
            for i in value:
                emp.classification.add_timecard(i)


def process_receipts():
    '''load receipt data'''
    with open("receipts.txt", 'r') as f:
        r = [i.split(',') for i in f.read().split('\n')]

        emp_id_list = [i[0] for i in r]

        for i in emp_id_list[:-1]:
            emp = find_employee_by_id(i)
            for j in emp_id_list[1:]:
                emp.classification.add_receipt(i)


def run_payroll():
    '''execute main payroll logic'''
    if os.path.exists(pay_log_file):
        os.remove(pay_log_file)
    for emp in employees:
        emp.issue_payment()


def main():
    '''main priogram logig'''
    load_employees()
    process_timecards()
    process_receipts()
    run_payroll()

    # Save copy of payroll file; delete old file
    shutil.copyfile('paylog.txt', 'paylog_old.txt')
    if os.path.exists(pay_log_file):
        os.remove(pay_log_file)

    # Change Karina Gaay to Salaried and MailMethod by changing her Employee object:
    emp = find_employee_by_id('688997')
    emp.make_salaried(45884.99)
    emp.mail_method()
    emp.issue_payment()

    # Change TaShya Snow to Commissioned and DirectMethod; add some receipts
    emp = find_employee_by_id('522759')
    emp.make_commissioned(50005.50, 25)
    emp.direct_method('30417353-K', '465794-3611')
    clas = emp.classification
    clas.add_receipt(1109.73)
    clas.add_receipt(746.10)
    emp.issue_payment()

    # Change Rooney Alvarado to Hourly; add some hour entries
    emp = find_employee_by_id('165966')
    emp.make_hourly(21.53)
    clas = emp.classification
    clas.add_timecard(8.0)
    clas.add_timecard(8.0)
    clas.add_timecard(8.0)
    clas.add_timecard(8.0)
    clas.add_timecard(8.0)
    emp.issue_payment()


if __name__ == '__main__':
    main()
