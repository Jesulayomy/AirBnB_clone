from console import HBNBCommand
from io import StringIO
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from unittest.mock import patch
import os
import sys
import unittest


class ConsoleTest(unittest.TestCase):
    """ A class to test the console class """

    s_test = FileStorage()

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

    def testquit(self):
        """ tests the quit command """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("quit")
            value = f.getvalue()
            self.assertEqual(value, "")

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

    def test_show_class_call(self):
        """ test Class.show() instance """

        objs = self.s_test._FileStorage__objects.copy()
        for key in objs.keys():
            del self.s_test._FileStorage__objects[key]

        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

        ConsoleTest.setUpClass()
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Amenity.show(\"{}\")".format(
                self.amenity_id))
            value = f.getvalue()[:-1]
            all_objs = storage.all()
            key = "Amenity.{}".format(self.amenity_id)
            obj = all_objs[key]
            self.assertEqual(value, obj.__str__())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.show(\"{}\")".format(
                self.base_id))
            value = f.getvalue()[:-1]
            all_objs = storage.all()
            key = "BaseModel.{}".format(self.base_id)
            obj = all_objs[key]
            self.assertEqual(value, obj.__str__())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("City.show(\"{}\")".format(
                self.city_id))
            value = f.getvalue()[:-1]
            all_objs = storage.all()
            key = "City.{}".format(self.city_id)
            obj = all_objs[key]
            self.assertEqual(value, obj.__str__())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Place.show(\"{}\")".format(
                self.place_id))
            value = f.getvalue()[:-1]
            all_objs = storage.all()
            key = "Place.{}".format(self.place_id)
            obj = all_objs[key]
            self.assertEqual(value, obj.__str__())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Review.show(\"{}\")".format(
                self.review_id))
            value = f.getvalue()[:-1]
            all_objs = storage.all()
            key = "Review.{}".format(self.review_id)
            obj = all_objs[key]
            self.assertEqual(value, obj.__str__())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("State.show(\"{}\")".format(
                self.state_id))
            value = f.getvalue()[:-1]
            all_objs = storage.all()
            key = "State.{}".format(self.state_id)
            obj = all_objs[key]
            self.assertEqual(value, obj.__str__())

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("User.show(\"{}\")".format(
                self.user_id))
            value = f.getvalue()[:-1]
            all_objs = storage.all()
            key = "User.{}".format(self.user_id)
            obj = all_objs[key]
            self.assertEqual(value, obj.__str__())

    def test_destroy_class_call(self):
        """ test Class.show() instance """

        objs = self.s_test._FileStorage__objects.copy()
        for key in objs.keys():
            del self.s_test._FileStorage__objects[key]

        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

        ConsoleTest.setUpClass()
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Amenity.destroy(\"{}\")".format(
                self.amenity_id))
            value = f.getvalue()
            self.assertEqual(value, "")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.destroy(\"{}\")".format(
                self.base_id))
            value = f.getvalue()
            self.assertEqual(value, "")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("City.destroy(\"{}\")".format(
                self.city_id))
            value = f.getvalue()
            self.assertEqual(value, "")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Place.destroy(\"{}\")".format(
                self.place_id))
            value = f.getvalue()
            self.assertEqual(value, "")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Review.destroy(\"{}\")".format(
                self.review_id))
            value = f.getvalue()
            self.assertEqual(value, "")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("State.destroy(\"{}\")".format(
                self.state_id))
            value = f.getvalue()
            self.assertEqual(value, "")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("User.destroy(\"{}\")".format(
                self.user_id))
            value = f.getvalue()
            self.assertEqual(value, "")

    def test_count_class_call(self):
        """ test Class.show() instance """

        objs = self.s_test._FileStorage__objects.copy()
        for key in objs.keys():
            del self.s_test._FileStorage__objects[key]

        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

        ConsoleTest.setUpClass()
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Amenity.count()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "1")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.count()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "1")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("City.count()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "1")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Place.count()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "1")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Review.count()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "1")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("State.count()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "1")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("User.count()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "1")

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
            # value will be string that print a string of objects
            # create an expected value to check against value
            all_objs = storage.all()
            exp_val = ""
            for key in all_objs.keys():
                if all_objs[key].__class__.__name__ == "BaseModel":
                    exp_val += all_objs[key].__str__()
                    exp_val += '\n'

            self.assertEqual(value, exp_val[:-1])

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("all User ")
            value = f.getvalue()[:-1]
            # value will be string that print a string of objects
            # create an expected value to check against value
            all_objs = storage.all()
            exp_val = ""
            for key, obj in all_objs.items():
                if obj.__class__.__name__ == "User":
                    exp_val += all_objs[key].__str__()
                    exp_val += '\n'

            self.assertEqual(value, exp_val[:-1])

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

    def test_model_all(self):
        """ test model.all() command"""

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.all()")
            value = f.getvalue()[:-1]
            all_objs = storage.all()
            exp_val = ""
            for key in all_objs.keys():
                if all_objs[key].__class__.__name__ == "BaseModel":
                    exp_val += all_objs[key].__str__()
                    exp_val += '\n'

            self.assertEqual(value, exp_val[:-1])

    def test_model_all2(self):
        """ test model.all() for a model that has no object """

        objs = self.s_test._FileStorage__objects.copy()
        for key in objs.keys():
            del self.s_test._FileStorage__objects[key]

        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

        destroy = False

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Review.all()")
            value = f.getvalue()[:-1]

            if value == '':
                pass
            elif value != "** class doesn't exist **":
                destroy = True

        if destroy:
            with patch("sys.stdout", new=StringIO()) as f:
                HBNBCommand().onecmd("destroy Review {}".format(
                    self.review_id))
                value = f.getvalue()[:-1]

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Review.all()")
            value = f.getvalue()
            self.assertEqual(value, "")

    def test_model_all_wrong_model(self):
        """ test model.all() with wrong class """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("NewModel.all()")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** class doesn't exist **")

    def test_update(self):
        """ test the update command """

        ConsoleTest.setUpClass()
        # test update with user
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "update User {} first_name \"Samuel\""
                    .format(self.user_id))
            value = f.getvalue()[:-1]

            # update command prints nothing
            self.assertEqual(value, "")

            # get all objs and find the user object updated
            all_objs = storage.all()
            obj_key = "User.{}".format(self.user_id)
            obj = all_objs[obj_key]

            # check that the new attribute first_name exist and check value
            self.assertTrue("first_name" in obj.to_dict())
            self.assertEqual("Samuel", obj.first_name)

        # test update with City
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "update City {} city_id \"11213ef\""
                    .format(self.city_id))
            value = f.getvalue()[:-1]

            # update command prints nothing
            self.assertEqual(value, "")

            # get all objs and find the user object updated
            all_objs = storage.all()
            obj_key = "City.{}".format(self.city_id)
            obj = all_objs[obj_key]

            # check that the new attribute first_name exist and check value
            self.assertTrue("city_id" in obj.to_dict())
            self.assertEqual("11213ef", obj.city_id)

    def test_update2(self):
        """ test the update command to update an existing attr """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "update User {} first_name \"Samuel John Stones\""
                    .format(self.user_id))
            value = f.getvalue()[:-1]

            # get all objs and find the user object updated
            all_objs = storage.all()
            obj_key = "User.{}".format(self.user_id)
            obj = all_objs[obj_key]

            # check that the new attribute first_name exist and check value
            self.assertEqual("Samuel John Stones", obj.first_name)

        # test update with City
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "update City {} city_id \"1e21b\""
                    .format(self.city_id))
            value = f.getvalue()[:-1]

            # get all objs and find the user object updated
            all_objs = storage.all()
            obj_key = "City.{}".format(self.city_id)
            obj = all_objs[obj_key]

            # check that the new attribute first_name exist and check value
            self.assertEqual("1e21b", obj.city_id)

    def test_update3(self):
        """ test update with more attributes """

        with patch("sys.stdout", new=StringIO()) as f:
            # all other arguments are ignored after first attribute is updated
            command = "update State {} first_name ".format(self.state_id)
            command2 = "\"John John\" last_name \"Emeka\""
            HBNBCommand().onecmd(command + command2)

            # get all objs and find updated obj
            all_objs = storage.all()
            obj_key = "State.{}".format(self.state_id)
            obj = all_objs[obj_key]

            # check that first_name attribute exist and has correct val
            self.assertTrue("first_name" in obj.to_dict())
            self.assertEqual(obj.first_name, "John John")

            # check that last_name doesnt exit (was ignored)
            self.assertTrue("last_name" not in obj.to_dict())

    def test_update_no_value(self):
        """ test update when val is ommited """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel {} name"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** value missing **")

    def test_update_no_attribute(self):
        """ test update when attribute missing """

        ConsoleTest.setUpClass()
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel {}"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** attribute name missing **")

    def test_update_wrong_id(self):
        """ test update wrong id """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("update Place 110092"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** no instance found **")

    def test_update_no_id(self):
        """ test update with missing id """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("update Place "
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** instance id missing **")

    def test_update_wrong_model(self):
        """ test update with wrong model """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("update MyModel "
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** class doesn't exist **")

    def test_update_no_model(self):
        """ test update with missing model """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("update".format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** class name missing **")

    def test_model_update(self):
        """ test the model.update() command """

        ConsoleTest.setUpClass()
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "User.update(\"{}\", \"first_name\", \"Samuel\")"
                    .format(self.user_id))
            value = f.getvalue()[:-1]
            self.assertEqual(value, "")

            all_objs = storage.all()
            obj_key = "User.{}".format(self.user_id)
            obj = all_objs[obj_key]

            self.assertTrue("first_name" in obj.to_dict())
            self.assertEqual("Samuel", obj.first_name)

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "City.update(\"{}\", \"city_id\", \"11213ef\")"
                    .format(self.city_id))
            value = f.getvalue()[:-1]
            self.assertEqual(value, "")

            all_objs = storage.all()
            obj_key = "City.{}".format(self.city_id)
            obj = all_objs[obj_key]

            self.assertTrue("city_id" in obj.to_dict())
            self.assertEqual("11213ef", obj.city_id)

    def test_model_update2(self):
        """ test the model.update() command to update an existing attr """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "User.update(\"{}\", \"first_name\", \"Samuel Stones\")"
                    .format(self.user_id))
            value = f.getvalue()[:-1]

            all_objs = storage.all()
            obj_key = "User.{}".format(self.user_id)
            obj = all_objs[obj_key]

            self.assertEqual("Samuel Stones", obj.first_name)

    def test_model_update3(self):
        """ test model.update() with more attributes """

        with patch("sys.stdout", new=StringIO()) as f:
            command = "State.update(\"{}\", \"first_name\", ".format(
                                                            self.state_id)
            command2 = "\"John John\", \"last_name\", \"Emeka\")"
            HBNBCommand().onecmd(command + command2)

            all_objs = storage.all()
            obj_key = "State.{}".format(self.state_id)
            obj = all_objs[obj_key]

            self.assertTrue("first_name" in obj.to_dict())
            self.assertEqual(obj.first_name, "John John")

            self.assertTrue("last_name" not in obj.to_dict())

    def test_model_update_no_value(self):
        """ test model.update() when val is ommited """

        ConsoleTest.setUpClass()
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.update(\"{}\", \"name\")"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** value missing **")

    def test_model_update_no_attribute(self):
        """ test model.update() when attribute missing """

        ConsoleTest.setUpClass()
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.update(\"{}\")"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** attribute name missing **")

    def test_model_update_wrong_id(self):
        """ test model.update() wrong id """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Place.update(\"110092\")"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** no instance found **")

    def test_model_update_no_id(self):
        """ test model.update() with missing id """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Place.update()"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** instance id missing **")

    def test_model_update_wrong_model(self):
        """ test model.update() with wrong model """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("MyModel.update()"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** class doesn't exist **")

    def test_model_update_dict1(self):
        """ test the model.update() command with dict"""

        ConsoleTest.setUpClass()
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "User.update(\"{}\", {{'first_name': 'John'}})"
                    .format(self.user_id))
            value = f.getvalue()[:-1]
            self.assertEqual(value, "")

            all_objs = storage.all()
            obj_key = "User.{}".format(self.user_id)
            obj = all_objs[obj_key]

            self.assertTrue("first_name" in obj.to_dict())
            self.assertEqual("John", obj.first_name)

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "City.update(\"{}\", {{'city_id': '11213'}})"
                    .format(self.city_id))
            value = f.getvalue()[:-1]
            self.assertEqual(value, "")

            all_objs = storage.all()
            obj_key = "City.{}".format(self.city_id)
            obj = all_objs[obj_key]

            self.assertTrue("city_id" in obj.to_dict())
            self.assertEqual("11213", obj.city_id)

    def test_model_update_dict2(self):
        """ test the model.update() command to update an existing attr """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "User.update(\"{}\", {{\"first_name\": 'Samuel Stones'}})"
                    .format(self.user_id))
            value = f.getvalue()[:-1]

            all_objs = storage.all()
            obj_key = "User.{}".format(self.user_id)
            obj = all_objs[obj_key]

            self.assertEqual("Samuel Stones", obj.first_name)

    def test_model_update_dict3(self):
        """ test model.update() with more attributes """

        ConsoleTest.setUpClass()
        with patch("sys.stdout", new=StringIO()) as f:
            command = "User.update(\"{}\", {{'first_name': ".format(
                                                            self.user_id)
            command2 = "\"John John\", \"last_name\": 'Emeka', 'age': 89})"
            HBNBCommand().onecmd(command + command2)

            all_objs = storage.all()
            obj_key = "User.{}".format(self.user_id)
            obj = all_objs[obj_key]

            self.assertTrue("first_name" in obj.to_dict())
            self.assertEqual(obj.first_name, "John John")

            self.assertTrue("last_name" in obj.to_dict())
            self.assertEqual(obj.last_name, "Emeka")

            self.assertTrue("age" in obj.to_dict())
            self.assertEqual(obj.age, 89)

    def test_model_update_dict_wrong_id(self):
        """ test the model.update() command with wrong id"""

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "User.update(\"112345\", {'first_name': 'John'})")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** no instance found **")

    def test_model_update_dict_no_id(self):
        """ test the model.update() command with no id"""

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(
                    "User.update({'first_name': 'John'})")
            value = f.getvalue()[:-1]
            self.assertEqual(value, "** instance id missing **")

    def test_model_update_dict_wrong_model(self):
        """ test model.update() with wrong model """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("MyModel.update()"
                                 .format(self.base_id))
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** class doesn't exist **")

    def test_invalid_args(self):
        """ test some invalid args """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("hello Model")
            value = f.getvalue()[:-1]

            self.assertEqual(value, "*** Unknown syntax: hello Model")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Model.create()")
            value = f.getvalue()[:-1]

            self.assertEqual(value, "** class doesn't exist **")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Model.hide()")
            value = f.getvalue()[:-1]

            self.assertEqual(value, "*** Unknown syntax: Model.hide()")

    def test_invalid_args2(self):
        """ test some invalid args """

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("Model")
            value = f.getvalue()[:-1]

            self.assertEqual(value, "*** Unknown syntax: Model")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("User.update(")
            value = f.getvalue()[:-1]

            self.assertEqual(value, "*** Unknown syntax: User.update(")

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("how()")
            value = f.getvalue()[:-1]

            self.assertEqual(value, "*** Unknown syntax: how()")
