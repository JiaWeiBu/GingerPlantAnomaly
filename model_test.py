# anomalib test
from classes.anomalib_lib import GetModel

def main():
    print("anomalib test")
    print(GetModel())
    print(len(GetModel()))

    with open('anomalib_model.txt', 'w') as f:
        for model in GetModel():
            f.write(f"{model}\n")

if __name__ == "__main__":
    main()