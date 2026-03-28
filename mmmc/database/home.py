from pathlib import Path
import logging
import datetime
import sqlite3
logging.basicConfig(level=logging.DEBUG)

class HomePageDB():

    def __init__(self):
        self.db_path = Path(__file__).parent / "portfolio.db"
        self.conn = sqlite3.connect(self.db_path)
        self.conn_cursor = self.conn.cursor()
        self.home_table = "home"
        self.services_table = "services"

    def _commit_data(self):
        """Commits data to the database (does NOT close connection)."""
        try:
            self.conn.commit()
        except Exception as e:
            raise sqlite3.DatabaseError

    def _last_updated(self):
        """Updates the last_updated column"""
        query = f"""UPDATE home
                    SET last_updated = ? ;"""
        date = datetime.datetime.now()
        try:
            self.conn_cursor.execute(query, (date,))
            return
        except Exception as e:
            raise sqlite3.DatabaseError
        
    def _get_user_id(self) -> int:
        """retrieve the main users id"""
        query = f"""SELECT uid FROM home;"""
        try:
            self.conn_cursor.execute(query)
            uid = self.conn_cursor.fetchone()[0]
            return uid
        except Exception as e:
            raise sqlite3.Error
        
    def _create_user_name(self, name:str) -> dict:
        """Creates the name of the user"""

        query = f"""INSERT INTO home (name, last_updated)           VALUES(?,?);"""
        date = datetime.datetime.now()
        try:
            self.conn_cursor.execute(query, (name, date,))
            self._commit_data()
            return {"message": "Successful", "state": True}
        except Exception as e:
            return {"message": f"Unsuccessful - {e}", "state": False}
        
    def update_user_name(self, name:str) -> dict:
        """Update user's name"""
        query = f"""UPDATE home
                    SET name = ? WHERE uid = ?;"""
        uid = self._get_user_id()
        try:
            self.conn_cursor.execute(query, (name, uid,))
            self._last_updated()
            self._commit_data()
            return {"message": "Successful", "state": True}
        except Exception as e:
            logging.debug(f"Error {e}")
            return {"message": "Unsuccessful", "state": False}
    
    def update_short_about(self, about: str) -> dict:
        """Update the user's short about"""
        query = f"""UPDATE home
                    SET short_about = ? WHERE uid = ?;"""
        uid = self._get_user_id()
        try:
            self.conn_cursor.execute(query, (about, uid,))
            self._last_updated()
            self._commit_data()
            return {"message": "Successful", "state": True}
        except Exception as e:
            return {"message": "Unsuccessful", "state": False}
        
    def insert_service(self, service: str) -> dict:
        """Add a new service"""
        query = f"""INSERT INTO services VALUES(?, ?);"""
        uid = self._get_user_id()
        try:
            self.conn_cursor.execute(query, (service, uid))
            self._commit_data()
            return {"message": "Successful", "state": True}
        except Exception as e:
            logging.debug(e)
            return {"message": "Unsuccessful", "state": False}
        
    def update_service(self, new_service:str, old_service:str) -> dict:
        """Update existing service"""

        query = f"""UPDATE services 
                    SET service = ? WHERE service = ?;"""
        try:
            self.conn_cursor.execute(query, (new_service, old_service))
            self._commit_data()
            return {"message": "Successful", "state": True}
        except Exception as e:
            logging.debug(e)
            return {"message": f"Unsuccessful - {e}", "state": False}
        
        

if __name__ == "__main__":
   pass

