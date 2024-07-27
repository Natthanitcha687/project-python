main.py

import sys
from PySide6.QtWidgets import QApplication
from database.db import initialize_database, addUserAndOthers, printInfo, delete_all_appointment, clear_all_appointments
from window.LoginUI import LoginUI

if __name__ == " __main__":
    initialize_database()
    addUserAndOthers()
    printInfo()

    app = QApplication(sys.argv)
    window = LoginUI()
    window.show()

    sys.exit(app.exec())



All class
Admin class

from .Staff import Staff
from .Log import Log
class Admin(Staff) :
    def __init__(self, fname: str, lname: str, address: str, phone_number: str, password: str ,employee_id: str ,department:str, role: str):
        super().__init__(fname, lname, address, phone_number, password, employee_id, department, role)
    def get_id(self):
        return self.employee_id
    def get_appointment(self):
        return None



Appointment class

import persistent
from persistent.list import PersistentList

class ExaminationRoom(persistent.PersistentList):
    def __init__(self, room_number):
        self.room_number = room_number
        self.appointment_by_date = {}

    def add_appointment(self, appointment):
        if self.check_availability(appointment) == False:
            return False
        date + appointment.date
        if datenot in self.appointment_by_date:
            self.appointment_by_date[date] = PersistentList()
        self.appointment_by_date[date].append(appointment)
        appointment.room  == self
        self._p_changed = True
        from database.db import save
        save()
        return True

    def remove_appointment(self, appointment): 
        date = appointment.date
        if date in self.appointments_by_date:
            self.appointments_by_date[date].remove(appointment)
            appointment.room = None
            self._p_changed = True
            from database.db import save
            save()
            
    def get_appointments(self, date):
        if date in self.appointments_by_date:
            return self.appointments_by_date[date]
        return None

    def get_all_appointments(self):
        return self.appointments_by_date
        
    def get_today_appointments(self):
        from datetime import date
        today = date.today()
        today = today.strftime("%Y-%m-%d")
        return self.get_appointments(today)

    def get_room_number(self):
        return self.room_number
        
    def set_room_number(self, room_number):
        self.room_number = room_number
        self._p_changed = True
        from database.db import save
        save()
        
    def check_availability(self, appointment):
        date = appointment.date
        if date in self.appointments_by_date:
            for app in self.appointments_by_date[date]:
                if app.start_time <= appointment.start_time < app.end_time:
                    return False
                if app.start_time < appointment.end_time <= app.end_time:
                    return False
        return True



class Appointment(persistent.Persistent):
    def __init__(self, id, date, start_time, end_time, doctor, speciality, patient, confirm):
        self.id = id
        self.date = date
        self.patient = patient
        self.doctor = doctor
        self.speciality = speciality
        self.confirm = confirm
        self.start_time = start_time
        self.end_time = end_time
        self.room = None
        self.nurse = PersistentList()

    def cancel(self):
        self.confirm = False
        self._p_changed = True
        self.patient.remove_appointment(self.id)
        self.doctor.remove_appointment(self.id)
        if self.nurse is not None:
            for nurse in self.nurse:
                nurse.remove_appointment(self.id)
        if self.room is not None:
            self.room.remove_appointment(self)
        from database.db import delete_appointment_db
        delete_appointment_db(self.id)
        
    def schedule(self):
        self.confirm = "Yes"
        self._p_changed = True
        from database.db import save
        save()
    
    def reject(self):
        self.confirm = "reject"
        self._p_changed = True
        from database.db import save
        save()

