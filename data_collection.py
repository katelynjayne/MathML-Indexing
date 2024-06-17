import treeMatch_patical_match2 as tm
from query_tree import query_bplus_tree, get_top_matches, get_avg_score, get_max_score, query_b_tree
from time import time
from mathml_extractor import operator_extractor, get_dominant_operator
from xml.etree import ElementTree
from clustering_and_secondary import secondary_indexing, get_clustering_dict
import pandas
import os

dataset_path = "./../../Downloads/dataset_full/dataset_full/math/"

def bplus_approach(filename):
    start_time = time()
    best_data = query_bplus_tree(filename)
    fast_tree = tm.FastTreeMatch()
    scores = fast_tree.run(filename, best_data)
    if not scores:
        scores = {}
    top_ten = get_top_matches(scores)
    end_time = time()
    execution_time = (end_time - start_time) * 1000
    avg_score = get_avg_score(scores, top_ten)
    max_score = get_max_score(scores)
    # print(f"B+ Tree execution time: {execution_time} ms")
    return top_ten, execution_time, avg_score, max_score

def sequential_approach(filename, entire_dataset):
    start_time = time()
    fast_tree = tm.FastTreeMatch()
    scores = fast_tree.run(filename, entire_dataset)
    if not scores:
        scores = {}
    top_ten = get_top_matches(scores)
    end_time = time()
    execution_time = (end_time - start_time) * 1000
    # print(f"Sequential execution time: {execution_time} ms")
    return top_ten, execution_time

def secondary_approach(filename, idx_dict):
    start_time = time()
    dom_op = get_dominant_operator(filename)
    best_data = idx_dict[dom_op]
    fast_tree = tm.FastTreeMatch()
    scores = fast_tree.run(filename, best_data)
    if not scores:
        scores = {}
    top_ten = get_top_matches(scores)
    end_time = time()
    execution_time = (end_time - start_time) * 1000
    avg_score = get_avg_score(scores, top_ten)
    max_score = get_max_score(scores)
    # print(f"Secondary execution time: {execution_time} ms")
    return top_ten, execution_time, avg_score, max_score

def b_tree_approach(filename):
    start_time = time()
    best_data = query_b_tree(filename)
    fast_tree = tm.FastTreeMatch()
    scores = fast_tree.run(filename, best_data)
    if not scores:
        scores = {}
    top_ten = get_top_matches(scores)
    end_time = time()
    execution_time = (end_time - start_time) * 1000
    avg_score = get_avg_score(scores, top_ten)
    max_score = get_max_score(scores)
    # print(f"B Tree execution time: {execution_time} ms")
    return top_ten, execution_time, avg_score, max_score

def clustering_approach(filename, index_dict):
    start_time = time()
    dom_op = get_dominant_operator(filename)
    folder = index_dict[dom_op]
    best_data = []
    for file in os.listdir(folder):
        best_data.append(f"{folder}/{file}")
    fast_tree = tm.FastTreeMatch()
    scores = fast_tree.run(filename, best_data)
    if not scores:
        scores = {}
    top_ten = get_top_matches(scores)
    end_time = time()
    execution_time = (end_time - start_time) * 1000
    avg_score = get_avg_score(scores, top_ten)
    max_score = get_max_score(scores)
    # print(f"Clustering execution time: {execution_time} ms")
    return top_ten, execution_time, avg_score, max_score

if __name__ == "__main__":
    # entire_dataset = []
    # question_files = []
    # all_the_folders = os.listdir(dataset_path)
    # for folder in all_the_folders:
    #     if ".DS_Store" not in folder:
    #         question_path = f"{dataset_path}{folder}/question/"
    #         answer_path = f"{dataset_path}{folder}/answers/"
    #         for file in os.listdir(question_path):
    #             whole_path = question_path + file
    #             entire_dataset.append(whole_path)
    #             question_files.append(whole_path)
    #         for file in os.listdir(answer_path):
    #             whole_path = answer_path + file
    #             entire_dataset.append(whole_path)

    # Below code extracts the two hundred files used for other comparisons.
    # Above (commented) code will create a list of all the files in the dataset if more files are needed.

    df = pandas.read_csv("./comparison-results/bplus_vs_seq.csv")
    two_hundred_files = df["File"]
    
    # index_dict = secondary_indexing()
    location_dict = get_clustering_dict("./../clustering_dataset/")

    with open("./comparison-results/bplus_v_clustering.csv", 'w') as csv:
        csv.write("B+ Execution Time (ms),Clustering Execution Time (ms),B+ Avg Score,Clustering Avg Score,B+ Max Score,Clustering Max Score,Number of Operators,File\n")

        for file in two_hundred_files:
            # Skipping files with no operators or malformed MathML
            num_operators = len(operator_extractor(file))
            if num_operators == 0:
                continue
            try:
                ElementTree.parse(file)
            except:
                continue
            
            bplus_result, bplus_time, bplus_avg, bplus_max = bplus_approach(file)
            c_result, c_time, c_avg, c_max = clustering_approach(file, location_dict)

            csv.write(f"{bplus_time},{c_time},{bplus_avg},{c_avg},{bplus_max},{c_max},{num_operators},{file}\n")
            print(f"DONE: {bplus_time}, {c_time}, {file}")
    
