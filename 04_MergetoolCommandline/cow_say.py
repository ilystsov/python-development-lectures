import shlex

import cowsay
import cmd


class CowsayShell(cmd.Cmd):
    prompt = '(cowsay)'
    intro = "Python version of the classic cowsay program. Type help or ? to list commands.\n"

    def do_list_cows(self, arg):
        """List all cow characters.\nUSAGE: list_cows [path/to/file]"""

        args = shlex.split(arg)
        if len(args) == 1:
            print(cowsay.list_cows(arg if arg else cowsay.COW_PEN))
        else:
            print('Invalid arguments!')
            return

    def do_make_bubble(self, arg):
        """Wrap the text inside the bubble.\nUSAGE: make_bubble text [width [wrap_text]]"""
        args = shlex.split(arg)
        if len(args) == 0 or len(args) >= 4:
            print('Invalid arguments!')
            return
        text = args[0]
        width = 40
        wrap_text = True
        if len(args) >= 2:
            width = int(args[1])
        if len(args) == 3:
            wrap_text = bool(args[2])
        print(cowsay.make_bubble(text=text, width=width, wrap_text=wrap_text))


if __name__ == '__main__':
    CowsayShell().cmdloop()