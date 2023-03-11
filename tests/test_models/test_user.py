import unittest
import os
from datetime import datetime
from models import storage
from models.user import User


class UserTest(unittest.TestCase):
    """ A class to test the User class """

    def test_user1(self):
        """ Test user """

        u1 = User()

        # test default types
        self.assertEqual(len(u1.id), 36)
        self.assertTrue(type(u1.created_at) is datetime)
        self.assertTrue(type(u1.updated_at) is datetime)
        self.assertTrue(type(u1.email) is str)
        self.assertTrue(type(u1.password) is str)
        self.assertTrue(type(u1.first_name) is str)
        self.assertTrue(type(u1.last_name) is str)
        self.assertTrue(u1.created_at == u1.updated_at)

    def test_user2(self):
        """ Test user """

        u1 = User()

        # test default values
        self.assertEqual(u1.email, "")
        self.assertEqual(u1.password, "")
        self.assertEqual(u1.first_name, "")
        self.assertEqual(u1.last_name, "")

    def test_user3(self):
        """ Test user model """

        u1 = User()
        u1.email = "user@mail.com"
        u1.password = "7224"
        u1.first_name = "user1"
        u1.last_name = "user last"

        self.assertTrue(type(u1.id) is str)
        self.assertEqual(u1.email, "user@mail.com")
        self.assertEqual(u1.password, "7224")
        self.assertEqual(u1.first_name, "user1")
        self.assertEqual(u1.last_name, "user last")

    def test_user_args(self):
        """ Test user model with args """

        u1 = User(1, 3)  # 1 and 3 will be ignored

        # Test that id exist and is not 1 or 3
        self.assertTrue(u1.id is not None)
        self.assertTrue(u1.id != 1)
        self.assertTrue(u1.id != 3)

        # Test that created_at exist and is not 1 or 3
        self.assertTrue(u1.created_at is not None)
        self.assertTrue(u1.created_at != 1)
        self.assertTrue(u1.created_at != 3)

        # Test that updated_at exist and is not 1 or 3
        self.assertTrue(u1.updated_at is not None)
        self.assertTrue(u1.updated_at != 1)
        self.assertTrue(u1.updated_at != 3)

    def test_user_kwargs(self):
        """ test user with kwargs """

        u1 = User()
        u1.email = "user@mail.com"
        u1.first_name = "user1"
        u1_dict = u1.to_dict()
        u2 = User(**u1_dict)

        self.assertEqual(u1.id, u2.id)
        self.assertEqual(u1.created_at, u2.created_at)
        self.assertEqual(u1.updated_at, u2.updated_at)
        self.assertEqual(u1.email, u2.email)
        self.assertEqual(u1.first_name, u2.first_name)
        self.assertTrue(u1 is not u2)

    def test_user_str(self):
        """ test __str__ method of user """

        u1 = User()
        out_str = "[{}] ({}) {}".format(
                 u1.__class__.__name__, u1.id, u1.__dict__
                )

        self.assertEqual(u1.__str__(), out_str)

    def test_user_save(self):
        """ test the save method of user """

        u1 = User()

        # test that created_at and updated_at attributes are same
        self.assertEqual(u1.created_at, u1.updated_at)

        u1.save()  # saves u1 to file. Now updated_at will be different
        self.assertTrue(u1.created_at != u1.updated_at)

        fileName = "file.json"
        # test that file.json exists
        self.assertTrue(os.path.exists(fileName))
        # test that file.json is a file
        self.assertTrue(os.path.isfile(fileName))

        os.remove("file.json")

    def test_user_save_args(self):
        """ test the save method with args """

        u1 = User()

        with self.assertRaises(TypeError):
            u1.save(1, 2)

    def test_user_to_dict1(self):
        """ test the to_dict method """

        u1 = User()
        u1.email = "user@mail.com"
        u1.first_name = "user1"
        u1_dict = u1.to_dict()
        dict_attrs = [
            "__class__", "updated_at",
            "created_at", "id",
            "email", "first_name"
        ]

        self.assertTrue(type(u1_dict) is dict)
        for attr in dict_attrs:
            self.assertTrue(attr in u1_dict)

    def test_user_to_dict2(self):
        """ test the to_dict method """

        u1 = User()
        u1.email = "user@mail.com"
        u1.password = "7224"
        u1.first_name = "user1"
        u1.last_name = "user last"
        u1_dict = u1.to_dict()

        # test that updated_at and created_at was converted to strings
        self.assertTrue(type(u1_dict["updated_at"] is str))
        self.assertTrue(type(u1_dict["created_at"] is str))

        # test that __class__stores the correct class name
        self.assertEqual(u1_dict["__class__"], "User")

        self.assertEqual(u1.email, u1_dict["email"])
        self.assertEqual(u1.password, u1_dict["password"])
        self.assertEqual(u1.first_name, u1_dict["first_name"])
        self.assertEqual(u1.last_name, u1_dict["last_name"])

    def test_user_to_dict_args(self):
        """ test the to_dict method with args """

        u1 = User()

        with self.assertRaises(TypeError):
            u1.to_dict("h")