# def assign_nurse(self, nurse):
# self.nurse = nurse
# nurse.add_appointment(self.id)
# self._p_changed = True
# from database.db import save
# save()

    def add_nurse(self, nurse):
        self.nurse.append(nurse)
        nurse.add_appointment(self)
        self._p_changed = True
        from database.db import save
        save()
        
    def set_time(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self._p_changed = True
    
    def set_room(self, room):
        self.room = room
        room.add_appointment(self)
        self._p_changed = True
        from database.db import save
        save()


Doctor class

from .Staff import Staff
from persistent.list import PersistentList

class Doctor(Staff):
    def __init__(self, fname: str, lname: str, address: str, phone_number: str, password: str ,employee_id: str,department: str, role: str, specialty: list[str],qualifications: str, salary: int, working_time: str):
        super().__init__(fname, lname,address, phone_number, password, employee_id, department, role)
        self.specialty = specialty
        self.qualifications = qualifications
        self.salary = salary
        self.working_time = working_time
        self.appointments = PersistentList()

    def get_specialty(self):
        return self.specialty

    def get_department(self):
        return self.department

    def get_qualifications(self):
        return self.qualifications
        
    def get_salary(self):
        return self.salary
        
    def set_specialty(self, specialty):
        self.specialty = specialty
        
    def set_qualifications(self, qualifications):
        self.qualifications = qualifications
        
    def set_salary(self, salary):
        self.salary = salary
        
    def set_working_time(self, working_time):
        self.working_time = working_time
        
    def get_working_time(self):
        return self.working_time
        
    def add_appointment(self, appointment_id):
        self.appointments.append(appointment_id)
        self._p_changed = True
        
    def remove_appointment(self, appointment_id):
        if appointment_id in self.appointments:
            self.appointments.remove(appointment_id)
            self._p_changed = True
            
        def get_appointments(self):
            return list(self.appointments)
            
        def update_attributes(self, new_data):
            # ['doctor1', 'lname', '123 Main St', '123-456-7890', 'Cardiology', 'MDu', '80000', '8:00-17:00']
            # super().update_attributes(new_data[0], new_data[1], new_data[2], new_data[3])
            # self.set_specialty(new_data[4])
            # self.set_qualifications(new_data[5])
            # self.set_salary(int(new_data[6]))
            # self.set_working_time(new_data[7])


Log class

# from Person import Person
import persistent
from persistent.list import PersistentList
from datetime import datetime

class Log(persistent.Persistent):
    def __init__(self, id: int, actor, action: str, target):
        self.id = id
        self.time = datetime.now()
        self.actor = actor
        self.action = action
        self.target = target

    def get_id(self):
        return self.id
    
    def get_time(self):
        return self.time.strftime("%m/%d/%Y, %H:%M:%S")
        
    def get_actor(self):
        return self.actor
        
    def get_action(self):
        return self.action
        
    def get_target(self):
        return self.target
        
    def get_details(self):
        return f"{self.id} {self.time} {self.actor.get_fname()} {self.action} {self.target.get_fname()}"
        
    def get_actor_fname(self):
        return self.actor.get_fname()
        def get_target_fname(self):
        return self.target.get_fname()

Nurse class
from .Staff import Staff
from persistent.list import PersistentList

class Nurse(Staff):
    def __init__(self, fname: str, lname: str, address: str, phone_number: str, password: str, employee_id: str, department: str, role: str, assigned_wards: list, qualifications: str, salary: int, working_time: str):
        super().__init__(fname, lname,address, phone_number, password, employee_id, department, role)
        self.assigned_wards = assigned_wards
        self.qualifications = qualifications
        self.salary = salary
        self.working_time = working_time # "8:00-16:00"
        self.appointments = PersistentList()\
    
    def set_qualifications(self, qualifications):
        self.qualifications = qualifications

    def get_qualifications(self):
        return self.qualifications

    def set_salary(self, salary):
        self.salary = salary

    def get_salary(self):
        return self.salary

    def get_department(self):
        return self.department
        
    def set_working_time(self, working_time):
        self.working_time = working_time
        
    def get_working_time(self):
        return self.working_time
        
    def add_appointment(self, appointment):
        self.appointments.append(appointment)
        self._p_changed = True
        from database.db import save
        save()
        
    def remove_appointment(self, id):
        self.appointments.remove(id)
        self._p_changed = True
        from database.db import save
        save()
        
    def remove_appointment(self, appointment_id):
        if appointment_id in self.appointments:
            self.appointments.remove(appointment_id)
            self._p_changed = True
            
    def get_appointments(self):
        return list(self.appointments)
        
    def update_attributes(self, new_data):
        # ['Nurse1', 'lname', '123 Main St', '123-456-7890', 'Cardiology', 'BD', '40000']
        super().update_attributes(new_data[0], new_data[1], new_data[2], new_data[3])
        self.set_department(new_data[4])
        self.set_qualifications(new_data[5])
        self.set_salary(int(new_data[6]))
        self.set_working_time(new_data[7])


Patient class

from .Person import Person
from persistent.list import PersistentList
# from .db

class Patient(Person):
    def __init__(self, fname: str, lname: str, address: str,phone_number: str, password: str, patient_id: int,photo=None, medical_history=None):
        super().__init__(fname=fname, lname=lname, address=address,phone_number=phone_number, password=password,photo=photo)
        self.patient_id = patient_id
        self.medical_history = {}
        self.appointments = PersistentList()

    def get_id(self):
        return self.patient_id
        
    def update_attributes(self, new_data):
        # ['John', 'Doe', '123 Main St', '123-456-7890', '12345']
        super().update_attributes(new_data[0], new_data[1], new_data[2], new_data[3])
        
    def add_appointment(self, appointment):
        self.appointments.append(appointment)
        self._p_changed = True
        
    def remove_appointment(self, appointment_id):
        if appointment_id in self.appointments:
            self.appointments.remove(appointment_id)
            self._p_changed = True
    
    def get_appointments(self):
        return list(self.appointments)
        
    def display_reports(self):
        for report in self.medical_history:
            report.display_report()
    
    def add_medical_history(self, report):
        self.medical_history[report.id] = report
        self._p_changed = True


Person class

import hashlib
import persistent
from persistent.list import PersistentList
from abc import ABC, abstractmethod

class Person(persistent.Persistent, ABC):
    def __init__(self, fname: str, lname: str, address: str,phone_number: str,password: str, photo: str = None):
        self.fname = fname
        self.lname = lname
        self.address = address
        self.phone_number = phone_number
        self.photo = photo
        self.password = self.hash(password)
    
    @abstractmethod
    def get_id(self):
        pass

    def update_attributes(self, fname: str, lname: str, address: str, phone_number: str):
        self.fname = fname
        self.lname = lname
        self.address = address
        self.phone_number = phone_number
        
        def get_fname(self):
            return self.fname
            
        def get_lname(self):
            return self.lname
            
        def get_address(self):
            return self.address
            
        def get_phone_number(self):
            return self.phone_number
            
        def get_photo(self):
            return self.photo
            
        def get_password(self):
            return self.password
            
        def get_detail(self):
            return self.fname, self.lname, self.address, self.phone_number
            
        def set_fname(self, fname):
            self.fname = fname
            
        def set_lname(self, lname):
            self.lname = lname
            
        def set_address(self, address):
            self.address = address
            
        def set_phone_number(self, phone_number):
            self.phone_number = phone_number
            
        def set_photo(self, photo):
            self.photo = photo
            
        def set_password(self, password):
            self.password = self.hash(password)
            
        def hash(self, password):
            hashed = hashlib.sha256(password.encode()).hexdigest()
            return hashed
            
        def verify_password(self, password):
            return self.password == self.hash(password)

Report class
import persistent
from persistent.list import PersistentList
from datetime import datetime
from abc import ABC, abstractmethod
# from database.db import save
import transaction

class MedicalRecord(persistent.Persistent):
    def __init__(self, height=None, weight=None, sex=None, pulse_rate=None, blood_pressure=None, allegies=None,title=None, description=None, details=None):
        self.height = height
        self.weight = weight
        self.sex = sex
        self.pulse_rate = pulse_rate
        self.blood_pressure = blood_pressure
        self.allegies = allegies
        self.title = title
        self.description = description
        self.details = details

class BillableItem(ABC,persistent.Persistent):
    def __init__(self, name, price, discount_percentage):
        self.name = name
        self.price = price
        self.discount_percentage = discount_percentage
        self.total = 0

    @abstractmethod
    def calculate_sum(self) -> float:
        pass

class Medicine(BillableItem):
    def __init__(self, id, name, description, quantity, duration, when_to_consume, price_per_dose):
        super().__init__(name, price_per_dose * quantity, discount_percentage=0)
        self.medicine_id = id
        self.description = description
        self.quantity = quantity
        self.duration = duration
        self.when_to_consume = when_to_consume
        self.price_per_dose = price_per_dose
        self.total = self.calculate_sum()

    def calculate_sum(self):
        return self.price_per_dose * self.quantity

class Service(BillableItem):
    def __init__(self, name, price, discount_percentage, insurance_name, insurance_coverage):
        super().__init__(name, price, discount_percentage)
        self.insurance_name = insurance_name
        self.insurance_coverage = insurance_coverage
        self.total = self.calculate_sum()

    def calculate_sum(self):
        self.total = self.price - self.insurance_coverage
        self.total = self.total - (self.total * (self.discount_percentage/100))
        return self.total

    def save():
        transaction.commit()

class Bill(persistent.Persistent):
    def __init__(self, discount_percentage):
        self.services = PersistentList()
        self.medicines = PersistentList()
        self.discount_percentage = discount_percentage
        self.paid = "unpaid"
        self.slip = None

    def addSlip(self, path):
        with open(path, 'rb') as f:
            image_data = f.read()
            self.slip = image_data
            self.paid = "pending"
            save()

    def getSlip(self):
        return self.convert_to_qpixmap(self.slip)

    def convert_to_qpixmap(self, image_data):
        from PySide6.QtGui import QImage, QPixmap
        # Convert image data to QImage
        image = QImage.fromData(image_data)
        # Convert QImage to QPixmap
        pixmap = QPixmap.fromImage(image)
        print("Image converted to QPixmap")
        save()
        return pixmap

    def getStatus(self):
        return self.paid

    def confirmPayment(self):
        self.paid = "paid"
        save()

    def rejectPayment(self):
        self.paid = "unpaid"
        save()

    def setServices(self, services):
        self.services = services
        
    def setMedicines(self, medicines):
        self.medicines = medicines
        
    def addService(self, service):
        self.services.append(service)
        self._p_changed = True
    
    def addMedicine(self, medicine):
        self.medicines.append(medicine)
        self._p_changed = True
    
    def total_services(self):
        total = 0
        for service in self.services:
            total += service.total
        return total
    
    def total_medicines(self):
        total = 0
        for medicine in self.medicines:
            total += medicine.total
        return total
            
    def total_without_discount(self):
        return self.total_services() + self.total_medicines()
        
    def total_after_discount(self):
        if self.discount_percentage > 0:
            return self.total_without_discount() - (self.total_without_discount() * (self.discount_percentage/100))
        else:
            return self.total_without_discount() # No discount if percentage is 0

class Report(persistent.Persistent):
    def __init__(self, id: int, patient_id: int, doctor_id: int, medical_record: MedicalRecord, bill: Bill):
        self.id = id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.medical_record = medical_record
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.bill = bill

    def generate_report(self):
        print(f"Patient ID: {self.patient_id}")
        print(f"Doctor ID: {self.doctor_id}")
        print(f"Date: {self.date}")
        print(f"Height: {self.medical_record.height}")
        print(f"Weight: {self.medical_record.weight}")
        for service in self.bill.services:
            print(f"Service: {service.name}")
            print(f"Price: {service.price}")
            print(f"Discount: {service.discount_percentage}")
            print(f"Insurance: {service.insurance_name}")
            print(f"Insurance Coverage: {service.insurance_coverage}")
        for medicine in self.bill.medicines:
            print(f"Medicine: {medicine.name}")
            print(f"Price: {medicine.price}")
            print(f"Discount: {medicine.discount_percentage}")
            print(f"Quantity: {medicine.quantity}")
            print(f"Duration: {medicine.duration}")
            print(f"When to Consume: {medicine.when_to_consume}")
            print(f"Price per Dose: {medicine.price_per_dose}")
            print(f"Total Services: {self.bill.total_services()}")
            print(f"Total Medicines: {self.bill.total_medicines()}")
            print(f"Total without Discount: {self.bill.total_without_discount()}")
            print(f"Total after Discount: {self.bill.total_after_discount()}")
            # print(f"Title: {self.medical_record.title}")
            # # print(f"Description: {self.medical_record.description}")
            # # print(f"Details: {self.medical_record.details}")

import persistent
from persistent.list import PersistentList

class ExaminationRoom(persistent.Persistent):
    def __init__(self, room_number):
        self.room_number = room_number
        self.appointments_by_date = {}
        
    def add_appointment(self, appointment):
        if self.check_availability(appointment) == False:
            return False
        date = appointment.date
        if date not in self.appointments_by_date:
            self.appointments_by_date[date] = PersistentList()
        self.appointments_by_date[date].append(appointment)
        appointment.room = self
        self._p_changed = True
        from database.db import save
        save()
        return True
        
    def remove_appointment(self, appointment):
        date = appointment.date
        if date in self.appointments_by_date:
            self.appointments_by_date[date].remove(appointment)
            appointment.room = None
            self._p_changed = True
            from database.db import save
            save()

    def get_appointments(self, date):
        if date in self.appointments_by_date:
            return self.appointments_by_date[date]
        return None
        
    def get_all_appointments(self):
        return self.appointments_by_date
        
    def get_today_appointments(self):
        from datetime import date
        today = date.today()
        today = today.strftime("%Y-%m-%d")
        return self.get_appointments(today)
        
    def get_room_number(self):
        return self.room_number
        
    def set_room_number(self, room_number):
        self.room_number = room_number
        self._p_changed = True
        from database.db import save
        save()
        
    def check_availability(self, appointment):
        date = appointment.date
        if date in self.appointments_by_date:
            for app in self.appointments_by_date[date]:
                if app.start_time <= appointment.start_time < app.end_time:
                    return False
                if app.start_time < appointment.end_time <= app.end_time:
                    return False
        return True

class Appointment(persistent.Persistent):
    def __init__(self, id, date, start_time, end_time, doctor, speciality, patient, confirm):
        self.id = id
        self.date = date
        self.patient = patient
        self.doctor = doctor
        self.speciality = speciality
        self.confirm = confirm
        self.start_time = start_time
        self.end_time = end_time
        self.room = None
        self.nurse = PersistentList()

    def cancel(self):
        self.confirm = False
        self._p_changed = True
        self.patient.remove_appointment(self.id)
        self.doctor.remove_appointment(self.id)
        if self.nurse is not None:
            for nurse in self.nurse:
                nurse.remove_appointment(self.id)
        if self.room is not None:
            self.room.remove_appointment(self)
        from database.db import delete_appointment_db
        delete_appointment_db(self.id)

    def schedule(self):
        self.confirm = "Yes"
        self._p_changed = True
        from database.db import save
        save()
        
    def reject(self):
        self.confirm = "reject"
        self._p_changed = True
        from database.db import save
        save()
    # def assign_nurse(self, nurse):
    # self.nurse = nurse
    # nurse.add_appointment(self.id)
    # self._p_changed = True
    # from database.db import save
    # save()

    def add_nurse(self, nurse):
        self.nurse.append(nurse)
        nurse.add_appointment(self)
        self._p_changed = True
        from database.db import save
        save()
        
    def set_time(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self._p_changed = True
        
    def set_room(self, room):
        self.room = room
        room.add_appointment(self)
        self._p_changed = True
        from database.db import save
        save()

# from Person import Person

import persistent
from persistent.list import PersistentList
from datetime import datetime

class Log(persistent.Persistent):
    def __init__(self, id: int, actor, action: str, target):
        self.id = id
        self.time = datetime.now()
        self.actor = actor
        self.action = action
        self.target = target
        
    def get_id(self):
        return self.id
        
    def get_time(self):
        return self.time.strftime("%m/%d/%Y, %H:%M:%S")
        
    def get_actor(self):
        return self.actor
    
    def get_action(self):
        return self.action
        
    def get_target(self):
        return self.target
        
    def get_details(self):
        return f"{self.id} {self.time} {self.actor.get_fname()} {self.action} {self.target.get_fname()}"
        
    def get_actor_fname(self):
        return self.actor.get_fname()
        
    def get_target_fname(self):
        return self.target.get_fname()

import persistent
from persistent.list import PersistentList
from datetime import datetime
from abc import ABC, abstractmethod
# from database.db import save
import transaction

class MedicalRecord(persistent.Persistent):
    def __init__(self, height=None, weight=None, sex=None, pulse_rate=None, blood_pressure=None, allegies=None,title=None, description=None, details=None):
        self.height = height
        self.weight = weight
        self.sex = sex
        self.pulse_rate = pulse_rate
        self.blood_pressure = blood_pressure
        self.allegies = allegies
        self.title = title
        self.description = description
        self.details = details

class BillableItem(ABC,persistent.Persistent):
    def __init__(self, name, price, discount_percentage):
        self.name = name
        self.price = price
        self.discount_percentage = discount_percentage
        self.total = 0

    @abstractmethod
    def calculate_sum(self) -> float:
        pass

class Medicine(BillableItem):
    def __init__(self, id, name, description, quantity, duration, when_to_consume, price_per_dose):
        super().__init__(name, price_per_dose * quantity, discount_percentage=0)
        self.medicine_id = id
        self.description = description
        self.quantity = quantity
        self.duration = duration
        self.when_to_consume = when_to_consume
        self.price_per_dose = price_per_dose
        self.total = self.calculate_sum()

    def calculate_sum(self):
        return self.price_per_dose * self.quantity

class Service(BillableItem):
    def __init__(self, name, price, discount_percentage, insurance_name, insurance_coverage):
        super().__init__(name, price, discount_percentage)
        self.insurance_name = insurance_name
        self.insurance_coverage = insurance_coverage
        self.total = self.calculate_sum()
        
    def calculate_sum(self):
        self.total = self.price - self.insurance_coverage
        self.total = self.total - (self.total * (self.discount_percentage/100))
        return self.total

def save():
    transaction.commit()

class Bill(persistent.Persistent):
    def __init__(self, discount_percentage):
        self.services = PersistentList()
        self.medicines = PersistentList()
        self.discount_percentage = discount_percentage
        self.paid = "unpaid"
        self.slip = None
    
    def addSlip(self, path):
        with open(path, 'rb') as f:
            image_data = f.read()
            self.slip = image_data
        self.paid = "pending"
        save()

    def getSlip(self):
        return self.convert_to_qpixmap(self.slip)

    def convert_to_qpixmap(self, image_data):
        from PySide6.QtGui import QImage, QPixmap
        # Convert image data to QImage
        image = QImage.fromData(image_data)
        # Convert QImage to QPixmap
        pixmap = QPixmap.fromImage(image)
        print("Image converted to QPixmap")
        save()
        return pixmap

    def getStatus(self):
        return self.paid
        
    def confirmPayment(self):
        self.paid = "paid"
        save()
    
    def rejectPayment(self):
        self.paid = "unpaid"
        save()
        
    def setServices(self, services):
        self.services = services
        
    def setMedicines(self, medicines):
        self.medicines = medicines
        
    def addService(self, service):
        self.services.append(service)
        self._p_changed = True
        
    def addMedicine(self, medicine):
        self.medicines.append(medicine)
        self._p_changed = True
        
    def total_services(self):
        total = 0
        for service in self.services:
            total += service.total
        return total
        
    def total_medicines(self):
        total = 0
        for medicine in self.medicines:
            total += medicine.total
        return total
        
    def total_without_discount(self):
        return self.total_services() + self.total_medicines()

    def total_after_discount(self):
        if self.discount_percentage > 0:
            return self.total_without_discount() - (self.total_without_discount() * (self.discount_percentage/100))
        else:
            return self.total_without_discount() # No discount if percentage is 0

class Report(persistent.Persistent):
    def __init__(self, id: int, patient_id: int, doctor_id: int, medical_record: MedicalRecord, bill: Bill):
        self.id = id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.medical_record = medical_record
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.bill = bill
    
    def generate_report(self):
        print(f"Patient ID: {self.patient_id}")
        print(f"Doctor ID: {self.doctor_id}")
        print(f"Date: {self.date}")
        print(f"Height: {self.medical_record.height}")
        print(f"Weight: {self.medical_record.weight}")
        for service in self.bill.services:
            print(f"Service: {service.name}")
            print(f"Price: {service.price}")
            print(f"Discount: {service.discount_percentage}")
            print(f"Insurance: {service.insurance_name}")
            print(f"Insurance Coverage: {service.insurance_coverage}")
        for medicine in self.bill.medicines:
            print(f"Medicine: {medicine.name}")
            print(f"Price: {medicine.price}")
            print(f"Discount: {medicine.discount_percentage}")
            print(f"Quantity: {medicine.quantity}")
            print(f"Duration: {medicine.duration}")
            print(f"When to Consume: {medicine.when_to_consume}")
            print(f"Price per Dose: {medicine.price_per_dose}")
            print(f"Total Services: {self.bill.total_services()}")
            print(f"Total Medicines: {self.bill.total_medicines()}")
            print(f"Total without Discount: {self.bill.total_without_discount()}")
            print(f"Total after Discount: {self.bill.total_after_discount()}")
            # print(f"Title: {self.medical_record.title}")
            # print(f"Description: {self.medical_record.description}")
            # print(f"Details: {self.medical_record.details}")

Staff class

from .Person import Person

class Staff(Person):
    def __init__(self, fname: str, lname:str, address: str, phone_number: str, password: str, employee_id: int,department: list[str], role: str):
        super().__init__(fname, lname, address, phone_number, password)
        self.employee_id = employee_id
        self.department = department
        self.role = role

    def get_id(self):
        return self.employee_id
        
    def get_department(self):
        return self.department
        
    def get_role(self):
        return self.role
        
    def set_id(self, id):
        self.employee_id = id
        
    def set_department(self, department):
        self.department = department
    
    def set_role(self, role):
        self.role = role
        