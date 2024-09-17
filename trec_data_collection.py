from data_collection import bplus_approach, sequential_approach, secondary_approach
from clustering_and_secondary import get_entire_dataset, secondary_indexing
from clean_query import clean_query

def create_result_file(type: str, approach, structure):
    with open(f"{type}_res_2.tsv", 'w', encoding='utf-8') as res:
        for query in range(1,21):
            clean_query(f"./Queries/{query}.html")
            result, time, _, _, scores = approach("./cleaner_query.xml", structure)
            counter = 1
            for file in result:
                pieces = file.split('/')
                result_file = f"{pieces[-2]}:{pieces[-1][:-4]}"
                score = scores[file]
                res.write(f"NTCIR12-MathWiki-{query}\txxx\t{result_file}\t{counter}\t{score}\t{type}\n")
                counter += 1

create_result_file("bplus", bplus_approach, None)
# entire_dataset = get_entire_dataset()
# sec_dict = secondary_indexing(entire_dataset)
# create_result_file("seq", sequential_approach, entire_dataset)
# create_result_file("sec", secondary_approach, sec_dict)

'''
B+: no result for 2 (no operators) or 9 (malformed)
Top-rated answer for all, except second rated for 6
0.0665
AFTER cleaning:  0.0522
Seq: 2 literally returned 1108 results lol same result for 6
0.1349
Sec: 14, 4 returned nothing
0.1029
'''