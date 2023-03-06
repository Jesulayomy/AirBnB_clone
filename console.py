#!/usr/bin/env python3
""" Main: entry poiuint of the program """

import cmd
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """ main command """

    def do_create(self, line):
        """ creates a new instance of base model and saves it to the json """

        if line == 'BaseModel':
            new = BaseModel()
            new.save()
        elif line == '':
            print("** class name missing **")
        else:
            print("** class doesn't exist**")

    def do_show(self, line):
        """ shows the string representation of an object """

        pass

    def help_create(self):
        """ help desk for creating """

        print("used to create an instance of a class.")
        print("Usage: create <class_name>")

    def do_quit(self, line):
        """ exits the console """

        return True

    def help_quit(self):
        """ help documentation on quitting """

        print("Exit the HBNB Command interpreter using: quit or ctrl-d")

    def emptyline(self):
        """ overrides the emptyline function """

        pass

    cmd.prompt = '(hbnb) '
    do_EOF = do_quit
    help_EOF = help_quit

if __name__ == '__main__':
    HBNBCommand().cmdloop()
