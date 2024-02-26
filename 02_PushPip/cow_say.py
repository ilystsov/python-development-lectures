from cowsay import cowsay, list_cows
import argparse

parser = argparse.ArgumentParser(
    description="Python version of the classic cowsay program."
)
parser.add_argument("text", type=str, help="The message the cow will say.", nargs="?")

