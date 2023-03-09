#!/usr/bin/env python3
""" Main: entry poiuint of the program """

import cmd
import json
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User


class HBNBCommand(cmd.Cmd):
    """ main command """

    md = {
            "Amenity": Amenity,
            "BaseModel": BaseModel,
            "City": City,
            "Place": Place,
            "Review": Review,
            "State": State,
            "User": User
            }

    CLSSES = (
            'Amenity',
            'BaseModel',
            'City',
            'Place',
            'Review',
            'State',
            'User'
            )

    def default(self, line):
        """ default activity """

        cm = {
                "all": self.do_all,
                "update": self.call_update,
                "create": self.do_create,
                "show": self.do_show,
                "destroy": self.do_destroy,
                "count": self.count
                }

        full_line = line.split(".")
        if len(full_line) == 1:
            print("*** Unknown syntax: {}".format(line))
        else:
            if full_line[0] in self.md.keys():
                do_what = full_line[1].split("(", 1)
                if line[len(full_line[0]) + 1 + len(do_what[0])] != "(":
                    print("*** Unknown syntax: {}".format(line))
                    return
                if line[-1] != ")":
                    print("*** Unknown syntax: {}".format(line))
                    return
                if do_what[0] in cm.keys():
                    start_point = len(full_line[0]) + len(do_what[0]) + 2
                    bracket_line = full_line[0] + " " + line[start_point:-1]
                    cm[do_what[0]](bracket_line)
            else:
                print("*** Unknown syntax: {}".format(line))

    def help_default(self):
        """ default help docstring """

        print("Overrites the default text of doing nothing for class calls")

    def count(self, line):
        """ counts the instances in a class """

        args = line.split()
        counter = 0

        if args[0] in self.md.keys():
            for key in storage.all().keys():
                if args[0] == key[:len(args[0])]:
                    counter += 1
        print(counter)

    def help_count(self):
        """ docstring for count """

        print("used to count a class instance")

    def call_update(self, line):
        """ setup Class.Update for do_update """

        cls_name = line.split(" ", 1)
        c_name = cls_name[0]
        is_dict = cls_name[1].split(",", 1)
        if is_dict[1][1] == "{":
            dct = {}
            str_rep = "{}".format(is_dict[1][1:])
            dct = eval(str_rep)
            print(dct)
            ky = f"{cls_name[0]}.{is_dict[0][1:-1]}"
            for key in dct.keys():
                setattr(storage.all()[ky], key, dct[key])
            storage.save()
        else:
            args = cls_name[1].split(",")
            newl = c_name + " " + args[0][1:-1] + " " + args[1][2:-1] + args[2]
            self.do_update(newl)


    def help_class_update(self):
        """ helper docstring for class_update """

        print("converts the commas and quotes to a string literal")

    def complete_create(self, text, line, begidx, endidx):
        """ helps to complete class names """

        if not text:
            complete_list = self.CLSSES[:]
        else:
            complete_list = [i for i in self.CLSSES if i.startswith(text)]

        return complete_list

    def do_create(self, line):
        """ creates a new instance of base model and saves it to the json """

        args = line.split()

        if args == []:
            print("** class name missing **")
        elif args[0] in self.md.keys():
            new = self.md[args[0]]()
            new.save()
            print(new.id)
        else:
            print("** class doesn't exist **")

    def help_create(self):
        """ help desk for creating """

        print("used to create an instance of a class.")
        print("Usage: create <class_name>")

    def do_show(self, line):
        """ shows the string representation of an object """

        args = line.split()

        if args == []:
            print("** class name missing **")
        elif args[0] in self.md.keys():
            if len(args) == 1:
                print("** instance id missing **")
            else:
                if args[1][0] == '"' and args[1][-1] == '"':
                    args[1] = args[1][1:-1]
                key = '{}.{}'.format(args[0], args[1])
                if key in storage.all().keys():
                    print(storage.all()[key])
                else:
                    print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def help_show(self):
        """ docstring for the help for show command """

        print("show <Classname> <id>")
        print("Displays the object notation of an id")

    def do_destroy(self, line):
        """ destroys an instance and saves it to the json """

        args = line.split()

        if args == []:
            print("** class name missing **")
        elif args[0] in self.md.keys():
            if len(args) == 1:
                print("** instance id missing **")
            else:
                if args[1][0] == '"' and args[1][-1] == '"':
                    args[1] = args[1][1:-1]
                key = '{}.{}'.format(args[0], args[1])
                if key in storage.all().keys():
                    del storage.all()[key]
                    storage.save()
                else:
                    print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def help_destroy(self):
        """ dicstring for destroy command """

        print("destroy <ClassName> <id>")
        print("destroy a class object based on its id")

    def do_all(self, line):
        """
            Prints all string representation of all instances
            based or not on the class name.
        """

        args = line.split()

        if args == []:
            for key in storage.all().keys():
                print(storage.all()[key])
        elif args[0] in self.md.keys():
            for key in storage.all().keys():
                if key[:len(args[0])] == args[0]:
                    print(storage.all()[key])
        else:
            print("** class doesn't exist **")

    def help_all(self):
        """ docstring for all help """

        print("Usage: all\n\tall <ClassName>")
        print("Prints all string representation of all", end='')
        print("instances based or not on the class name.")

    def do_update(self, line):
        """ updates an instance based on its classname and id """

        args = line.split()

        if args == []:
            print("** class name missing **")
        elif args[0] in self.md.keys():
            if len(args) == 1:
                print("** instance id missing **")
            elif len(args) == 2:
                print("** attribute name missing **")
            elif len(args) == 3:
                print("** value missing **")
            else:
                attr_name = args[2]
                key = '{}.{}'.format(args[0], args[1])
                if key in storage.all().keys():
                    valu = []
                    valu.append(args[3])
                    if valu[0][0] == '"' and valu[0][-1] != '"':
                        i = 4
                        while i < len(args):
                            valu.append(args[i])
                            try:
                                if valu[i][-1] == '"':
                                    break
                            except IndexError:
                                pass
                            i += 1
                    valu = " ".join(valu)
                else:
                    print("** no instance found **")
            try:
                value = int(valu)
            except ValueError:
                try:
                    value = float(valu)
                except ValueError:
                    if valu[0] == '"' and valu[-1] == '"':
                        valu = valu[1:-1]
                    value = valu
            setattr(storage.all()[key], attr_name, value)
            storage.all()[key].save()
        else:
            print("** class doesn't exist **")

    def help_update(self):
        """ doctsring for help_update """

        print(" Updates an instance based on the class name", end='')
        print("and id by adding or updating attribute")

    def do_quit(self, line):
        """ exits the console """

        return True

    def help_quit(self):
        """ help documentation on quitting """

        print("Exit the HBNB Command interpreter using: quit or ctrl-d")

    def emptyline(self):
        """ overrides the emptyline function """

        pass

    def help_emptyline(self):
        """ help text for empty lines """

        print("Does nothing as opposed to repeating the last command")

    cmd.prompt = '(hbnb) '
    do_EOF = do_quit
    help_EOF = help_quit
    complete_destroy = complete_create
    complete_show = complete_create
    complete_all = complete_create
    complete_update = complete_create


if __name__ == '__main__':
    HBNBCommand().cmdloop()
