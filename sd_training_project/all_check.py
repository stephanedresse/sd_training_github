import os
import sys

def main():
    if check_reboot():
        print("Pending Reboot.")
        sys.exit(1)

    print("Everything ok.")
    sys.exit(0)

main()
