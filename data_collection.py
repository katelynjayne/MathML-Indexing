import treeMatch_patical_match2 as tm
from query_tree import query_bplus_tree, get_top_matches, get_avg_score, get_max_score, query_b_tree
from time import time
from mathml_extractor import operator_extractor, get_dominant_operator
from clustering_and_secondary import secondary_indexing, get_clustering_dict, get_entire_dataset
import random
import os

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
    avg_score = get_avg_score(scores, top_ten)
    max_score = get_max_score(scores)
    # print(f"Sequential execution time: {execution_time} ms")
    return top_ten, execution_time, avg_score, max_score

def secondary_approach(filename, idx_dict):
    start_time = time()
    dom_op = get_dominant_operator(filename, "")
    try:
        best_data = idx_dict[dom_op]
    except KeyError:
        best_data = []
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
    dom_op = get_dominant_operator(filename, "")
    folder = index_dict[dom_op]
    best_data = []
    try:
        for file in os.listdir(folder):
            best_data.append(f"{folder}/{file}")
    except FileNotFoundError:
        pass
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
    useable_files = []
    with open("./useable_files.txt", 'r', encoding="utf-8") as useable_files_file:
        useable_files = useable_files_file.readlines()
    useable_files = [file.strip() for file in useable_files]
    random.shuffle(useable_files)

    sec_dict = secondary_indexing()
    clus_dict = get_clustering_dict("./../clustering_dataset/")
    entire_dataset = get_entire_dataset()

    with open("./comparison-results/all_approaches_NTCIR-12.csv", 'w', encoding="utf-8") as csv:
        csv.write("File,Number of Operators,B+ Execution Time,Sequential Execution Time,Secondary Execution Time,B-Tree Execution Time,Clustering Execution Time,B+ Average Score,Sequential Average Score,Secondary Average Score,B-Tree Average Score,Clustering Average Score,B+ Max Score,Sequential Max Score,Secondary Max Score,B-Tree Max Score,Clustering Max Score\n")

        for short_filename in useable_files:
            file = f"./../../Downloads/NTCIR-12_Data/{short_filename}"
            num_operators = len(operator_extractor(file, ""))
            bplus_result, bplus_time, bplus_avg, bplus_max = bplus_approach(file)
            seq_result, seq_time, seq_avg, seq_max = sequential_approach(file, entire_dataset)
            sec_result, sec_time, sec_avg, sec_max = secondary_approach(file, sec_dict)
            b_result, b_time, b_avg, b_max = b_tree_approach(file)
            c_result, c_time, c_avg, c_max = clustering_approach(file, clus_dict)

            csv.write(f"{short_filename},{num_operators},{bplus_time},{seq_time},{sec_time},{b_time},{c_time},{bplus_avg},{seq_avg},{sec_avg},{b_avg},{c_avg},{bplus_max},{seq_max},{sec_max},{b_max},{c_max}\n")
            print(f"DONE: {short_filename},{num_operators},{bplus_time},{seq_time},{sec_time},{b_time},{c_time},{bplus_avg},{seq_avg},{sec_avg},{b_avg},{c_avg},{bplus_max},{seq_max},{sec_max},{b_max},{c_max}")
    
