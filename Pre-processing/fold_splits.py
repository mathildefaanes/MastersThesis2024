import json
import random

######################################################################################################
# This script creates a splits_final.json file for 5-fold cross-validation of the different training sets
# that spilts the 2D images randomly, but ensures that images from the same patients are in the same file.
######################################################################################################


def read_json(file):
    with open(file, "r") as file:
        data = json.load(file)
    all_images = []
    for item in data:
        train_files = item["train"]
        val_files = item["val"]
    all_images.extend(train_files)
    all_images.extend(val_files)
    print(len(all_images))
    #print(all_images)
    return all_images

def read_txt(txtfile):
    file = open(txtfile, 'r')
    lines = file.read().split('\n')
    all_images = []
    for line in lines:
        line_split = line.split(',')
        img = line_split[0]
        all_images.append(img[:-7])
    file.close()
    #print(all_images)
    print(len(all_images))
    return all_images

def write_split_json():
    #all_images = read_json("splits_final_254_random.json")
    all_images = read_txt("Dataset262_MRandUS_tumorarea200.txt")
    print(len(all_images))
    file = open("folds_all.txt", 'r')
    lines = file.read().split('\n')

    fold0 = lines[0].split(': ')[1]
    fold1 = lines[1].split(': ')[1]
    fold2 = lines[2].split(': ')[1]
    fold3 = lines[3].split(': ')[1]
    fold4 = lines[4].split(': ')[1]

    fold0 = fold0.strip("[]").replace("'","").split(", ")
    fold1 = fold1.strip("[]").replace("'","").split(", ")
    fold2 = fold2.strip("[]").replace("'","").split(", ")
    fold3 = fold3.strip("[]").replace("'","").split(", ")
    fold4 = fold4.strip("[]").replace("'","").split(", ")

    print(len(fold0))
    print(len(fold1))
    print(len(fold2))
    print(len(fold3))
    print(len(fold4))

    fold0 = [f for f in fold0 if f in all_images]
    fold1 = [f for f in fold1 if f in all_images]
    fold2 = [f for f in fold2 if f in all_images]
    fold3 = [f for f in fold3 if f in all_images]
    fold4 = [f for f in fold4 if f in all_images]


    print(len(fold0))
    print(len(fold1))
    print(len(fold2))
    print(len(fold3))
    print(len(fold4))
    print(len(fold1)+len(fold0)+len(fold3) + len(fold4) + len(fold2))


    new_data = [
        {
            "train": fold1 + fold2 + fold3 + fold4,
            "val": fold0
        },
        {
            "train": fold2 + fold3 + fold4 + fold0,
            "val": fold1
        },
        {
            "train": fold3 + fold4 + fold0 + fold1,
            "val": fold2
        },
        {
            "train": fold4 + fold0 + fold1 + fold2,
            "val": fold3
        },
        {
            "train": fold0 + fold1 + fold2 + fold3,
            "val": fold4
        }
    ]

    with open("splits_final_254_by_patient.json", "w") as file_json:
        json.dump(new_data, file_json)

write_split_json()

