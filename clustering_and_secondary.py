from mathml_extractor import get_dominant_operator
import os

dataset_path = "./../../Downloads/dataset_full/dataset_full/math/"

def secondary_indexing():
    '''
    This function parses the entire dataset and returns a secondary index dictionary.
    Make sure you've adjusted the dataset_path variable for your machine.
    '''
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
        
    indexes = {}
    for file in entire_dataset:
        index = get_dominant_operator(file)
        if index:
            if index not in indexes:
                indexes[index] = []

            indexes[index].append(file)
    return indexes

def clustering():
    '''
    will reorganize the dataset so like files are together, and a data structure for clustering indexing
    not yet implemented
    '''
    pass

if __name__ == "__main__":
    dict = secondary_indexing()
    dom_op = get_dominant_operator("./../../Downloads/dataset_full/dataset_full/math/107931/question/3.xml")
    files = dict[dom_op]
    print(f"{"./../../Downloads/dataset_full/dataset_full/math/107931/question/3.xml" in files}")
