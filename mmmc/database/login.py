# from pathlib import Path
# import logging
# import datetime
# import sqlite3
# logging.basicConfig(level=logging.DEBUG)

# class AdminLogin():
    
#     def __init__(self):
#         self.db_path = Path(__file__).parent / "portfolio.db"
#         self.conn = sqlite3.connect(self.db_path)
#         self.conn_cursor = self.conn.cursor()
#         self.admin_details_table = "admin_details"

#     def _commit_data(self):
#         """Commits data to the database (does NOT close connection)."""
#         try:
#             self.conn.commit()
#         except Exception as e:
#             raise sqlite3.DatabaseError

#     def _insert_password(self, password:str) -> dict:
#         """Insert hashed password into database"""
#         query = f"INSERT INTO {self.admin_details_table} (password) VALUES(?);"
#         try:
#             self.conn_cursor.execute(query, (password,))
#             self._commit_data()
#         except sqlite3.DatabaseError as e:
#             return {"message": f"Couldn't insert data, please try again", "state": False}
#         except sqlite3.DataError as e:
#             return {"message": f"Data error - Enter required information properly", "state": False}
#         except Exception as e:
#             return {"message": f"An error occurred - Please try again", "state": False}
        
#     def _get_password_or_email(self, request:str) -> str:
#         if request.strip().lower() == "password":
#             query = f"SELECT password FROM {self.admin_details_table};"
#             try:
#                 self.conn_cursor.execute(query)
#                 password = self.conn_cursor.fetchone()[0]
#                 return password
#             except sqlite3.DatabaseError as e:
#                     return {"message": f"Database could be locked, please try again", "state": False}
#             except sqlite3.DataError as e:
#                     return {"message": f"Data error", "state": False}
#             except Exception as e:
#                     return {"message": f"An error occurred - Please try again", "state": False}
#         elif request.strip().lower() == "email":
#             query = f"SELECT email FROM {self.admin_details_table};"
#             try:
#                 self.conn_cursor.execute(query)
#                 password = self.conn_cursor.fetchone()[0]
#                 return password
#             except sqlite3.DatabaseError as e:
#                     print(e)
#                     return {"message": f"Database could be locked, please try again", "state": False}
#             except sqlite3.DataError as e:
#                     return {"message": f"Data error", "state": False}
#             except Exception as e:
#                     return {"message": f"An error occurred - Please try again", "state": False}
        
#     def update_password(self, old_password:str, new_password:str) -> dict:
#         """Update password"""

#         password = self._get_password_or_email(request="password")
#         if password == old_password:
#             query = f"""UPDATE admin_details
#                     SET password = ? WHERE password = ?;"""
#             try:
#                 self.conn_cursor.execute(query, (new_password, old_password))
#                 self._commit_data()
#                 return {"message": "Successful - password updated", "state": True}
#             except sqlite3.DatabaseError as e:
#                 return {"message": f"Database could be locked, please try again", "state": False}
#             except sqlite3.DataError as e:
#                 return {"message": f"Data error", "state": False}
#             except Exception as e:
#                 return {"message": f"An error occurred - Please try again", "state": False}
#         else:
#             return {"message": f"Please enter the correct current password", "state": False}
        
#     def _insert_email(self, email:str) -> dict:
#         """insert password"""
#         query = f"INSERT INTO {self.admin_details_table} (email) VALUES(?);"
#         try:
#             self.conn_cursor.execute(query, (email,))
#             self._commit_data()
#         except sqlite3.DatabaseError as e:
#             return {"message": f"Couldn't insert data, please try again", "state": False}
#         except sqlite3.DataError as e:
#             return {"message": f"Data error - Enter required information properly", "state": False}
#         except Exception as e:
#             return {"message": f"An error occurred - Please try again", "state": False}
        
#     def update_email(self, old_email:str, new_email:str) -> str:
#         """Update exsiting email"""
#         email = self._get_password_or_email(request="email")

