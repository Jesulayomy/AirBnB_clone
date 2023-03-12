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
    """ main command entry point """

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
        """
            Default action taken on unknown commands
            This also handles helper commands of the format:
                ClassName.command(args)
        """

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
            return
        else:
            cmd1 = full_line[1].split("(", 1)
            if cmd1[0] not in cm.keys():
                print("*** Unknown syntax: {}".format(line))
                return
            if full_line[0] not in self.md.keys():
                print("** class doesn't exist **")
                return
            else:
                do_what = full_line[1].split("(", 1)
                try:
                    if line[len(full_line[0]) + 1 + len(do_what[0])] != "(":
                        print("*** Unknown syntax: {}".format(line))
                        return
                    if line[-1] != ")":
                        print("*** Unknown syntax: {}".format(line))
                        return
                except IndexError:
                    print("*** Unknown syntax: {}".format(line))
                    return
                if do_what[0] in cm.keys():
                    start_point = len(full_line[0]) + len(do_what[0]) + 2
                    bracket_line = full_line[0] + " " + line[start_point:-1]
                    cm[do_what[0]](bracket_line)
                else:
                    print("*** Unknown syntax: {}".format(line))
                    return

    def help_default(self):
        """ default help docstring """

        print("Usage: <ClassName.command(*args)>")
        print("\tOverrites the default syntax error to handle class calls")

    def count(self, line):
        """ Counts and prints the number of instances of a class """

        args = line.split()
        counter = 0

        if args[0] in self.md.keys():
            for key in storage.all().keys():
                if args[0] == key[:len(args[0])]:
                    counter += 1
        print(counter)

    def help_count(self):
        """ docstring for count """

        print("Usage: <ClassName.count()>")
        print("\tUsed to count a class instance")

    def call_update(self, line):
        """
            Setup Class.Update(args) for do_update()
            or dictionary version Class.Update(id, {})
        """

        # cls_name[0] = classname, cls_name[1] = rest of the line
        cls_name = line.split(" ", 1)
        # instance check
        if cls_name[1] == '' or cls_name[1][0] == '{':
            print("** instance id missing **")
            return
        # set classname to cn
        cn = cls_name[0]
        # is_dict[0] is the id enclosed in dQuotes
        is_dict = cls_name[1].split(",", 1)
        key1 = "{}.{}".format(cn, is_dict[0][1:-1])
        if key1 in storage.all():
            pass
        else:
            print("** no instance found **")
            return
        if len(is_dict) == 1:
            print("** attribute name missing **")
            return

        # is_dict[1] is the rest of the line after <"id",> or <"id"> if
        # attr_name is missing is_dict[1] = " attr_name, 'value' ..."
        str_rep = "{}".format(is_dict[1][1:])
        try:
            dct = eval(str_rep)
        except Exception:
            return
        # cmmd is <class id>
        cmmd = cn + " {}".format(is_dict[0][1:-1])
        if type(dct) is dict:
            for key in dct.keys():
                try:
                    setattr(storage.all()[key1], key, dct[key])
                    storage.all()[key1].save()
                except KeyError:
                    pass
            return
        elif type(dct) is tuple:
            i = 0
            while i < 2:
                cmmd += " "
                if i == 1:
                    cmmd += '"'
                cmmd += dct[i]
                i += 1
            cmmd += '"'
            newl = cmmd
        elif type(dct) is str:
            args = cls_name[1].split(",", 2)
            try:
                newl = cn + " " + args[0][1:-1] + " "
            except IndexError:
                print("** instance id missing **")
            try:
                if args[1][1] == '"' or args[1][1] == "'":
                    newl = newl + args[1][2:-1]
                else:
                    newl = newl + args[1][1:]
                newl = newl + args[2]
            except IndexError:
                pass
        self.do_update(newl)

    def help_call_update(self):
        """ helper docstring for class_update """

        print("Converts (, and \") to a string literal or updates with dict")

    def complete_create(self, text, line, begidx, endidx):
        """ helps to complete class names """

        if not text:
            complete_list = self.CLSSES[:]
        else:
            complete_list = [i for i in self.CLSSES if i.startswith(text)]

        return complete_list

    def help_complete_create(self):
        """ Docstring for complete_create/show/all/destroy/update """

        print("Usage: command <tab><tab>")
        print("       command (cl-nm)<tab>")
        print("\tAutocompletes the classname based on\
                string being typed after command")

    def do_create(self, line):
        """ Creates a new instance of base model and saves it to the json """

        args = line.split()

        if args == []:
            print("** class name missing **")
            return
        if args[0] in self.md.keys():
            new = self.md[args[0]]()
            new.save()
            print(new.id)
            return
        else:
            print("** class doesn't exist **")
            return

    def help_create(self):
        """ Help docstring for create command """

        print("Usage: create <class_name>")
        print("\tUsed to create an instance of a class. The id is printed")

    def do_show(self, line):
        """ Displays the string representation of an object """

        args = line.split()

        if args == []:
            print("** class name missing **")
            return
        if args[0] in self.md.keys():
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

        print("Usage: show <Classname> <id>")
        print("\tDisplays the object notation of an id")

    def do_destroy(self, line):
        """ destroys an instance and saves it to the json """

        args = line.split()

        if args == []:
            print("** class name missing **")
            return
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
                    return
        else:
            print("** class doesn't exist **")
            return

    def help_destroy(self):
        """ dicstring for destroy command """

        print("Usage: destroy <ClassName> <id>")
        print("\tDestroy a class object based on its id")

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
            return

    def help_all(self):
        """ docstring for all help """

        print("Usage: all\n\tall <ClassName>")
        print("Prints all string representation of all", end='')
        print("instances based or not on the class name.")

    def do_update(self, line):
        """ updates an instance based on its classname and id """

        if not line:
            print("** class name missing **")
            return

        args = line.split(" ", 3)

        if args[0] in self.md.keys():
            if len(args) == 1:
                print("** instance id missing **")
                return
            elif len(args) == 2:
                key = '{}.{}'.format(args[0], args[1])
                if key in storage.all().keys():
                    print("** attribute name missing **")
                else:
                    print("** no instance found **")
                return
            elif len(args) == 3:
                print("** value missing **")
                return
            else:
                clas_name = args[0]
                clas_id = args[1]
                attr_name = args[2]
                key = '{}.{}'.format(args[0], args[1])
                if key in storage.all().keys():
                    args_valu = args[3].split(' ')
                    valu = []
                    if args_valu[0][0] == '"' and args_valu[0][-1] == '"':
                        args_res = args_valu[0][1:-1]
                        valu.append(args_res)
                    elif args_valu[0][0] == '"' and args_valu[0][-1] != '"':
                        valu.append(args_valu[0])
                        i = 1
                        while i < len(args_valu):
                            valu.append(args_valu[i])
                            if args_valu[i][-1] == '"':
                                break
                            i += 1
                        valu[0] = valu[0][1:]
                        valu[i] = valu[i][:-1]
                    elif args_valu[0][0] != '"':
                        valu.append(args_valu[0])

                    valu = " ".join(valu)
                else:
                    print("** no instance found **")
                    return
            try:
                value = int(valu)
            except ValueError:
                try:
                    value = float(valu)
                except ValueError:
                    try:
                        if valu[0] == '"' and valu[-1] == '"':
                            valu = valu[1:-1]
                    except IndexError:
                        pass
                    value = valu
            setattr(storage.all()[key], attr_name, value)
            storage.all()[key].save()
        else:
            print("** class doesn't exist **")

    def help_update(self):
        """ doctsring for help_update """

        print("Usage: update <classname> <id> <attribute_name> <value>")
        print("\tUpdates an instance based on the class name", end='')
        print(" and id by adding or updating attribute")

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

    prompt = '(hbnb) '
    do_EOF = do_quit
    help_EOF = help_quit
    complete_destroy = complete_create
    complete_show = complete_create
    complete_all = complete_create
    complete_update = complete_create


if __name__ == '__main__':
    HBNBCommand().cmdloop()
