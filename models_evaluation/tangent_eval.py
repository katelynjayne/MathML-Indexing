import treeMatch_patical_match2 as tm
import pandas
from app_eval import find_file
from query_tree import get_avg_score, get_max_score

def transform_filename(filepath):
    pieces = filepath.split('/')
    return f"{pieces[-2]}:{pieces[-1][:-4]}"



quer_result_dict = {}

with open(r"C:\Users\Kate\Downloads\all_app_cft_res - first run\all_app_cft_res - first run", 'r', encoding='utf-8') as file:
        for line in file.readlines():
            elements = line.split()
            quer = int(elements[0].split('-')[-1])
            result = elements[2]
            if quer not in quer_result_dict:
                quer_result_dict[quer] = []
            if len(quer_result_dict[quer]) == 10:
                 continue
            else:
                quer_result_dict[quer].append(result)

df = pandas.read_csv("./comparison-results/all_approaches_NTCIR-12.csv")
queries = df["File"]
path_rep_dict = {}
for file in queries:
    path_rep_dict[transform_filename(file)] = file
query_files_sorted = sorted(path_rep_dict.items())
queries = [item[1] for item in query_files_sorted]

with open("./comparison-results/tangent_scores.csv", 'w', encoding="utf-8") as outfile:
        outfile.write("File,Max Score,Avg Score,Number of Files not Found\n")
        for i, file in enumerate(queries):
            if i == 521:
                continue
            answer_file = f"./../../Downloads/NTCIR-12_Data/{file}"
            results = quer_result_dict[i]
            res_filepaths = []
            files_not_found = 0
            for result in results:
                colon_idx = result.rfind(':')
                article = result[:colon_idx]
                num = result[colon_idx+1:]
                filepath = find_file(article, num)
                if filepath:
                    res_filepaths.append(filepath)
                else:
                    files_not_found += 1
            fast_match = tm.FastTreeMatch()
            scores = fast_match.run(answer_file, res_filepaths)
            max_score = get_max_score(scores)
            avg_score = get_avg_score(scores, res_filepaths)
            outfile.write(f"{file},{max_score},{avg_score},{files_not_found}\n")

    
