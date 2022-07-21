from msnrbf.decoder import parse

if (__name__ == "__main__"):
    with open("msnrbf/sgscredits", "rb") as f:
        result = parse(f)
        print(result)