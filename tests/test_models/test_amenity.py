import unittest
import os
from datetime import datetime
from models import storage
from models.amenity import Amenity


class TestAmenityClass(unittest.TestCase):
    """ unittests for amenity class """

    def test_amenity_defaults(self):

        a1 = Amenity()

        self.assertEqual(len(a1.id), 36)
        self.assertTrue(isinstance(a1.created_at, datetime))
        self.assertTrue(isinstance(a1.updated_at, datetime))
        self.assertTrue(isinstance(a1.name, str))
        self.assertTrue(a1.created_at == a1.updated_at)

    def test_amenity_name(self):
        """ tests for name attribute of amenity class """

        a1 = Amenity()
        self.assertEqual(a1.name, "")

        a1.name = "Default"
        self.assertEqual(a1.name, "Default")

        d1 = {"name": "Simple"}
        a2 = Amenity(**d1)
        self.assertTrue(a2.name == "Simple")

        self.assertTrue(type(a1.name), str)
        self.assertTrue(type(a2.name), str)

    def test_amenity_id(self):
        """ tests for id attribute of amenity class """

        a1 = Amenity()

        self.assertTrue(len(a1.id), 32)
        self.assertTrue(type(a1.id), str)

    def test_amenity_datetimes(self):
        """ tests for datetime attributes of amenity class """

        a1 = Amenity()

        self.assertTrue(type(a1.created_at) is datetime)
        a1.updated_at = datetime.now()
        self.assertTrue(a1.created_at != a1.updated_at)

    def test_amenity_kwargs(self):
        """ tests for **kwargs in amenity (should be handled) """

        a1 = Amenity()
        d1 = a1.to_dict()
        a2 = Amenity(**d1)

        self.assertEqual(a1.id, a2.id)
        self.assertEqual(a1.created_at, a2.created_at)
        self.assertEqual(a1.updated_at, a2.updated_at)
        self.assertEqual(a1.name, a2.name)
        self.assertTrue(a1 is not a2)

    def test_amenity_args(self):
        """ tests for *args in amenity (should be ignored) """

        a1 = Amenity("Hello", "World", "Michael")

        self.assertEqual(a1.name, "")
        self.assertTrue(a1.id is not None)
        self.assertTrue(a1.id != "Hello")
        self.assertTrue(a1.name != "Hello")

    def test_amenity_str(self):
        """ test __str__ method of amenity """

        a1 = Amenity()
        out_str = "[{}] ({}) {}".format(
                a1.__class__.__name__, a1.id, a1.__dict__
                )

        self.assertEqual(a1.__str__(), out_str)

    def test_amenity_save(self):
        """ test the save method of amenity """

        a1 = Amenity()

        self.assertEqual(a1.created_at, a1.updated_at)

        a1.save()
        self.assertTrue(a1.created_at != a1.updated_at)

        fileName = "file.json"
        self.assertTrue(os.path.exists(fileName))
        self.assertTrue(os.path.isfile(fileName))

        os.remove("file.json")

    def test_amenity_save_args(self):
        """ test the save method with args """

        a1 = Amenity()

        with self.assertRaises(TypeError):
            a1.save(1, 2)

    def test_amenity_to_dict1(self):
        """ test the to_dict method """

        a1 = Amenity()
        a1.name = "amenity1"
        a1_dict = a1.to_dict()
        dict_attrs = ["__class__", "updated_at", "created_at", "id", "name"]

        self.assertTrue(type(a1_dict) is dict)

        for attr in dict_attrs:
            self.assertTrue(attr in a1_dict)

    def test_amenity_to_dict2(self):
        """ test the to_dict method """

        a1 = Amenity()
        a1.name = "amenity1"
        a1_dict = a1.to_dict()

        self.assertTrue(type(a1_dict["updated_at"] is str))
        self.assertTrue(type(a1_dict["created_at"] is str))

        self.assertEqual(a1_dict["__class__"], "Amenity")

        self.assertEqual(a1.name, a1_dict["name"])

    def test_amenity_to_dict_args(self):
        """ test the to_dict method with args """

        a1 = Amenity()

        with self.assertRaises(TypeError):
            a1.to_dict("hello world")
