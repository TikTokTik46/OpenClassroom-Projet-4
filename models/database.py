from tinydb import TinyDB, Query


class Database:
    """Model representing the database"""

    def __init__(self, db_name):
        """Database initialization"""
        self.db = TinyDB(str(db_name) + '.json')

    def search(self, table_, var, val: str):
        """Search in a table all the line that fit with the value
        of one variable"""
        return self.db.table(table_).search(Query()[var] == val)

    def insert_db(self, object_):
        """Add an object in the database by using is serialized method"""
        table_ = str(object_.__class__.__name__)
        self.db.table(table_).insert(object_.serialize())

    def modify_db(self, table_, var, val: str, var_to_modify, new_val):
        """Modifies a variable of an object saved in the database"""
        self.db.table(table_).update({var_to_modify: new_val},
                                     Query()[var] == val)

    def info_table(self, table_):
        """Return all the data saved in a table"""
        return self.db.table(table_).all()
