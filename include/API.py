import pinfo
import Database

class DB_factory():
    plain_text_DB = "plain text DB";
    SQL = "SQL";
    LiteSQL = "LiteSQL";
    MySQL = "MySQL";

    def __init__():
        pass

    @staticmethod
    def create(which_DB: str):
        if which_DB == DB_factory.plain_text_DB:
            return Database.Plain_text_DB_t()
        return None

class DB_API:
    def __init__(self):
        self.DB = None
        
    def load_info(self, UID: str):
        return self.DB.require_by_UID(UID)

    def write_back(self, UID: str, patient_info: pinfo.patient_info_t):
        self.DB.set_by_UID(UID, patient_info)

    def set_DB(self, DB: Database.meta_DB_t, DB_path: str):
        self.DB_path = DB_path
        self.DB = DB
        self.DB.set_DB_dir(DB_path)
        return self.DB.connect()

    def set_IDB(self, IDB: Database.meta_DB_t, DB_path: str):
        self.IDB_path = IDB_path
        self.IDB = IDB
        self.IDB.set_DB_dir(IDB_path)
        return self.IDB.connect()

def main():
    api = DB_API()
    api.set_DB(DB_factory.create(DB_factory.plain_text_DB), "../DB/central_DB")
    info = api.load_info("0001")
    print(str(info))

if __name__ == "__main__":
    main()
