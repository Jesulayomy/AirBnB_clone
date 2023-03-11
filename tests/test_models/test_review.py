import unittest
import os
from datetime import datetime
from models import storage
from models.review import Review


class ReviewTest(unittest.TestCase):
    """ A class to test the Review class """

    def test_review1(self):
        """ Test review """

        r1 = Review()

        # testing default types
        self.assertEqual(len(r1.id), 36)
        self.assertTrue(type(r1.created_at) is datetime)
        self.assertTrue(type(r1.updated_at) is datetime)
        self.assertTrue(type(r1.place_id) is str)
        self.assertTrue(type(r1.user_id) is str)
        self.assertTrue(type(r1.text) is str)
        self.assertTrue(r1.created_at == r1.updated_at)

    def test_review2(self):
        """ test review model """

        r1 = Review()

        # testing default values
        self.assertEqual(r1.place_id, "")
        self.assertEqual(r1.user_id, "")
        self.assertEqual(r1.text, "")

    def test_review3(self):
        """ Test review model """

        r1 = Review()
        r1.place_id = "1223"
        r1.user_id = "11234"
        r1.text = "review1"

        self.assertTrue(type(r1.id) is str)
        self.assertEqual(r1.place_id, "1223")
        self.assertEqual(r1.user_id, "11234")
        self.assertEqual(r1.text, "review1")

    def test_review_args(self):
        """ Test review model with args """

        r1 = Review(1, 3)  # 1 and 3 will be ignored

        # Test that id exist and is not 1 or 3
        self.assertTrue(r1.id is not None)
        self.assertTrue(r1.id != 1)
        self.assertTrue(r1.id != 3)

        # Test that created_at exist and is not 1 or 3
        self.assertTrue(r1.created_at is not None)
        self.assertTrue(r1.created_at != 1)
        self.assertTrue(r1.created_at != 3)

        # Test that updated_at exist and is not 1 or 3
        self.assertTrue(r1.updated_at is not None)
        self.assertTrue(r1.updated_at != 1)
        self.assertTrue(r1.updated_at != 3)

    def test_review_kwargs(self):
        """ test review with kwargs """

        r1 = Review()
        r1.text = "review1"
        r1_dict = r1.to_dict()
        r2 = Review(**r1_dict)

        self.assertEqual(r1.id, r2.id)
        self.assertEqual(r1.created_at, r2.created_at)
        self.assertEqual(r1.updated_at, r2.updated_at)
        self.assertEqual(r1.text, r2.text)
        self.assertTrue(r1 is not r2)

    def test_review_str(self):
        """ test __str__ method of review """

        r1 = Review()
        out_str = "[{}] ({}) {}".format(
                 r1.__class__.__name__, r1.id, r1.__dict__
                )

        self.assertEqual(r1.__str__(), out_str)

    def test_review_save(self):
        """ test the save method of review """

        r1 = Review()

        # test that created_at and updated_at attributes are same
        self.assertEqual(r1.created_at, r1.updated_at)

        r1.save()  # saves r1 to file. Now updated_at will be different
        self.assertTrue(r1.created_at != r1.updated_at)

        fileName = "file.json"
        # test that file.json exists
        self.assertTrue(os.path.exists(fileName))
        # test that file.json is a file
        self.assertTrue(os.path.isfile(fileName))

    def test_review_save_args(self):
        """ test the save method with args """

        r1 = Review()

        with self.assertRaises(TypeError):
            r1.save(1, 2)

    def test_review_to_dict1(self):
        """ test the to_dict method """

        r1 = Review()
        r1.text = "review1"
        r1_dict = r1.to_dict()
        dict_attrs = ["__class__", "updated_at", "created_at", "id", "text"]

        self.assertTrue(type(r1_dict) is dict)
        for attr in dict_attrs:
            self.assertTrue(attr in r1_dict)

    def test_review_to_dict2(self):
        """ test the to_dict method """

        r1 = Review()
        r1.place_id = "1223"
        r1.user_id = "11234"
        r1.text = "review1"
        r1_dict = r1.to_dict()

        # test that updated_at and created_at was converted to strings
        self.assertTrue(type(r1_dict["updated_at"] is str))
        self.assertTrue(type(r1_dict["created_at"] is str))

        # test that __class__stores the correct class name
        self.assertEqual(r1_dict["__class__"], "Review")

        self.assertEqual(r1.place_id, r1_dict["place_id"])
        self.assertEqual(r1.user_id, r1_dict["user_id"])
        self.assertEqual(r1.text, r1_dict["text"])

    def test_review_to_dict_args(self):
        """ test the to_dict method with args """

        r1 = Review()

        with self.assertRaises(TypeError):
            r1.to_dict("h")
