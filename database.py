from ZODB import FileStorage, DB
import transaction
from persistent import Persistent
from persistent.list import PersistentList
import BTrees.OOBTree

from All_class.Admin import Admin
from All_class.Doctor import Doctor
from All_class.Patient import Patient
from All_class.Nurse import Nurse
from All_class.Log import Log
from All_class.Appointment import Appointment , ExaminationRoom
from All_class.Report import Medicine, Service, Bill, MedicalRecord, Report

storage = FileStorage.FileStorage('src/database/healthcare_management.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

current_user = None
print("database opened")

def initialize_database():
    print("has attr promptPayId: ", hasattr(root, "promptPayId"))
    if not hasattr(root, "promptPayId"):
        root.promptPayId = "1119902161810"
    
    print("has attr rooms: ", hasattr(root, "rooms"))
    if not hasattr(root, "rooms"):
        root.rooms = BTrees.OOBTree.BTree()
    
    print("has attr users: ", hasattr(root, "users"))
    if not hasattr(root, "users"):
        root.users = BTrees.OOBTree.BTree()
        
    print("user id count: ", hasattr(root, "user_id_count"))
    if not hasattr(root, "user_id_count"):
        root.user_id_count = 0
        
    print("employee id list: ", hasattr(root, "employee_id_list"))
    if not hasattr(root, "employee_id_list"):
        root.employee_id_list = PersistentList()
        
    print("has attr logs: ", hasattr(root, "logs"))
    if not hasattr(root, "logs"):
        root.logs = BTrees.OOBTree.BTree()
        
    print("has attr log id count: ", hasattr(root, "log_id_count"))
    if not hasattr(root, "log_id_count"):
        root.log_id_count = 0
        
    print("has attr appointment", hasattr(root, "appointments"))
    if not hasattr(root, 'appointments'):
        root.appointments = BTrees.OOBTree.BTree()

    print("appointment id count", hasattr(root, "last_appointment_id"))
    if not hasattr(root, 'last_appointment_id'):
        root.last_appointment_id = 0
        
    print("appointment id list: ", hasattr(root, "appointment_id_list"))
    if not hasattr(root, "appointment_id_list"):
        root.appointment_id_list = PersistentList()
        
    print("has attr reports: ", hasattr(root, "reports"))
    if not hasattr(root, "reports"):
        root.reports = BTrees.OOBTree.BTree()
        
    print("report id count: ", hasattr(root, "report_id_count"))
    if not hasattr(root, "report_id_count"):
        root.report_id_count = 0
        
    print("has attr medicines: ", hasattr(root, "medicines"))
    if not hasattr(root, "medicines"):
        root.medicines = BTrees.OOBTree.BTree()
        
    print("has attr current_medicine_selected: ", hasattr(root, "current_medicine_selected"))
    if not hasattr(root, "current_medicine_selected"):
        root.current_medicine_selected = PersistentList()
        
    print("has attr current_service_selected: ", hasattr(root, "current_service_selected"))
    if not hasattr(root, "current_service_selected"):
        root.current_service_selected = PersistentList()

    root.current_medicine_selected = []
    root.current_service_selected = []

    def printInfo():
        print("user id count: ", root.user_id_count)
        print("employee id list: ", root.employee_id_list)
        print("appointmen id list: ", root.appointment_id_list)
        for user in root.users.values():
            print(user.get_id(), user.__class__.__name__ ,user.fname, user.password)
            # if user.role == "Doctor":
            # print(type(user.salary))
        print("log id count: ", root.log_id_count)
        print("reports id count: ", root.report_id_count)
# def print_all_doctor_appointments():
        # for user_id, user in root.users.items():
        # if isinstance(user, Doctor):
            # print(f"Doctor: {user.fname} {user.lname} (ID: {user_id}) has the following appointments:")
            # for appointment_id in user.get_appointments():
                # appointment = root.appointments.get(appointment_id)
                # if appointment:
                    # print(f" Appointment ID: {appointment_id}, Date: {appointment.date}, Start Time:{appointment.start_time}, End Time: {appointment.end_time}, Patient ID: {appointment.patient}")
                # else:
                    # print(" Appointment not found.")
                # print()

# def print_all_patient_appointments():
        # for user_id, user in root.users.items():
        # if isinstance(user, Patient):
            # print(f"Patient: {user.fname} {user.lname} (ID: {user_id}) has the following appointments:")
            # for appointment_id in user.get_appointments():
                # appointment = root.appointments.get(appointment_id)
                # if appointment:
                    # print(f" Appointment ID: {appointment_id}, Date: {appointment.date}, Start Time:{appointment.start_time}, End Time: {appointment.end_time}, Doctor ID: {appointment.doctor}")
                # else:
                    # print(" Appointment not found.")
                # print()

def print_appointment_info():
    for appointment_id, appointment in root.appointments.items():
        print(f"Appointment ID: {appointment_id}")
        print(f"Date: {appointment.date}")
        print(f"Start Time: {appointment.start_time}")
        print(f"End Time: {appointment.end_time}")
        print(f"Doctor ID: {appointment.doctor}")
        if appointment.doctor.get_id() in root.users:
            print(f"Doctor Name: {appointment.doctor.fname} {appointment.doctor.lname}")
        else:
            print("Doctor ID not found in users")
        print(f"Confirmation: {appointment.confirm}")
        print(f"Patient ID: {appointment.patient} \n")

def delete_all_appointments():
    appointment_ids = list(root.appointments.keys())
    for appointment_id in appointment_ids:
        del root.appointments[appointment_id]
    transaction.commit()

    root.last_appointment_id = 0
    root.appointment_id_list = PersistentList()
    transaction.commit()

def clear_all_appointments():
    for user_id, user in root.users.items():
        if isinstance(user, Doctor) or isinstance(user, Patient):
            user.appointments = PersistentList()
            print(f"Cleared appointments for {user.__class__.__name__} ID: {user_id}")
            
    transaction.commit()
    print("All appointments cleared.")

def getPromptPayId():
    return root.promptPayId

def setPromptPayId(promptPayId):
    root.promptPayId = promptPayId
    transaction.commit()
    
def add_first_admin():
    root.user_id_count += 1
    admin = Admin("admin", "Admin1", "Admin1", "Admin1", "password", root.user_id_count, "Main Head", "Admin")
    root.users[root.user_id_count] = admin
    root.employee_id_list.append(root.user_id_count)
    transaction.commit()

def add_doctor(current_user, fname, lname, address, phone_number, password, department, specialty, degree, salary,working_time):
    root.user_id_count += 1
    specialty = specialty.split(",")
    doctor = Doctor(fname, lname, address, phone_number, password, root.user_id_count, department, "Doctor", specialty,
    degree, salary, working_time)
    root.users[root.user_id_count] = doctor
    root.employee_id_list.append(root.user_id_count)
    add_log_db(current_user, "added Doctor", doctor)
    transaction.commit()

def add_admin(current_user, fname, lname, address, phone_number, password, department):
    root.user_id_count += 1
    admin = Admin(fname, lname, address, phone_number, password, root.user_id_count, department, "Admin")
    root.users[root.user_id_count] = admin
    root.employee_id_list.append(root.user_id_count)
    add_log_db(current_user, "added Admin", admin)
    transaction.commit()

def add_nurse(current_user, fname, lname, address, phone_number, password, department, assigned_wards, qualifications,salary, working_time):
    root.user_id_count += 1
    assigned_wards = assigned_wards.split(",")
    nurse = Nurse(fname, lname, address, phone_number, password, root.user_id_count, department, "Nurse", assigned_wards,
    qualifications, salary, working_time)
    root.users[root.user_id_count] = nurse
    root.employee_id_list.append(root.user_id_count)
    add_log_db(current_user, "added Nurse", nurse)
    transaction.commit()

def add_patient(current_user, fname, lname, address, phone_number, password):
    root.user_id_count += 1
    patient = Patient(fname, lname, address, phone_number, password, root.user_id_count)
    root.users[root.user_id_count] = patient
    add_log_db(current_user, "added Patient", patient)
    transaction.commit()

def add_admin_if_no_admin():
    if len(root.employee_id_list) == 0:
        add_first_admin()

def add_doctor_if_no_doctor():
    if not any(isinstance(user, Doctor) for user in root.users.values()):
        print("Adding 5 doctors")
        add_doctor(root.users[1],"doctor1", "doe", "123 street", "1234567890", "password", "Surgery", "Heart,Brain", "MD",100000, "8:00-17:00")
        add_doctor(root.users[1],"doctor2", "doe", "123 street", "1234567890", "password", "Surgery", "Face", "DD",290000, "10:00-19:00")
        add_doctor(root.users[1],"doctor3", "doe", "123 street", "1234567890", "password", "Orthopedics", "Bone,Leg","MD", 150000, "12:00-21:00")
        add_doctor(root.users[1],"doctor4", "doe", "123 street", "1234567890", "password", "Orthopedics", "Leg,Skull","DD", 170000, "8:00-20:00")
        add_doctor(root.users[1],"doctor5", "doe", "123 street", "1234567890", "password", "Orthopedics", "Hand", "MD",120000, "8:00-14:00")
def add_nurse_if_no_nurse():
    if not any(isinstance(user, Nurse) for user in root.users.values()):
        print("Adding 5 nurses")
        add_nurse(root.users[1],"nurse1", "doe", "123 street", "1234567890", "password", "Cardiology", "1,2,3", "BSc",50000, "8:00-17:00")
        add_nurse(root.users[1],"nurse2", "doe", "123 street", "1234567890", "password", "Neurology", "4,5,6", "BSc",60000, "11:00-20:00")
        add_nurse(root.users[1],"nurse3", "doe", "123 street", "1234567890", "password", "Orthopedics", "7,8,9", "BSc",45000, "8:00-24:00")
        add_nurse(root.users[1],"nurse4", "doe", "123 street", "1234567890", "password", "Orthopedics", "10,11,12", "BSc",40000, "8:00-19:00")
        add_nurse(root.users[1],"nurse5", "doe", "123 street", "1234567890", "password", "Orthopedics", "13,14,15", "BSc",30000, "5:00-23:00")
def add_patient_if_no_patient():
    if not any(isinstance(user, Patient) for user in root.users.values()):
        print("Adding 3 patients")
        add_patient(root.users[1],"p1", "doe", "123 street", "1234567890", "password")
        add_patient(root.users[1],"patient2", "doe", "123 street", "1234567890", "password")
        add_patient(root.users[1],"patient3", "doe", "123 street", "1234567890", "password")

def add_medicine_if_no_medicine():
    if not any(isinstance(medicine, Medicine) for medicine in root.medicines.values()):
        print("Adding 6 medicines")
        add_medicine_db("u4083", "Parazetamol", "For fever", 100, "2 weeks", "after breakfast", 10)
        add_medicine_db("gg083", "Sara", "For headache", 200, "1 week", "before sleep", 20)
        add_medicine_db("ki083", "Serphony", "For cold", 300, "3 days", "2 capsule before dinner", 30)
        add_medicine_db("lo083", "Tyraxynl", "For cough", 400, "1 week", "after breakfast", 40)
        add_medicine_db("pou03", "Polymorzync", "For stomach pain", 500, "2 weeks", "when have fever", 50)
        add_medicine_db("uu083", "Gyhofrewoqy", "For body pain", 600, "1 week", "3 capsule before dinner", 60)

def add_report_if_no_report():
    if not any(isinstance(report, Report) for report in root.reports.values()):
        print("Adding 2 reports to patient 1 and 1 report to patient 2")
        patient1 = get_patient_by_name("p1")
        patient2 = get_patient_by_name("patient2")

        medical_record_1 = MedicalRecord(180, 80, "male", 80, 120, "none", "Headage", "Having High Headage pain", "loremipsum dolor sit amet consectetuer adipiscing elit")
    bill = Bill(10)
    service_1 = Service("Checking", 100, 10, "Thai Care", 50)
    service_2 = Service("X-ray", 100, 10, "Thai Care", 50)
    medicine_1 = Medicine("u4083", "Parazetamol", "For fever", 100, "2 weeks", "after breakfast", 10)
    medicine_2 = Medicine("gg083", "Sara", "For headache", 200, "1 week", "before sleep", 20)
    # bill.setServices([service_1, service_2])
    # bill.setMedicines([medicine_1, medicine_2])
    bill.addService(service_1)
    bill.addService(service_2)
    bill.addMedicine(medicine_1)
    bill.addMedicine(medicine_2)
    for service in bill.services:
        print(service.name)
    add_report(patient1.get_id(), root.users[2], medical_record_1, bill)
    add_report(patient2.get_id(), root.users[2], medical_record_1, bill)
    bill_2 = Bill(20)
    medical_record_2 = MedicalRecord(180, 80, "male", 80, 120, "none", "Stomachage", "Having High Stomach pain","lorem ipsum dolor sit amet consectetuer adipiscing elit")
    bill_2.setServices([service_1])
    bill_2.setMedicines([medicine_1])
    add_report(patient1.get_id(), root.users[2], medical_record_2, bill_2)

def authenticate_user_db(username, password):
    for user in root.users.values():
        if user.get_fname() == username:
            if user.verify_password(password):
                current_user = user
                add_log_db(current_user, "logged in", current_user)
                return current_user
    return None
