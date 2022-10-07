from tinydb import TinyDB, Query


class Database:

    def __init__(self, db_name):
        self.db = TinyDB(str(db_name) + '.json')
        self.q = Query()

    def clean_db(self, table_):
        self.db.table(table_).truncate()

    def search_1(self, table_, var, val):
        return self.db.table(table_).search(self.q[var] == val)

    def search_value_with_id(self, table_, id_, var):
        return self.db.table(table_).search(self.q["id"] == id_)[0][var]

    def search_2(self, table_, var_1, val_1, var_2, val_2):
        return self.db.table(table_).search((self.q[var_1] == val_1) & (self.q[var_2] == val_2))

    def insert_db(self, object_):
        table_ = str(object_.__class__.__name__)
        self.db.table(table_).insert(object_.serialize())

    def modify_db(self, table_, var, val, var_to_modify, new_val):
        self.db.table(table_).update({var_to_modify: new_val}, self.q[var] == val)

    def info_all(self):
        return self.db.all()

    def info_table(self, table_):
        return self.db.table(table_).all()
