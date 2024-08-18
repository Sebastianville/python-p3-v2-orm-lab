from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    @property 
    def year(self):
        return self._year 
    @year.setter
    def year(self, value):
        if isinstance(value, int) and value >= 2000:
            self._year = value 
        else: 
            raise ValueError('Number is less than 2000')


    @property 
    def summary(self):
        return self._summary 
    @summary.setter
    def summary(self, value):
        if isinstance(value, str ) and len(value) > 0:
            self._summary = value 
        else: 
            raise ValueError('Summary should not be empty')
    
    @property
    def employee_id(self):
        return self._employee_id
    @employee_id.setter
    def employee_id(self, value):
        if isinstance(value, int) and Employee.find_by_id(value):
            self._employee_id = value
        else:
            raise ValueError("Employee ID must be the ID of an existing Employee instance.")

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        try: 
            # Insert a new row with the year, summary, and employee_id
            sql=  """
                INSERT INTO reviews (year, summary, employee_id) VALUES(?, ?, ?);
            """
            CURSOR.execute(sql, (self.year, self.summary, self.employee_id  ))
            CONN.commit()
            # Get the ID of the newly inserted row 
            self.id=CURSOR.lastrowid
            Review.all[self.id] = self 
        
        except Exception as x: 
            print(f'something went wrong: {x}')

    @classmethod
    def create(cls, year, summary, employee_id):
        review = cls(year, summary, employee_id)
        review.save()
        return review 
        
   
    @classmethod
    def instance_from_db(cls, row):
        review = cls(
            id = row[0],
            year = row[1],
            summary = row[2],
            employee_id = row[3]
        )
        return review 

        
   

    @classmethod
    def find_by_id(cls, id):
        sql= """ SELECT * FROM reviews WHERE id=? """
        row = CURSOR.execute(sql, (id, )).fetchone()
        if not row: 
            return None
        else: 
            return cls.instance_from_db(row)

    def update(self):
        sql= """UPDATE reviews SET year=?, summary=?, employee_id=? WHERE id=?;"""
        CURSOR.execute(sql, (self.year, self.summary, self.employee_id, self.id))
        CONN.commit()

    def delete(self):
        sql = """DELETE FROM reviews WHERE id=?;"""
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        # Remove the instance from the all dictionary
        if self.id in Review.all: 
            del Review.all[self.id]
            self.id = None
        else: 
            print("Instance has no ID, it might")

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM reviews;"
        reviews = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in CURSOR.execute(sql).fetchall()]

