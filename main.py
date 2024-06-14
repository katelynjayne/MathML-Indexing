import treeMatch_patical_match2 as tm
from query_tree import query_bplus_tree, get_top_matches, get_avg_score, get_max_score, query_b_tree
from initialize_bplustree import dataset_path
from time import time
import os
from mathml_extractor import operator_extractor
from xml.etree import ElementTree
from clustering import secondary_indexing, get_index
import pandas

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
    dom_op = get_index(filename)
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
    # print(f"Execution time: {execution_time} ms")
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

if __name__ == "__main__":
    entire_dataset = []
    question_files = []
    all_the_folders = os.listdir(dataset_path)
    for folder in all_the_folders:
        if ".DS_Store" not in folder:
            question_path = f"{dataset_path}{folder}/question/"
            answer_path = f"{dataset_path}{folder}/answers/"
            for file in os.listdir(question_path):
                whole_path = question_path + file
                entire_dataset.append(whole_path)
                question_files.append(whole_path)
            for file in os.listdir(answer_path):
                whole_path = answer_path + file
                entire_dataset.append(whole_path)

    df = pandas.read_csv("./bplus_vs_seq_results.csv")
    two_hundered_files = df["File"]
    with open("./comparison_data.csv", 'w') as csv:
        csv.write("B+ Execution Time (ms),B Execution Time (ms),B+ Avg Score,B Avg Score,B+ Max Score,B Max Score,Number of Operators,File\n")

        for file in question_files:
            num_operators = len(operator_extractor(file))
            if num_operators == 0:
                continue
            try:
                ElementTree.parse(file)
            except:
                continue
            
            bplus_result, bplus_time, bplus_avg, bplus_max = bplus_approach(file)
            # seq_result, seq_time = sequential_approach(file, entire_dataset)
            b_result, b_time, b_avg, b_max = b_tree_approach(file)
            # diff = len(set(bplus_result) ^ set(seq_result))
            # same_top_result = False
            # top_result_included = False
            # if bplus_result[0] == seq_result[0]:
            #     same_top_result = True
            # if same_top_result or bplus_result[0] in seq_result or seq_result[0] in bplus_result:
            #     top_result_included = True
            


            csv.write(f"{bplus_time},{b_time},{bplus_avg},{b_avg},{bplus_max},{b_max},{num_operators},{file}\n")
            print(f"DONE: {bplus_time}, {b_time}, {file}")
        

'''
Friendly reminder that the bplus tree does not handle files with no operator well... look into?
in questions: 43.64% 0 operators
in whole dataset: 42.6077% 0 operators
problematic!!
also... what's up with the malformed files??
only .4% malformed
'''
    
