import sqlite3
import atexit
import sys

# dto


class hat(object):
    def __init__(self, id, topping, supplier, quantity):
        self.id = id
        self.topping = topping
        self.supplier = supplier
        self.quantity = quantity


class supplier(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name


class order(object):
    def __init__(self, id, location, hat):
        self.id = id
        self.location = location
        self.hat = hat

# functions dte


class _hats:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, hat):
        self._conn.execute("INSERT INTO hats(id, topping, supplier, quantity) VALUES (?,?,?,?)", [
                           hat.id, hat.topping, hat.supplier, hat.quantity])

    def find(self, topping):
        c = self._conn.cursor()
        c.execute(
            "SELECT id, topping, supplier, quantity FROM hats WHERE topping = ?", [topping])
        return_hat = c.fetchone()
        if return_hat == None:
            return None
        else:
            return hat(*return_hat)

    def findall(self, topping):
        c = self._conn.cursor()
        c.execute(
            "SELECT id, topping, supplier, quantity FROM hats WHERE topping = ?", [topping])
        return c.fetchall()

    def orderhat(self, id):  # order the hats
        hattoorder = self.find(id)
        self._conn.execute("UPDATE hats SET quantity = ? WHERE id = ?", [
            hattoorder.quantity-1, hattoorder.id])
        if(hattoorder.quantity-1 == 0):
            self._conn.execute(
                "DELETE FROM hats WHERE id=?", [hattoorder.id])


class _suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("INSERT INTO suppliers(id, name) VALUES (?,?)", [
                           supplier.id, supplier.name])

    def find(self, id):
        c = self._conn.cursor()
        c.execute("SELECT id,name FROM suppliers WHERE id = ?", [id])
        return supplier(*c.fetchone())


class _orders:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, order):
        self._conn.execute("INSERT INTO orders(id, location, hat) VALUES (?,?,?)", [
                           order.id, order.location, order.hat])

    def find(self, id):
        c = self._conn.cursor()
        c.execute("SELECT id,location,hat FROM orders WHERE id = ?", [id])
        return order(*c.fetchone())


class _repository(object):
    def __init__(self, database):
        self._conn = sqlite3.connect(database)
        self.hats = _hats(self._conn)
        self.suppliers = _suppliers(self._conn)
        self.orders = _orders(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE suppliers(id INTEGER PRIMARY KEY, name STRING NOT NULL);
        CREATE TABLE hats(id INTEGER PRIMARY KEY, topping STRING NOT NULL, supplier INTEGER REFERENCES suppliers(id), quantity INTEGER NOT NULL);
        CREATE TABLE orders(id INTEGER PRIMARY KEY, loction STRING NOT NULL, hat INTEGER REFERENCES hats(id))""")


repo = _repository(sys.argv[4])
repo.create_tables()
atexit.register(repo._close)  # when we close the program
