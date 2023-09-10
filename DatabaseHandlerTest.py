import unittest
from DatabaseHandler import DatabaseHandler


class DatabaseConnectorTest(unittest.TestCase):

    def test_DatabaseConnection(self):
        db = DatabaseHandler()
        db.connect()
        self.assertTrue(db.conn.closed == 0)
        db.disconnect()

    def test_DatabaseDisconnect(self):
        db = DatabaseHandler()
        db.connect()
        db.disconnect()
        self.assertFalse(db.conn.close == 0)
        
if __name__ == '__main__':
    unittest.main()
