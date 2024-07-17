from mathml_extractor import get_dominant_operator
import os
import shutil

dataset_path = "./../../Downloads/dataset_full/dataset_full/math/"
ntcir_path = "./../../Downloads/NTCIR-12_Data/MathArticles/"

def get_entire_dataset():
    print("getting dataset")
    mse_folders = os.listdir(dataset_path)
    entire_dataset = []
    for folder in mse_folders:
        if ".DS_Store" not in folder:
            question_path = f"{dataset_path}{folder}/question/"
            answer_path = f"{dataset_path}{folder}/answers/"
            for file in os.listdir(question_path):
                whole_path = question_path + file
                entire_dataset.append(whole_path)
            for file in os.listdir(answer_path):
                whole_path = answer_path + file
                entire_dataset.append(whole_path)
    
    ntcir_folders = os.listdir(ntcir_path)
    for folder in ntcir_folders:
        articles = os.listdir(f"{ntcir_path}{folder}")
        for article in articles:
            path_to_article = f"{ntcir_path}{folder}/{article}/"
            for file in os.listdir(path_to_article):
                whole_path = path_to_article + file
                entire_dataset.append(whole_path)
    
    return entire_dataset

def secondary_indexing(entire_dataset=[]):
    '''
    This function parses the entire dataset and returns a secondary index dictionary.
    Make sure you've adjusted the dataset_path variable for your machine.
    '''
    indexes = {}
    print("getting op dict")
    for file in entire_dataset:
        ns = "{http://www.w3.org/1998/Math/MathML}"
        if "NTCIR-12" in file:
            ns = ""
        index = get_dominant_operator(file, ns)
        if index:
            if index not in indexes:
                indexes[index] = []

            indexes[index].append(file)
    return indexes

def clustering(new_dataset_location, operator_dict={}):
    '''
    This function will organize the dataset so files with the same dominant operator are stored together.
    Takes in as an argument the location where this newly organized dataset should be stored.
    Returns a dictionary: keys are operators, values are the location of the folder of files with that dominant operator.
    '''
    locations = {}
    print("in clustering")

    reserved_names = ['con', 'prn', 'aux', 'nul', 'com1', 'com2', 'com3', 'com4', 'com5', 'com6', 'com7', 'com8', 'com9', 'lpt1', 'lpt2', 'lpt3', 'lpt4', 'lpt5', 'lpt6', 'lpt7', 'lpt8', 'lpt9']

    for operator in operator_dict.keys():
        if operator in reserved_names:
            new_operator = f"{operator}_reserved"
        else:
            new_operator = operator
        new_folder_path = os.path.join(new_dataset_location, new_operator)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        locations[operator] = new_folder_path

        for i, file in enumerate(operator_dict[operator]):
            shutil.copyfile(file, f"{new_folder_path}/{i}.xml")

    return locations

def get_clustering_dict(clustered_dataset_location, operator_dict={}):
    '''
    Relatively faster way to get the clustering index dictionary if the dataset has already been organized on your machine with clustering().
    Takes in the path to the clustered dataset, returns the dictionary.
    '''
    locations = {}
    for operator in operator_dict.keys():
        locations[operator] = f"{clustered_dataset_location}{operator}"
    return locations


if __name__ == "__main__":
    print(clustering("./../clustering_dataset_new/"))