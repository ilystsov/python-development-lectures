from cowsay import cowsay, list_cows
import argparse

parser = argparse.ArgumentParser(
    description="Python version of the classic cowsay program."
)
parser.add_argument("text", type=str, help="The message the cow will say.", nargs="?")
parser.add_argument("-e", help="The cow's eyes.", default="oo")
parser.add_argument("-f", help="The cow file to use.", default="default")
parser.add_argument("-T", help="The cow's tongue.", default="  ")
parser.add_argument(
    "-n", help="Wrap text. By default, text is wrapped.", action="store_false"
)
parser.add_argument("-W", help="Maximum width of the text.", type=int, default=40)
presets = ["b", "d", "g", "p", "s", "t", "w", "y"]
group = parser.add_mutually_exclusive_group()
for preset in presets:
    group.add_argument(
        f"-{preset}", help=f"Use the {preset} character preset.", action="store_true"
    )
parser.add_argument("-l", help="List all cow characters.", action="store_true")
args = parser.parse_args()
if args.l:
    print(sorted(list_cows()))

