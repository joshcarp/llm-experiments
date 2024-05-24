import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Not enough args supplied")
        raise SystemError
    if sys.argv[1] == "clone":
        print("clone")
    elif sys.argv[1] == "somethingelse":
        print("somethingelse")
