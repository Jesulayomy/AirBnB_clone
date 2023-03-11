import unittest
import os
from datetime import datetime
from models import storage
from models.city import City


class CityTest(unittest.TestCase):
    """ A class to test the City class """

    def test_city1(self):
        """ Test city """

        c1 = City()

        # test default types
        self.assertEqual(len(c1.id), 36)
        self.assertTrue(type(c1.created_at) is datetime)
        self.assertTrue(type(c1.updated_at) is datetime)
        self.assertTrue(type(c1.state_id) is str)
        self.assertTrue(type(c1.name) is str)
        self.assertTrue(c1.created_at == c1.updated_at)

    def test_city2(self):
        """ test city """

        c1 = City()

        # test default values
        self.assertEqual(c1.state_id, "")
        self.assertEqual(c1.name, "")

    def test_city3(self):
        """ Test city model """

        c1 = City()
        c1.state_id = "1234"
        c1.name = "city1"

        self.assertTrue(type(c1.id) is str)
        self.assertEqual(c1.state_id, "1234")
        self.assertEqual(c1.name, "city1")

    def test_city_args(self):
        """ Test city model with args """

        c1 = City(1, 3)  # 1 and 3 will be ignored

        # Test that id exist and is not 1 or 3
        self.assertTrue(c1.id is not None)
        self.assertTrue(c1.id != 1)
        self.assertTrue(c1.id != 3)

        # Test that created_at exist and is not 1 or 3
        self.assertTrue(c1.created_at is not None)
        self.assertTrue(c1.created_at != 1)
        self.assertTrue(c1.created_at != 3)

        # Test that updated_at exist and is not 1 or 3
        self.assertTrue(c1.updated_at is not None)
        self.assertTrue(c1.updated_at != 1)
        self.assertTrue(c1.updated_at != 3)

    def test_city_kwargs(self):
        """ test city with kwargs """

        c1 = City()
        c1.name = "city1"
        c1_dict = c1.to_dict()
        c2 = City(**c1_dict)

        self.assertEqual(c1.id, c2.id)
        self.assertEqual(c1.created_at, c2.created_at)
        self.assertEqual(c1.updated_at, c2.updated_at)
        self.assertEqual(c1.name, c2.name)
        self.assertTrue(c1 is not c2)

    def test_city_str(self):
        """ test __str__ method of city """

        c1 = City()
        out_str = "[{}] ({}) {}".format(
                 c1.__class__.__name__, c1.id, c1.__dict__
                )

        self.assertEqual(c1.__str__(), out_str)

    def test_city_save(self):
        """ test the save method of city """

        c1 = City()

        # test that created_at and updated_at attributes are same
        self.assertEqual(c1.created_at, c1.updated_at)

        c1.save()  # saves c1 to file. Now updated_at will be different
        self.assertTrue(c1.created_at != c1.updated_at)

        fileName = "file.json"
        # test that file.json exists
        self.assertTrue(os.path.exists(fileName))
        # test that file.json is a file
        self.assertTrue(os.path.isfile(fileName))

    def test_city_save_args(self):
        """ test the save method with args """

        c1 = City()

        with self.assertRaises(TypeError):
            c1.save(1, 2)

    def test_city_to_dict1(self):
        """ test the to_dict method """

        c1 = City()
        c1.name = "city1"
        c1_dict = c1.to_dict()
        dict_attrs = ["__class__", "updated_at", "created_at", "id", "name"]

        self.assertTrue(type(c1_dict) is dict)
        for attr in dict_attrs:
            self.assertTrue(attr in c1_dict)

    def test_city_to_dict2(self):
        """ test the to_dict method """

        c1 = City()
        c1.state_id = "1234"
        c1.name = "city1"
        c1_dict = c1.to_dict()

        # test that updated_at and created_at was converted to strings
        self.assertTrue(type(c1_dict["updated_at"] is str))
        self.assertTrue(type(c1_dict["created_at"] is str))

        # test that __class__stores the correct class name
        self.assertEqual(c1_dict["__class__"], "City")

        self.assertEqual(c1.state_id, c1_dict["state_id"])
        self.assertEqual(c1.name, c1_dict["name"])

    def test_city_to_dict_args(self):
        """ test the to_dict method with args """

        c1 = City()

        with self.assertRaises(TypeError):
            c1.to_dict("h")
