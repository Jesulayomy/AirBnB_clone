import unittest
import os
from datetime import datetime
from models import storage
from models.base_model import BaseModel


class BaseModelTest(unittest.TestCase):
    """ A class to test the BaseModel class """

    def test_base1(self):
        """ Test base model """

        b1 = BaseModel()

        self.assertEqual(len(b1.id), 36)
        self.assertTrue(type(b1.created_at) is datetime)
        self.assertTrue(type(b1.updated_at) is datetime)
        self.assertTrue(b1.created_at == b1.updated_at)

    def test_base2(self):
        """ Test base model """

        b1 = BaseModel()
        b1.name = "Model1"
        b1.num = 72

        self.assertTrue(type(b1.id) is str)
        self.assertEqual(b1.name, "Model1")
        self.assertEqual(b1.num, 72)

    def test_base_args(self):
        """ Test base model with args """

        b1 = BaseModel(1, 3)  # 1 and 3 will be ignored

        # Test that id exist and is not 1 or 3
        self.assertTrue(b1.id is not None)
        self.assertTrue(b1.id != 1)
        self.assertTrue(b1.id != 3)

        # Test that created_at exist and is not 1 or 3
        self.assertTrue(b1.created_at is not None)
        self.assertTrue(b1.created_at != 1)
        self.assertTrue(b1.created_at != 3)

        # Test that updated_at exist and is not 1 or 3
        self.assertTrue(b1.updated_at is not None)
        self.assertTrue(b1.updated_at != 1)
        self.assertTrue(b1.updated_at != 3)

    def test_base_kwargs(self):
        """ test base with kwargs """

        b1 = BaseModel()
        b1_dict = b1.to_dict()
        b2 = BaseModel(**b1_dict)

        self.assertEqual(b1.id, b2.id)
        self.assertEqual(b1.created_at, b2.created_at)
        self.assertEqual(b1.updated_at, b2.updated_at)
        self.assertTrue(b1 is not b2)

    def test_base_str(self):
        """ test __str__ method of base """

        b1 = BaseModel()
        out_str = "[{}] ({}) {}".format(
                 b1.__class__.__name__, b1.id, b1.__dict__
                )

        self.assertEqual(b1.__str__(), out_str)

    def test_base_save(self):
        """ test the save method of base """

        b1 = BaseModel()

        # test that created_at and updated_at attributes are same
        self.assertEqual(b1.created_at, b1.updated_at)

        b1.save()  # saves b1 to file. Now updated_at will be different
        self.assertTrue(b1.created_at != b1.updated_at)

        fileName = "file.json"
        # test that file.json exists
        self.assertTrue(os.path.exists(fileName))
        # test that file.json is a file
        self.assertTrue(os.path.isfile(fileName))

        os.remove("file.json")

    def test_base_save_args(self):
        """ test the save method with args """

        b1 = BaseModel()

        with self.assertRaises(TypeError):
            b1.save(1, 2)

    def test_base_to_dict1(self):
        """ test the to_dict method """

        b1 = BaseModel()
        b1_dict = b1.to_dict()
        dict_attrs = ["__class__", "updated_at", "created_at", "id"]

        self.assertTrue(type(b1_dict) is dict)
        for attr in dict_attrs:
            self.assertTrue(attr in b1_dict)

    def test_base_to_dict2(self):
        """ test the to_dict method """

        b1 = BaseModel()
        b1.name = "MyModel1"
        b1.num = 72
        b1_dict = b1.to_dict()

        # test that updated_at and created_at was converted to strings
        self.assertTrue(type(b1_dict["updated_at"] is str))
        self.assertTrue(type(b1_dict["created_at"] is str))

        # test that __class__stores the correct class name
        self.assertEqual(b1_dict["__class__"], "BaseModel")

        self.assertEqual(b1.name, b1_dict["name"])
        self.assertEqual(b1.num, b1_dict["num"])

    def test_base_to_dict_args(self):
        """ test the to_dict method with args """

        b1 = BaseModel()

        with self.assertRaises(TypeError):
            b1.to_dict("h")