#         if email == old_email:
#             query = f"""UPDATE admin_details
#                     SET email = ? WHERE email = ?;"""
#             try:
#                 self.conn_cursor.execute(query, (new_email, old_email))
#                 self._commit_data()
#                 return {"message": "Successful - email updated", "state": True}
#             except sqlite3.DatabaseError as e:
#                 return {"message": f"Database could be locked, please try again", "state": False}
#             except sqlite3.DataError as e:
#                 return {"message": f"Data error", "state": False}
#             except Exception as e:
#                 return {"message": f"An error occurred - Please try again", "state": False}
#         else:
#             return {"message": f"Please enter the correct current email", "state": False}
        

# if __name__ == "__main__":
#     adminLogin = AdminLogin()

#     # new_password = f"scrypt:32768:8:1$U7qLiH3IkPJryVMX$9242b280aac247e6761f1c6e786182196f4ad669015cfa46c988ad7d42a3a3c740efd4d9bf0283079bcbc862eec9e3141bd8a17530d55fc0f24e41d7f9c01728"
#     # old_password = adminLogin._get_password_or_email(request="password")

#     # res = adminLogin.update_password(old_password, new_password)
#     # print(res)
#     # # res = adminLogin.update_password("1234", "2468")
#     # # print(res)   
#     # # res = adminLogin.update_email("khona6047@gmail.com", "khona6047@gmail.com")
#     # # print(res)

#     res1 = adminLogin._get_password_or_email(request="email")
#     res2 = adminLogin._get_password_or_email(request="password")
#     print(res1)
#     print(res2)

from pathlib import Path
import sqlite3


class AdminLogin:

    def __init__(self):
        self.db_path = Path(__file__).parent / "portfolio.db"
        self.admin_details_table = "admin_details"

    def _get_connection(self):
        """Creates a NEW SQLite connection per call — thread-safe."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # ===========================
    # INSERT PASSWORD
    # ===========================
    def _insert_password(self, password: str) -> dict:
        query = f"INSERT INTO {self.admin_details_table} (password) VALUES (?)"
        try:
            with self._get_connection() as conn:
                conn.execute(query, (password,))
            return {"message": "Password inserted", "state": True}
        except Exception:
            return {"message": "Couldn't insert password", "state": False}

    # ===========================
    # GET PASSWORD OR EMAIL
    # ===========================
    def _get_password_or_email(self, request: str) -> str | dict:
        if request.lower() == "password":
            query = f"SELECT password FROM {self.admin_details_table} LIMIT 1"
        else:
            query = f"SELECT email FROM {self.admin_details_table} LIMIT 1"

        try:
            with self._get_connection() as conn:
                row = conn.execute(query).fetchone()
                return row[0] if row else None
        except Exception:
            return {"message": "Error accessing data", "state": False}

    # ===========================
    # UPDATE PASSWORD
    # ===========================
    def update_password(self, old_password: str, new_password: str) -> dict:
        current = self._get_password_or_email("password")

        if current != old_password:
            return {"message": "Incorrect current password", "state": False}

        query = f"UPDATE {self.admin_details_table} SET password=? WHERE password=?"
        try:
            with self._get_connection() as conn:
                conn.execute(query, (new_password, old_password))
            return {"message": "Password updated", "state": True}
        except Exception:
            return {"message": "Couldn't update password", "state": False}

    # ===========================
    # INSERT EMAIL
    # ===========================
    def _insert_email(self, email: str) -> dict:
        query = f"INSERT INTO {self.admin_details_table} (email) VALUES (?)"
        try:
            with self._get_connection() as conn:
                conn.execute(query, (email,))
            return {"message": "Email inserted", "state": True}
        except Exception:
            return {"message": "Couldn't insert email", "state": False}

    # ===========================
    # UPDATE EMAIL
    # ===========================
    def update_email(self, old_email: str, new_email: str) -> dict:
        current = self._get_password_or_email("email")

        if current != old_email:
            return {"message": "Incorrect current email", "state": False}

        query = f"UPDATE {self.admin_details_table} SET email=? WHERE email=?"
        try:
            with self._get_connection() as conn:
                conn.execute(query, (new_email, old_email))
            return {"message": "Email updated", "state": True}
        except Exception:
            return {"message": "Couldn't update email", "state": False}
