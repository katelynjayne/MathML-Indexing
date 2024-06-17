from mathml_extractor import get_dominant_operator
import os
import shutil

dataset_path = "./../../Downloads/dataset_full/dataset_full/math/"

def get_entire_dataset():
    all_the_folders = os.listdir(dataset_path)
    entire_dataset = []
    for folder in all_the_folders:
        if ".DS_Store" not in folder:
            question_path = f"{dataset_path}{folder}/question/"
            answer_path = f"{dataset_path}{folder}/answers/"
            for file in os.listdir(question_path):
                whole_path = question_path + file
                entire_dataset.append(whole_path)
            for file in os.listdir(answer_path):
                whole_path = answer_path + file
                entire_dataset.append(whole_path)
    return entire_dataset

def secondary_indexing():
    '''
    This function parses the entire dataset and returns a secondary index dictionary.
    Make sure you've adjusted the dataset_path variable for your machine.
    '''
    entire_dataset = get_entire_dataset()
    indexes = {}
    for file in entire_dataset:
        index = get_dominant_operator(file)
        if index:
            if index not in indexes:
                indexes[index] = []

            indexes[index].append(file)
    return indexes

def clustering(new_dataset_location):
    '''
    This function will organize the dataset so files with the same dominant operator are stored together.
    Takes in as an argument the location where this newly organized dataset should be stored.
    Returns a dictionary: keys are operators, values are the location of the folder of files with that dominant operator.
    '''
    operator_dict = secondary_indexing()
    locations = {}

    if new_dataset_location[-1] != '/':
        new_dataset_location = f"{new_dataset_location}/"

    for operator in operator_dict.keys():
        new_folder_path = f"{new_dataset_location}{operator}"
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        locations[operator] = new_folder_path

        for i, file in enumerate(operator_dict[operator]):
            shutil.copyfile(file, f"{new_folder_path}/{i}.xml")

    return locations

def get_clustering_dict(clustered_dataset_location):
    '''
    Relatively faster way to get the clustering index dictionary if the dataset has already been organized on your machine with clustering().
    Takes in the path to the clustered dataset, returns the dictionary.
    '''
    operator_dict = secondary_indexing()
    locations = {}
    for operator in operator_dict.keys():
        locations[operator] = f"{clustered_dataset_location}{operator}"
    return locations


if __name__ == "__main__":
    print(clustering("./../clustering_dataset/"))