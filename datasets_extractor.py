# this is a script to extract the name of defect from MVTec

from os import listdir

def list_folders(path : str) -> list[str]:
    # it is guaranteed that the listdir will find only folders
    return [f for f in listdir(path)]

def main():
    anomaly_folders : list[str] = []
    type_folders : list[str] = []
    for type_folder in list_folders("datasets"):
        type_folders.append(type_folder)
        anomaly_folders = anomaly_folders + list_folders(f"datasets/{type_folder}/ground_truth")
            
    with open("datasets_mvtect.txt", "w") as f:
        f.write("type\n")
        for type_folder in type_folders:
            f.write(f"{type_folder}\n")
        f.write("\n")
        f.write("anomaly\n")
        for anomaly_folder in anomaly_folders:
            f.write(f"{anomaly_folder}\n")

if __name__ == "__main__":
    main()