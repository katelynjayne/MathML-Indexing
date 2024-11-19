import treeMatch_patical_match2 as tm
from time import time
from query_tree import get_top_matches, get_avg_score, get_max_score
import pickle
from mathml_extractor import operand_extractor, operator_extractor
import pandas


def query_dict(filename):
    symbols = set(operator_extractor(filename, ''))
    operands = operand_extractor(filename, '', version=1)

    with open('./python_dict.txt', 'rb') as file:
        dataset_dict = pickle.load(file)

    counts = {}
    for symbol in symbols:
        result = dataset_dict[symbol]
        for file, ops in result:
            operands_diff = -abs(operands - ops)
            if file in counts:
                counts[file][0] += 1
            else:
                counts[file] = [1, operands_diff]
    return get_top_matches(counts)

def hashing_approach(filename):
    start_time = time()
    best_data = query_dict(filename)
    fast_tree = tm.FastTreeMatch()
    scores = fast_tree.run(filename, best_data)
    if not scores:
        scores = {}
    top_ten = get_top_matches(scores)
    end_time = time()
    execution_time = (end_time - start_time) * 1000
    avg_score = get_avg_score(scores, top_ten)
    max_score = get_max_score(scores)
    return len(best_data), execution_time, avg_score, max_score


df = pandas.read_csv("./comparison-results/bplus_extensions.csv")
files = df["File"]
with open("comparison-results/hashing_results.csv", 'w', encoding='utf8') as out:
    out.write("File,Hashing Execution Time,B+ Execution Time,Same Results\n")
    for i, file in enumerate(files):
        full_name = "./../../Downloads/NTCIR-12_Data/" + file
        num_results, execution_time, avg_score, max_score = hashing_approach(full_name)
        match = num_results == df["Original Number of Results"][i] and round(avg_score,6) == round(df["Original Average Score"][i],6) and max_score == 1
        out.write(f"{file},{execution_time},{df["Original Execution Time"][i]},{match}\n")
    


# import os
# ntcir_path = "./../../Downloads/NTCIR-12_Data/MathArticles/"
# op_dict = {}
# folders = os.listdir(ntcir_path)
# for folder in folders:
#     articles = os.listdir(f"{ntcir_path}{folder}")
#     for article in articles:
#         path_to_article = f"{ntcir_path}{folder}/{article}/"
#         for file in os.listdir(path_to_article):
#             whole_path = path_to_article + file
#             operands = operand_extractor(whole_path, "", version=1)
#             indexes = operator_extractor(whole_path, "")
#             for index in indexes:
#                 if not index in op_dict:
#                     op_dict[index] = set()
#                 op_dict[index].add((whole_path,operands))
                

# print(len(op_dict))
# inp = input("y/n")
# if inp == 'y': 
#     with open("python_dict.txt", 'wb') as file:
#         pickle.dump(op_dict, file)