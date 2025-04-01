import sys
import os

def list_env_variables():
    for key in sorted(os.environ):
        print(f"{key}={os.environ[key]}")

def filter_env_variables(filters):
    for key in sorted(os.environ):
        if any(f in key for f in filters):
            print(f"{key}={os.environ[key]}")

def main():
    args = sys.argv[1:]
    
    if not args:
        list_env_variables()
    else:
        filter_env_variables(args)

if __name__ == "__main__":
    main()
