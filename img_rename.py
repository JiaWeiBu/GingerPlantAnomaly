import os

file_path = "datasets/plant"

"""
datasets/plant
    week3
        60
            4_3.jpg
            2_3.jpg
        top
            4_2.jpg
            2_8.jpg

i want to rename the files to:
datasets/plant
    week3
        60
            00001.jpg
            00002.jpg
        top
            00001.jpg
            00002.jpg

rename the files number 1 to n does not matter the order

"""

def main():
    for week_num in range(3,21):
        count = 1
        for files in os.listdir(f"{file_path}/week{week_num}/60"):
            os.rename(f"{file_path}/week{week_num}/60/{files}", f"{file_path}/week{week_num}/60/{count:05}.jpg")
            count += 1
        count = 1
        for files in os.listdir(f"{file_path}/week{week_num}/top"):
            os.rename(f"{file_path}/week{week_num}/top/{files}", f"{file_path}/week{week_num}/top/{count:05}.jpg")
            count += 1
        print(f"week{week_num} done")
            

if __name__ == "__main__":
    main()