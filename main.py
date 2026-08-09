## this is the main program file, program is launched through this file
#  and runs through a modular and recursive structure
#  i.e as a general rule, functions should be defined in individual .py source files.
from program_mods.game import backbone

def main():
    backbone()

if __name__ == "__main__":
    main()
    