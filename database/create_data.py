import sqlite3
import numpy as np
import io
import cv2


class DatabaseManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()


    def create_tables(self):
        self.cursor.executescript("""
                                
            CREATE TABLE EMPLOYEES (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME CHAR(30) NOT NULL,
                GENDER CHAR(10),
                BIRTH_YEAR INTEGER,
                POSITION TEXT NOT NULL,
                DEPARTMENT TEXT NOT NULL,
                FEATURE BLOB);
                                  
            CREATE TABLE ATTENDANCE (
                ID INTEGER PRIMARY KEY,
                ID_NV TEXT NOT NULL,
                DATE DATE NOT NULL,
                CHECK_IN_TIME TIME NOT NULL,
                CHECK_OUT_TIME TIME NOT NULL,
                FOREIGN KEY (ID)
                REFERENCES EMPLOYEES (ID_NV));
        """)
        self.conn.commit()

    def insert_into_employees(self, name, gender, birth_year, position, department, feature):
        self.cursor.execute("""
            INSERT INTO EMPLOYEES ( NAME, GENDER, BIRTH_YEAR, POSITION, DEPARTMENT, FEATURE)
            VALUES (?, ?, ?, ?, ?, ?)""", (name, gender, birth_year, position, department, feature))
        self.conn.commit()


    def select_all_from_employees(self):
        self.cursor.execute("SELECT * FROM EMPLOYEES")
        rows = self.cursor.fetchall()
        list_employees = []
        for row in rows:
            feature = np.frombuffer(row[6], dtype=np.float32)
            list_employees.append((row[0], row[1], feature))
        return list_employees


    def update_employee_name(self, id, new_name, new_position, new_department):
        self.cursor.execute("""
            UPDATE EMPLOYEES
            SET NAME = ?, POSITION = ?, DEPARTMENT = ?
            WHERE ID = ?""", (new_name, new_position, new_department, id))
        self.conn.commit()


    def select_from_attendance(self , id_nv, date):
        self.cursor.execute("SELECT * FROM ATTENDANCE WHERE ID_NV = ? AND DATE(DATE) = DATE(?)", (id_nv, date))
        rows = self.cursor.fetchall()
        return rows


    def insert_into_attendance(self, id_nv, date, check_in_time, check_out_time):
        self.cursor.execute("""
            INSERT INTO ATTENDANCE (ID_NV, DATE, CHECK_IN_TIME, CHECK_OUT_TIME)
            VALUES (?, ?, ?, ?)""", (id_nv, date, check_in_time, check_out_time))
        self.conn.commit()


    def update_attendance_date(self, id, new_date):
        self.cursor.execute("""
            UPDATE ATTENDANCE
            SET DATE = ?
            WHERE ID = ?""", (new_date, id))
        self.conn.commit()


    def update_attendance_check_out(self, id_nv, date, check_out_time):
        self.cursor.execute("""
            UPDATE ATTENDANCE
            SET CHECK_OUT_TIME = ?
            WHERE ID_NV = ? AND DATE = ?""", (check_out_time, id_nv, date))
        self.conn.commit()

    def update_attendance_check_in(self, id, date, check_in_time):
        self.cursor.execute("""
            UPDATE ATTENDANCE
            SET CHECK_IN_TIME = ?
            WHERE ID = ? AND DATE = ?""", (check_in_time, id, date))
        self.conn.commit()

        
    def delete_employee(self, employee_id):
        self.cursor.execute("""
            DELETE FROM EMPLOYEES
            WHERE ID = ?""", (employee_id,))
        self.conn.commit()


    def delete_all_rows_from_attendance(self):
        self.cursor.execute("DELETE FROM ATTENDANCE")
        self.conn.commit()


    def close_connection(self):
        self.conn.close()

#<<<<<<=== SỬ DỤNG LỚP DATABASE_MANAGER ===>>>>>>

db_manager = DatabaseManager('databases.db')
# db_manager.create_tables()
# db_manager = DatabaseManager('database/databases.db')
# db_manager.insert_into_employees('John Doe', 'Male', 1990, 'Manager', 'HR', , np.array([1, 2, 3, 4, 5], dtype=np.float32))
# db_manager.insert_into_attendance('3', '2024-05-10', '08:21:40', '17:02:09')
# db_manager.select_all_from_employees()
# db_manager.delete_all_rows_from_attendance()
# db_manager.update_employee_name(1, 'Hoàng Ngọc Phú','Nhân Viên','DEV')
# db_manager.update_attendance_date('9', '2024-04-10')
# db_manager.update_attendance_check_out('1', '2023-10-10 15:00:00')
# db_manager.update_attendance_check_in('4', '2024-04-05', '08:19:22')
# db_manager.delete_employee(1)
db_manager.close_connection()
