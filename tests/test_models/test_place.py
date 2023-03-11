import unittest
import os
from datetime import datetime
from models import storage
from models.place import Place


class PlaceTest(unittest.TestCase):
    """ A class to test the Place class """

    def test_place1(self):
        """ Test place """

        p1 = Place()

        # testing default types
        self.assertEqual(len(p1.id), 36)
        self.assertTrue(type(p1.created_at) is datetime)
        self.assertTrue(type(p1.updated_at) is datetime)
        self.assertTrue(type(p1.city_id) is str)
        self.assertTrue(type(p1.user_id) is str)
        self.assertTrue(type(p1.name) is str)
        self.assertTrue(type(p1.description) is str)
        self.assertTrue(type(p1.number_rooms) is int)
        self.assertTrue(type(p1.number_bathrooms) is int)
        self.assertTrue(type(p1.max_guest) is int)
        self.assertTrue(type(p1.price_by_night) is int)
        self.assertTrue(type(p1.latitude) is float)
        self.assertTrue(type(p1.longitude) is float)
        self.assertTrue(type(p1.amenity_ids) is list)
        self.assertTrue(p1.created_at == p1.updated_at)

    def test_place2(self):
        """ test place model """

        p1 = Place()

        # testing default values
        self.assertEqual(p1.city_id, "")
        self.assertEqual(p1.user_id, "")
        self.assertEqual(p1.name, "")
        self.assertEqual(p1.description, "")
        self.assertEqual(p1.number_rooms, 0)
        self.assertEqual(p1.number_bathrooms, 0)
        self.assertEqual(p1.max_guest, 0)
        self.assertEqual(p1.price_by_night, 0)
        self.assertEqual(p1.latitude, 0.0)
        self.assertEqual(p1.longitude, 0.0)
        self.assertEqual(p1.amenity_ids, [])

    def test_place3(self):
        """ Test place model """

        p1 = Place()
        p1.city_id = "1223"
        p1.user_id = "11234"
        p1.name = "place1"
        p1.description = "describing"
        p1.number_rooms = 12
        p1.number_bathrooms = 13
        p1.max_guest = 4
        p1.price_by_night = 1000
        p1.latitude = 16.7
        p1.longitude = 12.2
        p1.amenity_ids = ["123", "112"]

        self.assertTrue(type(p1.id) is str)
        self.assertEqual(p1.city_id, "1223")
        self.assertEqual(p1.user_id, "11234")
        self.assertEqual(p1.name, "place1")
        self.assertEqual(p1.description, "describing")
        self.assertEqual(p1.number_rooms, 12)
        self.assertEqual(p1.number_bathrooms, 13)
        self.assertEqual(p1.max_guest, 4)
        self.assertEqual(p1.price_by_night, 1000)
        self.assertEqual(p1.latitude, 16.7)
        self.assertEqual(p1.longitude, 12.2)
        self.assertEqual(p1.amenity_ids, ["123", "112"])

    def test_place_args(self):
        """ Test place model with args """

        p1 = Place(1, 3)  # 1 and 3 will be ignored

        # Test that id exist and is not 1 or 3
        self.assertTrue(p1.id is not None)
        self.assertTrue(p1.id != 1)
        self.assertTrue(p1.id != 3)

        # Test that created_at exist and is not 1 or 3
        self.assertTrue(p1.created_at is not None)
        self.assertTrue(p1.created_at != 1)
        self.assertTrue(p1.created_at != 3)

        # Test that updated_at exist and is not 1 or 3
        self.assertTrue(p1.updated_at is not None)
        self.assertTrue(p1.updated_at != 1)
        self.assertTrue(p1.updated_at != 3)

    def test_place_kwargs(self):
        """ test place with kwargs """

        p1 = Place()
        p1.name = "place1"
        p1_dict = p1.to_dict()
        p2 = Place(**p1_dict)

        self.assertEqual(p1.id, p2.id)
        self.assertEqual(p1.created_at, p2.created_at)
        self.assertEqual(p1.updated_at, p2.updated_at)
        self.assertEqual(p1.name, p2.name)
        self.assertTrue(p1 is not p2)

    def test_place_str(self):
        """ test __str__ method of place """

        p1 = Place()
        out_str = "[{}] ({}) {}".format(
                 p1.__class__.__name__, p1.id, p1.__dict__
                )

        self.assertEqual(p1.__str__(), out_str)

    def test_place_save(self):
        """ test the save method of place """

        p1 = Place()

        # test that created_at and updated_at attributes are same
        self.assertEqual(p1.created_at, p1.updated_at)

        p1.save()  # saves p1 to file. Now updated_at will be different
        self.assertTrue(p1.created_at != p1.updated_at)

        fileName = "file.json"
        # test that file.json exists
        self.assertTrue(os.path.exists(fileName))
        # test that file.json is a file
        self.assertTrue(os.path.isfile(fileName))

    def test_place_save_args(self):
        """ test the save method with args """

        p1 = Place()

        with self.assertRaises(TypeError):
            p1.save(1, 2)

    def test_place_to_dict1(self):
        """ test the to_dict method """

        p1 = Place()
        p1.name = "place1"
        p1_dict = p1.to_dict()
        dict_attrs = ["__class__", "updated_at", "created_at", "id", "name"]

        self.assertTrue(type(p1_dict) is dict)
        for attr in dict_attrs:
            self.assertTrue(attr in p1_dict)

    def test_place_to_dict2(self):
        """ test the to_dict method """

        p1 = Place()
        p1.city_id = "1223"
        p1.user_id = "11234"
        p1.name = "place1"
        p1.description = "describing"
        p1.number_rooms = 12
        p1.number_bathrooms = 13
        p1.max_guest = 4
        p1.price_by_night = 1000
        p1.latitude = 16.7
        p1.longitude = 12.2
        p1.amenity_ids = ["123", "112"]
        p1_dict = p1.to_dict()

        # test that updated_at and created_at was converted to strings
        self.assertTrue(type(p1_dict["updated_at"] is str))
        self.assertTrue(type(p1_dict["created_at"] is str))

        # test that __class__stores the correct class name
        self.assertEqual(p1_dict["__class__"], "Place")

        self.assertEqual(p1.city_id, p1_dict["city_id"])
        self.assertEqual(p1.user_id, p1_dict["user_id"])
        self.assertEqual(p1.name, p1_dict["name"])
        self.assertEqual(p1.description, p1_dict["description"])
        self.assertEqual(p1.number_rooms, p1_dict["number_rooms"])
        self.assertEqual(p1.number_bathrooms, p1_dict["number_bathrooms"])
        self.assertEqual(p1.max_guest, p1_dict["max_guest"])
        self.assertEqual(p1.price_by_night, p1_dict["price_by_night"])
        self.assertEqual(p1.latitude, p1_dict["latitude"])
        self.assertEqual(p1.longitude, p1_dict["longitude"])
        self.assertEqual(p1.amenity_ids, p1_dict["amenity_ids"])

    def test_place_to_dict_args(self):
        """ test the to_dict method with args """

        p1 = Place()

        with self.assertRaises(TypeError):
            p1.to_dict("h")
