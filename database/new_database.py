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
                NAME CHAR(20) NOT NULL,
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


    def insert_into_employees(self, name, feature):
        self.cursor.execute("""
            INSERT INTO EMPLOYEES ( NAME, FEATURE)
            VALUES (?, ?)""", ( name, feature))
        self.conn.commit()


    def select_all_from_employees(self):
        self.cursor.execute("SELECT * FROM EMPLOYEES")
        rows = self.cursor.fetchall()
        list_employees = []
        for row in rows:
            feature = np.frombuffer(row[2], dtype=np.float32)
            list_employees.append((row[0], row[1], feature))
        return list_employees


    def update_employee_name(self, id, new_name):
        self.cursor.execute("""
            UPDATE EMPLOYEES
            SET NAME = ?
            WHERE ID = ?""", (new_name, id))
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
        

    def delete_all_rows_from_attendance(self):
        self.cursor.execute("DELETE FROM ATTENDANCE")
        self.conn.commit()


    def close_connection(self):
        self.conn.close()

#<<<<<<=== SỬ DỤNG LỚP DATABASE_MANAGER ===>>>>>>

# db_manager = DatabaseManager('database_new.db')
# db_manager = DatabaseManager('database/database_new.db')
# db_manager.create_tables()
# db_manager.insert_into_employees('Phu123456', np.array([1, 2, 3, 4, 5], dtype=np.float32))
# db_manager.insert_into_attendance('1', '2023-10-17', '08:25:32', '17:30:00')
# db_manager.select_all_from_employees()
# db_manager.delete_all_rows_from_attendance()
# db_manager.update_employee_name(4, 'Phú đẹp zai quê Thái Lọ')
# db_manager.update_attendance_date('2', '2023-10-18')
# db_manager.update_attendance_check_out('1', '2023-10-10 15:00:00')
# db_manager.close_connection()
