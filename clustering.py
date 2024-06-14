from mathml_extractor import operator_extractor
from collections import Counter
import os
from initialize_bplustree import dataset_path

def get_index(filename: str):
    '''
    Given a MathML file, generates an index for the clustering approach.
    Returns the most frequent operator or, if multiple operators with the highest frequency, returns first in the file.
    '''
    operators = operator_extractor(filename)
    if operators:
        counts = Counter(operators)
        max_count = max(counts.values())
        most_frequent = [operator for operator, freq in counts.items() if freq == max_count]
        return most_frequent[0]
    return None


def secondary_indexing():
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
        index = get_index(file)
        if index:
            if index not in indexes:
                indexes[index] = []

            indexes[index].append(file)
    return indexes
if __name__ == "__main__":
    dict = secondary_indexing()
    dom_op = get_index("./../../Downloads/dataset_full/dataset_full/math/107931/question/3.xml")
    files = dict[dom_op]
    print(f"{"./../../Downloads/dataset_full/dataset_full/math/107931/question/3.xml" in files}")
