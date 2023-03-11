import unittest
import os
from datetime import datetime
from models import storage
from models.state import State


class StateTest(unittest.TestCase):
    """ A class to test the State class """

    def test_state1(self):
        """ Test state """

        s1 = State()

        # test default types
        self.assertEqual(len(s1.id), 36)
        self.assertTrue(type(s1.created_at) is datetime)
        self.assertTrue(type(s1.updated_at) is datetime)
        self.assertTrue(type(s1.name) is str)
        self.assertTrue(s1.created_at == s1.updated_at)

    def test_state2(self):
        """ test state """

        s1 = State()

        # test default values
        self.assertEqual(s1.name, "")

    def test_state3(self):
        """ Test state model """

        s1 = State()
        s1.name = "state1"

        self.assertTrue(type(s1.id) is str)
        self.assertEqual(s1.name, "state1")

    def test_state_args(self):
        """ Test state model with args """

        s1 = State(1, 3)  # 1 and 3 will be ignored

        # Test that id exist and is not 1 or 3
        self.assertTrue(s1.id is not None)
        self.assertTrue(s1.id != 1)
        self.assertTrue(s1.id != 3)

        # Test that created_at exist and is not 1 or 3
        self.assertTrue(s1.created_at is not None)
        self.assertTrue(s1.created_at != 1)
        self.assertTrue(s1.created_at != 3)

        # Test that updated_at exist and is not 1 or 3
        self.assertTrue(s1.updated_at is not None)
        self.assertTrue(s1.updated_at != 1)
        self.assertTrue(s1.updated_at != 3)

    def test_state_kwargs(self):
        """ test state with kwargs """

        s1 = State()
        s1.name = "state1"
        s1_dict = s1.to_dict()
        s2 = State(**s1_dict)

        self.assertEqual(s1.id, s2.id)
        self.assertEqual(s1.created_at, s2.created_at)
        self.assertEqual(s1.updated_at, s2.updated_at)
        self.assertEqual(s1.name, s2.name)
        self.assertTrue(s1 is not s2)

    def test_state_str(self):
        """ test __str__ method of state """

        s1 = State()
        out_str = "[{}] ({}) {}".format(
                 s1.__class__.__name__, s1.id, s1.__dict__
                )

        self.assertEqual(s1.__str__(), out_str)

    def test_state_save(self):
        """ test the save method of state """

        s1 = State()

        # test that created_at and updated_at attributes are same
        self.assertEqual(s1.created_at, s1.updated_at)

        s1.save()  # saves s1 to file. Now updated_at will be different
        self.assertTrue(s1.created_at != s1.updated_at)

        fileName = "file.json"
        # test that file.json exists
        self.assertTrue(os.path.exists(fileName))
        # test that file.json is a file
        self.assertTrue(os.path.isfile(fileName))

        os.remove("file.json")

    def test_state_save_args(self):
        """ test the save method with args """

        s1 = State()

        with self.assertRaises(TypeError):
            s1.save(1, 2)

    def test_state_to_dict1(self):
        """ test the to_dict method """

        s1 = State()
        s1.name = "state1"
        s1_dict = s1.to_dict()
        dict_attrs = ["__class__", "updated_at", "created_at", "id", "name"]

        self.assertTrue(type(s1_dict) is dict)
        for attr in dict_attrs:
            self.assertTrue(attr in s1_dict)

    def test_state_to_dict2(self):
        """ test the to_dict method """

        s1 = State()
        s1.name = "state1"
        s1_dict = s1.to_dict()

        # test that updated_at and created_at was converted to strings
        self.assertTrue(type(s1_dict["updated_at"] is str))
        self.assertTrue(type(s1_dict["created_at"] is str))

        # test that __class__stores the correct class name
        self.assertEqual(s1_dict["__class__"], "State")

        self.assertEqual(s1.name, s1_dict["name"])

    def test_state_to_dict_args(self):
        """ test the to_dict method with args """

        s1 = State()

        with self.assertRaises(TypeError):
            s1.to_dict("h")
