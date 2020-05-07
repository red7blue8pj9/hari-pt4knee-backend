from database import db


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def json(self):
        return {
                   "id": self.id,
                   "email": self.email
               }, 200

    # Method to save user to DB
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Method to remove user from DB
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Class method which finds user from DB by email

    @classmethod
    def find_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    # Class method which finds user from DB by id
    @classmethod
    def find_user_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


class TableModel(db.Model):
    __tablename__ = "data_table"
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(80), primary_key=True)
    create_time = db.Column(db.Date)
    modified_time = db.Column(db.Date)
    admin_user = db.Column(db.String(30))
    restriction_level = db.Column(db.Integer)

    def __init__(self, table_name, create_time, modified_time, admin_user, restriction_level):
        self.table_name = table_name
        self.create_time = create_time
        self.modified_time = modified_time,
        self.admin_user = admin_user,
        self.restriction_level = restriction_level

    def json(self):
        return {
            "id": self.id,
            "table_name": self.table_name,
            "create_time": self.create_time,
            "modified_time": self.modified_time,
            "admin_user": self.admin_user,
            "restriction_level": self.restriction_level
        }

    # Method to save table to DB
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Method to remove table from DB
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Class methods
    @classmethod
    def find_table_by_table_name(cls, table_name):
        return cls.query.filter_by(table_name=table_name).first()

    @classmethod
    def find_all_tables(cls):
        return cls.query.all()


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d")


class DateCount(db.Model):
    __tablename__ = "DATE_COUNT"
    START_DATE = db.Column(db.Date(), primary_key=True)
    DISTINCT_STUDY_ID = db.Column(db.Integer)
    DISTINCT_VISIT_ID = db.Column(db.Integer)
    TOT_COLUMNS = db.Column(db.Integer)

    def json(self):
        return {
            "TIME": dump_datetime(self.START_DATE),
            "DISTINCT_STUDY_ID": self.DISTINCT_STUDY_ID,
            "DISTINCT_VISIT_ID": self.DISTINCT_VISIT_ID,
            "TOT_COLUMNS": self.TOT_COLUMNS
        }

    @classmethod
    def find_all_values(cls):
        return cls.query.all()


class DateCountByMonth(db.Model):
    __tablename__ = "DATE_COUNT_BY_MONTH"
    YEAR = db.Column(db.Integer, primary_key=True)
    MONTH = db.Column(db.Integer, primary_key=True)
    DISTINCT_STUDY_ID = db.Column(db.Integer)
    DISTINCT_VISIT_ID = db.Column(db.Integer)
    TOT_COLUMNS = db.Column(db.Integer)

    def __init__(self, YEAR, MONTH, DISTINCT_STUDY_ID, DISTINCT_VISIT_ID, TOT_COLUMNS):
        self.YEAR = YEAR,
        self.MONTH = MONTH,
        self.DISTINCT_STUDY_ID = DISTINCT_STUDY_ID,
        self.DISTINCT_VISIT_ID = DISTINCT_VISIT_ID,
        self.TOT_COLUMNS = TOT_COLUMNS

    def json(self):
        return {
            "TIME": str(self.YEAR) + '-' + str(self.MONTH),
            "DISTINCT_STUDY_ID": self.DISTINCT_STUDY_ID,
            "DISTINCT_VISIT_ID": self.DISTINCT_VISIT_ID,
            "TOT_COLUMNS": self.TOT_COLUMNS
        }

    @classmethod
    def find_all_values(cls):
        return cls.query.all()


class DateCountByYear(db.Model):
    __tablename__ = "DATE_COUNT_BY_YEAR"
    YEAR = db.Column(db.Integer, primary_key=True)
    DISTINCT_STUDY_ID = db.Column(db.Integer)
    DISTINCT_VISIT_ID = db.Column(db.Integer)
    TOT_COLUMNS = db.Column(db.Integer)

    def json(self):
        return {
            "TIME": self.YEAR,
            "DISTINCT_STUDY_ID": self.DISTINCT_STUDY_ID,
            "DISTINCT_VISIT_ID": self.DISTINCT_VISIT_ID,
            "TOT_COLUMNS": self.TOT_COLUMNS
        }

    @classmethod
    def find_all_values(cls):
        return cls.query.all()


class ProcedureCategory(db.Model):
    __tablename__ = "PROC_CATE_COUNT"
    KNEE_PROC_CATE = db.Column(db.String, primary_key=True)
    DISTINCT_STUDY_ID = db.Column(db.Integer)

    def json(self):
        return {
            "KNEE_PROC_CATE": self.KNEE_PROC_CATE,
            "DISTINCT_STUDY_ID": self.DISTINCT_STUDY_ID
        }

    @classmethod
    def find_all_values(cls):
        return cls.query.all()


class ProcedureSubCategory(db.Model):
    __tablename__ = "PROC_SUBCATE_COUNT"
    KNEE_PROC_CATE = db.Column(db.String, primary_key=True)
    KNEE_PROC_SUBCATE = db.Column(db.String, primary_key=True)
    DISTINCT_STUDY_ID = db.Column(db.Integer)

    def json(self):
        return {
            "KNEE_PROC_CATE": self.KNEE_PROC_CATE,
            "KNEE_PROC_SUBCATE": self.KNEE_PROC_SUBCATE,
            "DISTINCT_STUDY_ID": self.DISTINCT_STUDY_ID
        }

    @classmethod
    def find_all_values(cls):
        return cls.query.all()
