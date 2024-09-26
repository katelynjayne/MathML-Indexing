import treeMatch_patical_match2 as tm
import pandas
import os
from query_tree import get_avg_score, get_max_score
import unicodedata

def find_file(article, num):
    article = unicodedata.normalize('NFC', article)
    path = "./../../Downloads/NTCIR-12_Data/MathArticles/"
    for folder in os.listdir(path):
        articles = os.listdir(f"{path}{folder}")
        if article not in articles:
            continue
        path_to_article = f"{path}{folder}/{article}/"
        files = os.listdir(path_to_article)
        if f"{num}.xml" not in files:
            continue
        return f"{path_to_article}{num}.xml"
    # print(f"COULDN'T FIND FILE: {article}:{num}")

if __name__ == "__main__":
    quer_result_dict = {}

    with open("./comparison-results/Approach-0-Raw-Results", 'r', encoding='utf-8') as file:
        for line in file.readlines():
            elements = line.split()
            quer = int(elements[0].split('-')[1]) - 1
            result = elements[2]
            if quer not in quer_result_dict:
                quer_result_dict[quer] = []
            quer_result_dict[quer].append(result)

    df = pandas.read_csv("./comparison-results/all_approaches_NTCIR-12.csv")
    files = df["File"]
    total_not_found = 0
    with open("./comparison-results/approach_0_scores_3.csv", 'w', encoding="utf-8") as file:
        file.write("Query Number,File,Max Score,Avg Score,Top Ten Avg Score,Number of Files not Found,Total Files Returned\n")
        idx = 0
        for query in quer_result_dict:
            while query != idx:
                file.write(f"{idx+1},{files[idx]},0,0,0,0,0\n")
                idx += 1
            idx += 1
            answer_file = f"./../../Downloads/NTCIR-12_Data/{files[query]}"
            results = quer_result_dict[query]
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
            total_not_found += files_not_found
            fast_match = tm.FastTreeMatch()
            scores = fast_match.run(answer_file, res_filepaths)
            max_score = get_max_score(scores)
            avg_score = get_avg_score(scores, res_filepaths)
            top_ten_avg_score = get_avg_score(scores, res_filepaths[:10])
            file.write(f"{query+1},{files[query]},{max_score},{avg_score},{top_ten_avg_score},{files_not_found},{len(results)}\n")
    print(f"NOT FOUND: {total_not_found}")

    '''
    FOUND: 15532 NOT FOUND: 1808 -> 1545

    '''

