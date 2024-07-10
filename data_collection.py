import treeMatch_patical_match2 as tm
from query_tree import query_bplus_tree, get_top_matches, get_avg_score, get_max_score, query_b_tree
from time import time
from mathml_extractor import operator_extractor, get_dominant_operator
from xml.etree import ElementTree
from clustering_and_secondary import secondary_indexing, get_clustering_dict, get_entire_dataset
import pandas
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
    dataset_path = "./../../Downloads/NTCIR-12_Data/MathArticles/wpmath0000001/"
    all_the_folders = os.listdir(dataset_path)
    test_data = []
    for folder in all_the_folders:
        for file in os.listdir(f"{dataset_path}{folder}/"):
            test_data.append(f"{dataset_path}{folder}/{file}")
    
    # sec_dict = secondary_indexing()
    # clus_dict = get_clustering_dict("./../clustering_dataset/")
    # entire_dataset = get_entire_dataset()

    # with open("./comparison-results/all_approaches_NTCIR-12.csv", 'w') as csv:
    #     csv.write("File,Number of Operators,B+ Execution Time,Sequential Execution Time,Secondary Execution Time,B-Tree Execution Time,Clustering Execution Time,B+ Average Score,Sequential Average Score,Secondary Average Score,B-Tree Average Score,Clustering Average Score,B+ Max Score,Sequential Max Score,Secondary Max Score,B-Tree Max Score,Clustering Max Score\n")
    norm_count = malformed_count = zero_ops_counts = altered_count = 0
    for file in test_data:
        # Skipping files with no operators or malformed MathML
        try:
            ElementTree.parse(file)
        except:
            try:
                with open(file, 'r') as malformed:
                    text = malformed.read()
                    text = text.replace('>&<', '>&amp;<')
                    text = text.replace('>"<', '>&quot;<')
                    text = text.replace(">'<", '>&apos;<')
                    text = text.replace('><<', '>&lt;<')
                    text = text.replace('>><', '>&rt;<')
                    ElementTree.fromstring(text)
                    altered_count += 1
            except Exception as e:
                # print(f"MALFORMED MATHML: {file}")
                # print(e)
                malformed_count += 1
                continue
        num_operators = len(operator_extractor(file))
        if num_operators == 0:
            # print(f"ZERO OPERATORS: {file}")
            zero_ops_counts += 1
            continue
        norm_count += 1
    print(f"NORMAL: {norm_count}, MALFORMED: {malformed_count}, ZERO OPS: {zero_ops_counts}, ALTERABLE: {altered_count}")
            
            # bplus_result, bplus_time, bplus_avg, bplus_max = bplus_approach(file)
            # seq_result, seq_time, seq_avg, seq_max = sequential_approach(file, entire_dataset)
            # sec_result, sec_time, sec_avg, sec_max = secondary_approach(file, sec_dict)
            # b_result, b_time, b_avg, b_max = b_tree_approach(file)
            # c_result, c_time, c_avg, c_max = clustering_approach(file, clus_dict)

            # csv.write(f"{file},{num_operators},{bplus_time},{seq_time},{sec_time},{b_time},{c_time},{bplus_avg},{seq_avg},{sec_avg},{b_avg},{c_avg},{bplus_max},{seq_max},{sec_max},{b_max},{c_max}\n")
            # print(f"DONE: {file},{num_operators},{bplus_time},{seq_time},{sec_time},{b_time},{c_time},{bplus_avg},{seq_avg},{sec_avg},{b_avg},{c_avg},{bplus_max},{seq_max},{sec_max},{b_max},{c_max}")
    

    '''
    16: NORMAL: 0, MALFORMED: 81, ZERO OPS: 33761, ALTERABLE: 263
    15: NORMAL: 0, MALFORMED: 40, ZERO OPS: 22747, ALTERABLE: 142
    14: NORMAL: 0, MALFORMED: 103, ZERO OPS: 34400, ALTERABLE: 343
    13: NORMAL: 0, MALFORMED: 98, ZERO OPS: 34321, ALTERABLE: 296
    12: NORMAL: 0, MALFORMED: 115, ZERO OPS: 34456, ALTERABLE: 347
    11: NORMAL: 0, MALFORMED: 24, ZERO OPS: 9706, ALTERABLE: 61
    10: NORMAL: 0, MALFORMED: 18, ZERO OPS: 9495, ALTERABLE: 68
    09: NORMAL: 0, MALFORMED: 69, ZERO OPS: 32907, ALTERABLE: 299
    08: NORMAL: 0, MALFORMED: 110, ZERO OPS: 31379, ALTERABLE: 270
    07: NORMAL: 0, MALFORMED: 79, ZERO OPS: 35920, ALTERABLE: 300
    06: NORMAL: 0, MALFORMED: 73, ZERO OPS: 34787, ALTERABLE: 270
    05: NORMAL: 0, MALFORMED: 125, ZERO OPS: 37297, ALTERABLE: 399
    04: NORMAL: 0, MALFORMED: 85, ZERO OPS: 38789, ALTERABLE: 265
    03: NORMAL: 0, MALFORMED: 100, ZERO OPS: 41259, ALTERABLE: 373
    02: NORMAL: 0, MALFORMED: 114, ZERO OPS: 47632, ALTERABLE: 439
    01: NORMAL: 0, MALFORMED: 111, ZERO OPS: 53812, ALTERABLE: 460
    '''
