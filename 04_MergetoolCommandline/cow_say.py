import shlex

import cowsay
import cmd

class CowsayShell(cmd.Cmd):
    prompt = '(cowsay)'
    intro = "Python version of the classic cowsay program. Type help or ? to list commands.\n"

    def do_list_cows(self, arg):
        """List all cow characters."""

        args = shlex.split(arg)
        if len(args) == 1:
            print(cowsay.list_cows(arg if arg else cowsay.COW_PEN))




if __name__ == '__main__':
    CowsayShell().cmdloop()