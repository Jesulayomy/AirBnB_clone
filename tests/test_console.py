import unittest
import sys
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class ConsoleTest(unittest.TestCase):
    """ A class to test the console class """

    models = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    @classmethod
    def setUpClass(cls):
        """ creates all models to be used for testing """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            cls.base_id = f.getvalue()[:-1]

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            cls.user_id = f.getvalue()[:-1]

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            cls.state_id = f.getvalue()[:-1]

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            cls.city_id = f.getvalue()[:-1]

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            cls.amenity_id = f.getvalue()[:-1]

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            cls.place_id = f.getvalue()[:-1]

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            cls.review_id = f.getvalue()[:-1]

    def test_create(self):
        """ test the create command """

        # test create for BaseModel
        with patch("sys.stdout", new=StringIO()) as f:
            # create model and get value printed without '\n'
            HBNBCommand().onecmd("create BaseModel")
            value = f.getvalue()[:-1]

            # test if value is string
            self.assertTrue(type(value) is str)

            all_objs = storage.all()
            obj_key = "BaseModel.{}".format(value)

            # test that key is in storage
            self.assertTrue(obj_key in all_objs)

            # test that id are same
            self.assertEqual(value, all_objs[obj_key].id)

        # test create for User
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            value = f.getvalue()[:-1]
            self.assertTrue(type(value) is str)
            all_objs = storage.all()
            obj_key = "User.{}".format(value)
            self.assertTrue(obj_key in all_objs)
            self.assertEqual(value, all_objs[obj_key].id)

    def test_create_wrong_model(self):
        """ test create with unknown model type """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create MyModel")
            value = f.getvalue()
            self.assertEqual(value, "** class doesn't exist **\n")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Users")
            value = f.getvalue()
            self.assertEqual(value, "** class doesn't exist **\n")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create 1")
            value = f.getvalue()
            self.assertEqual(value, "** class doesn't exist **\n")

    def test_create_no_model(self):
        """ test create ommiting model name """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            value = f.getvalue()
            self.assertEqual(value, "** class name missing **\n")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create  ")
            value = f.getvalue()
            self.assertEqual(value, "** class name missing **\n")

    def test_show(self):
        """ test the show command """

        # test the show command
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show State {}".format(self.state_id))
            value = f.getvalue()[:-1]
            # find the new object created in storage

            all_objs = storage.all()
            key = "State.{}".format(self.state_id)
            obj = all_objs[key]

            # test that value is equal to __str__() of obj
            # show command prints the obj using obj.__str__()
            # - so value should be equal to obj.__str__()
            self.assertEqual(value, obj.__str__())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show City {}".format(self.city_id))
            value = f.getvalue()[:-1]
            all_objs = storage.all()
            key = "City.{}".format(self.city_id)
            obj = all_objs[key]
            self.assertEqual(value, obj.__str__())

    def test_show_wrong_id(self):
        """ test the show comand with wrong id """

        # test with wrong id
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show State 123kkiwq")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show User 123kaeells")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show State test")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

    def test_show_no_id(self):
        """ test show omitting id """

        # test with wrong id
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show State")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** instance id missing **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show State   ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** instance id missing **")

    def test_show_wrong_model(self):
        """ test show with wrong class """

        # test with wrong class
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show Stat ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show myModel 1123")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show model ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

    def test_show_no_model(self):
        """ test show with no model """

        # test with no model
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class name missing **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show   ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class name missing **")

    def test_destroy(self):
        """ test destroy command """

        ConsoleTest.setUpClass()
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy Review {}".format(self.review_id))
            value = f.getvalue()
            self.assertEqual(value, "")

        # test that instance doesnt exist for deleted id
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show Review {}".format(self.review_id))
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

        # test for place
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy Place {}".format(self.place_id))
            value = f.getvalue()
            # doesnt print
            self.assertEqual(value, "")

        # test that instance doesnt exist for deleted id
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("show Place {}".format(self.place_id))
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

    def test_destroy_wrong_id(self):
        """ test the destroy comand with wrong id """

        # test with wrong id
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy State 123kkiwq")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy User 123kaeells")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy State test")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

    def test_destroy_no_id(self):
        """ test destroy omitting id """

        # test with wrong id
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy State")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** instance id missing **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy State   ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** instance id missing **")

    def test_destroy_wrong_model(self):
        """ test destroy with wrong class """

        # test with wrong class
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy Stat ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy myModel 1123")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy model ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

    def test_destroy_no_model(self):
        """ test destroy with no model """

        # test with no model
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class name missing **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("destroy   ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class name missing **")

    def test_all(self):
        """ test the all command """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all")
            value = f.getvalue()[:-1]
            # value will be string that print an array of objects
            # create an expected value to check against value
            all_objs = storage.all()
            exp_val = ""
            for key in all_objs.keys():
                exp_val += all_objs[key].__str__()
                exp_val += "\n"

            self.assertEqual(value, exp_val[:-1])

    def test_all_model(self):
        """ test all command with model """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all BaseModel ")
            value = f.getvalue()[:-1]
            # value will be string that print an array of objects
            # create an expected value to check against value
            all_objs = storage.all()
            exp_val = ""
            for key in all_objs.keys():
                if all_objs[key].__class__.__name__ == "BaseModel":
                    exp_val += all_objs[key].__str__()

            self.assertEqual(value, exp_val)

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all User ")
            value = f.getvalue()[:-1]
            # value will be string that print an array of objects
            # create an expected value to check against value
            all_objs = storage.all()
            exp_val = []
            for key, obj in all_objs.items():
                if obj.__class__.__name__ == "User":
                    exp_val.append(all_objs[key].__str__())

    def test_all2(self):
        """ test all for a model that has no object """

        # check if a model exist and destroy it
        destroy = False
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all Review")
            value = f.getvalue()[:-1]

            if value != "** class doesn't exist **":
                destroy = True

        if destroy:
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("destroy Review {}".format(
                    self.review_id))
                value = f.getvalue()[:-1]

        # test all when model doesnt exist
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all Review")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "")

        # recreate model to prevent failure of other tests
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            value = f.getvalue()[:-1]
            ConsoleTest.review_id = value

    def test_all_wrong_model(self):
        """ test all with wrong class """

        # test with wrong class
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all Stat ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all myModel 1123")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all model ")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")
