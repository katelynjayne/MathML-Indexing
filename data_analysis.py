import pandas
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from statistics import mean

def sequential_analysis_v1():
    '''
    Avg B+ Time: 743.073165713258
    Avg Seq Time: 80398.66825241354
    Correlation Coefficient: -0.2360261919465195
    P-value: 0.0007430960024968117
    The correlation (between number of operators and difference between results) is statistically significant.
    Percent same top result: 0.7263681592039801
    '''
    df = pandas.read_csv("./comparison-results/bplus_vs_seq_results.csv")

    differences = df["Difference Between Results"]
    operators = df["Number of Operators"]
    bplus = df["B+ Execution Time (ms)"]
    seq = df["Sequential Execution Time (ms)"]
    samesies = df["Same Top Result"]

    print(f"Avg B+ Time: {mean(bplus)}")
    print(f"Avg Seq Time: {mean(seq)}")

    correlation, p_value = stats.pearsonr(operators, differences)

    print(f'Correlation Coefficient: {correlation}')
    print(f'P-value: {p_value}')

    # Interpret the p-value
    alpha = 0.05
    if p_value < alpha:
        print("The correlation is statistically significant.")
    else:
        print("The correlation is not statistically significant.")

    m, b = np.polyfit(operators, differences, 1)

    plt.scatter(operators, differences, edgecolors='w', linewidth=0.5, label="Data Points")
    plt.plot(operators, m*operators + b, color='red', label=f'Trend Line (y={m:.2f}x + {b:.2f})')
    plt.xlabel("Amount of Operators")
    plt.ylabel("Difference")
    plt.legend()
    plt.show()

    counter = 0
    for result in samesies:
        if result:
            counter += 1

    print(f"Percent True: {counter / len(samesies)}")

def sequential_analysis_v2():
    '''
    Avg B+ time: 785.9896652734102
    Avg Seq time: 84263.91315697438
    Avg B+ score: 0.8285296726625021
    Avg Seq score: 0.898304428225348
    '''

    df = pandas.read_csv("./comparison-results/bplus_v_seq.csv")

    bplus_time = df["B+ Execution Time (ms)"]
    seq_time = df["Sequential Execution Time (ms)"]

    print(f"Avg B+ time: {mean(bplus_time)}")
    print(f"Avg Seq time: {mean(seq_time)}")

    bplus_avg_scores = df["B+ Avg Score"]
    seq_avg_scores = df["Seq Avg Score"]

    print(f"Avg B+ score: {mean(bplus_avg_scores)}")
    print(f"Avg Seq score: {mean(seq_avg_scores)}")

    bplus_max_scores = df["B+ Max Score"]
    seq_max_scores = df["Seq Max Score"]

    print(f"Best B+ scores: {set(bplus_max_scores)}")
    print(f"Best B scores: {set(seq_max_scores)}")

def b_tree_analysis():
    '''
    B-Tree and B+-Tree got the SAME results. TINIEST difference in speed.
    Avg B+ time: 676.0913367066986
    Avg B time: 914.8397937434297
    '''

    df2 = pandas.read_csv("./comparison-results/bplus_v_b.csv")

    bplus_time = df2["B+ Execution Time (ms)"]
    b_time = df2["B Execution Time (ms)"]

    print(f"Avg B+ time: {mean(bplus_time)}")
    print(f"Avg B time: {mean(b_time)}")

    bplus_avg_scores = df2["B+ Avg Score"]
    b_avg_scores = df2["B Avg Score"]

    print(f"Avg B+ score: {mean(bplus_avg_scores)}")
    print(f"Avg B score: {mean(b_avg_scores)}")

    bplus_max_scores = df2["B+ Max Score"]
    b_max_scores = df2["B Max Score"]

    print(f"Best B+ scores: {set(bplus_max_scores)}")
    print(f"Best B scores: {set(b_max_scores)}")

def secondary_results():
    '''
    Avg B+ time: 754.9190900812101
    Avg sec time: 7203.132819180465
    Avg B+ score: 0.8285296726625021
    Avg sec score: 0.8768250618743398
    Both had at least one score of 1 (perfect match) for every file.
    Percent secondary better score: 52.5%
    Percent B+ better score: 6.0%
    Percent same average score: 42.0%
    '''
    df3 = pandas.read_csv("./comparison-results/bplus_v_sec.csv")

    bplus_time = df3["B+ Execution Time (ms)"]
    sec_time = df3["Secondary Execution Time (ms)"]

    print(f"Avg B+ time: {mean(bplus_time)}")
    print(f"Avg sec time: {mean(sec_time)}")

    bplus_avg_scores = df3["B+ Avg Score"]
    sec_avg_scores = df3["Sec Avg Score"]

    print(f"Avg B+ score: {mean(bplus_avg_scores)}")
    print(f"Avg sec score: {mean(sec_avg_scores)}")

    bplus_max_scores = df3["B+ Max Score"]
    sec_max_scores = df3["Sec Max Score"]

    print(f"Best B+ scores: {set(bplus_max_scores)}")
    print(f"Best sec scores: {set(sec_max_scores)}")

    sec_percent = 0
    bplus_percent = 0
    same_percent = 0

    for bplus, sec in zip(bplus_avg_scores, sec_avg_scores):
        if bplus > sec:
            bplus_percent += 1
        elif sec > bplus:
            sec_percent += 1
        else:
            same_percent += 1

    print(f"Percent secondary better score: {sec_percent / 2}%")
    print(f"Percent B+ better score: {bplus_percent / 2}%")
    print(f"Percent same average score: {same_percent / 2}%")

def clustering_results():
    '''
    Avg B+ time: 782.2261390401356
    Avg clustering time: 7475.2446241046655
    Avg B+ score: 0.8285296726625021
    Avg clustering score: 0.8768250618743398
    Both always had a score of 1 (perfect) in the results
    Percent clustering better score: 52.5%
    Percent B+ better score: 6.0%
    Percent same average score: 42.0%
    '''
    df4 = pandas.read_csv("./comparison-results/bplus_v_clustering.csv")

    bplus_time = df4["B+ Execution Time (ms)"]
    c_time = df4["Clustering Execution Time (ms)"]

    print(f"Avg B+ time: {mean(bplus_time)}")
    print(f"Avg clustering time: {mean(c_time)}")

    bplus_avg_scores = df4["B+ Avg Score"]
    c_avg_scores = df4["Clustering Avg Score"]

    print(f"Avg B+ score: {mean(bplus_avg_scores)}")
    print(f"Avg clustering score: {mean(c_avg_scores)}")

    bplus_max_scores = df4["B+ Max Score"]
    c_max_scores = df4["Clustering Max Score"]

    print(f"Best B+ scores: {set(bplus_max_scores)}")
    print(f"Best clustering scores: {set(c_max_scores)}")


    clus_percent = 0
    bplus_percent = 0
    same_percent = 0

    for bplus, clus in zip(bplus_avg_scores, c_avg_scores):
        if bplus > clus:
            bplus_percent += 1
        elif clus > bplus:
            clus_percent += 1
        else:
            same_percent += 1

    print(f"Percent clustering better score: {clus_percent / 2}%")
    print(f"Percent B+ better score: {bplus_percent / 2}%")
    print(f"Percent same average score: {same_percent / 2}%")

def all_data_analysis():
    df = pandas.read_csv("./comparison-results/all_data_combined.csv")
    df_b = pandas.read_csv("./comparison-results/bplus_v_b.csv")
    bplus_time = df["Average B+ Execution Time"]
    more_bplus_time = df_b["B+ Execution Time (ms)"]
    first = mean(bplus_time)
    second = mean(more_bplus_time)
    # print(f"Overall B+ Execution time: {mean([first, second])}")

    fastest = df["Fastest Approach"]
    labels = ["Sequential","Secondary","B+-Tree","B-Tree","Clustering"]
    frequency = [0,0,0,0,0]
    for result in fastest:
        idx = labels.index(result)
        frequency[idx] += 1
    while 0 in frequency:
        labels.remove(labels[frequency.index(0)])
        frequency.remove(0)


    __, __, autotexts = plt.pie(frequency, labels=labels, autopct= '%1.2f%%', colors=["black","dimgray","darkgray","lightgray"])
    for autotext in autotexts[:2]:
        autotext.set_color('white')
    plt.savefig("./comparison-results/fastest.png")
    plt.clf()

def avg_df(data):
    return f"Average {data.name}: {mean(list(data))}"

def avg_2df(data1, data2):
    return f"Average {data1.name}: {(mean(list(data1)) + mean(list(data2))) / 2}"

def wiki_data_analysis():
    df = pandas.read_csv("./comparison-results/no_sequential_NTCIR-12.csv")
    df2 = pandas.read_csv("./comparison-results/all_approaches_NTCIR-12.csv")
    bplus_time = list(df["B+ Execution Time"])
    bplus_time.extend(list(df2["B+ Execution Time"]))
    print(f"AVG B+ TIME: {mean(bplus_time)}")
    seq_time = df2["Sequential Execution Time"]
    print(avg_df(seq_time))
    sec_time = list(df["Secondary Execution Time"])
    sec_time.extend(list(df2["Secondary Execution Time"]))
    print(f"AVG SEC TIME: {mean(sec_time)}")
    b_time = list(df["B-Tree Execution Time"])
    b_time.extend(list(df2["B-Tree Execution Time"]))
    print(f"AVG B TIME: {mean(b_time)}")
    clus_time = list(df["Clustering Execution Time"])
    clus_time.extend(list(df2["Clustering Execution Time"]))
    print(f"AVG CLUS TIME: {mean(clus_time)}")

    bplus_avg = df["B+ Average Score"]
    bplus_avg2 = df2["B+ Average Score"]
    print(avg_2df(bplus_avg, bplus_avg2))
    seq_avg = df2["Sequential Average Score"]
    print(avg_df(seq_avg))
    sec_avg = df["Secondary Average Score"]
    sec_avg2 = df2["Secondary Average Score"]
    print(avg_2df(sec_avg, sec_avg2))
    b_avg = df["B-Tree Average Score"]
    b_avg2 = df2["B-Tree Average Score"]
    print(avg_2df(b_avg, b_avg2))
    clus_avg = df["Clustering Average Score"]
    clus_avg2 = df2["Clustering Average Score"]
    print(avg_2df(clus_avg, clus_avg2))

    bplus_max = df["B+ Max Score"]
    bplus_max2 = df2["B+ Max Score"]
    print(avg_2df(bplus_max, bplus_max2))
    seq_max = df2["Sequential Max Score"]
    print(avg_df(seq_max))
    sec_max = df["Secondary Max Score"]
    sec_max2 = df2["Secondary Max Score"]
    print(avg_2df(sec_max, sec_max2))
    b_max = df["B-Tree Max Score"]
    b_max2 = df2["B-Tree Max Score"]
    print(avg_2df(b_max, b_max2))
    clus_max = df["Clustering Max Score"]
    clus_max2 = df2["Clustering Max Score"]
    print(avg_2df(clus_max, clus_max2))

    # sec_times_cleaned = list(sec_time)
    # for time, score in zip(sec_time,sec_max):
    #     if time == 0 and score == 0:
    #         sec_times_cleaned.remove(0)

    # print(f"SEC: {mean(sec_times_cleaned)}")
        
    # clus_times_cleaned = list(clus_time)
    # for time, score in zip(clus_time,clus_max):
    #     if time == 0 and score == 0:
    #         clus_times_cleaned.remove(0)

    # print(f"CLUS: {mean(clus_times_cleaned)}")

    labels = ["Secondary","B+-Tree","B-Tree","Clustering"]
    frequency = [0,0,0,0]
    for times in zip(sec_time, bplus_time, b_time, clus_time):
        fastest = min(times)
        if fastest == 0:
            continue
        idx = times.index(fastest)
        frequency[idx] += 1
    
    _, _, autotexts = plt.pie(frequency, labels=labels, autopct='%1.2f%%', colors=["black","dimgray","darkgray","lightgray"])
    for autotext in autotexts[:2]:
        autotext.set_color('white')
    plt.savefig("./comparison-results/fastest-NTCIR.png")
    plt.show()

# wiki_data_analysis()

def approach_analysis():
    df = pandas.read_csv("./comparison-results/approach_0_scores.csv")
    max_score = df["Max Score"]
    avg_score = df["Avg Score"]
    top_avg_score = df["Top Ten Avg Score"]
    num_files = df["Total Files Returned"]
    filenames = df["File"]
    not_found = df["Number of Files not Found"]

    for score,file in zip(max_score, filenames):
        if score != 1 and score != 0:
            print(file)
  

    print(avg_df(max_score))
    print(avg_df(avg_score))
    print(avg_df(top_avg_score))

    cleaned_max = [x for x in max_score if x != 0]
    cleaned_avg = [x for x in avg_score if x != 0]
    cleaned_top_avg = [x for x in top_avg_score if x != 0]

    print(mean(cleaned_max))
    print(mean(cleaned_avg))
    print(mean(cleaned_top_avg))

# approach_analysis()

'''
MathArticles/wpmath0000016/Multiple_kernel_learning/33.xml
--> it's 33 in our dataset but 34 in the html file?
Average Max Score: 0.8409815271546836
Average Avg Score: 0.6009970402079011
Average Top Ten Avg Score: 0.6754470773591297
0.9699902273987122
0.6931915111971177
0.7790623729632407
'''

# with open("./comparison-results/APP0_TEST_TIMES_all_approaches_NTCIR12_latex_queries_csv.csv", 'r') as file:
#     times = []
#     for line in file.readlines():
#         times.append(float(line.split()[1]))
#     print(mean(times))

def tangent_analysis():
    df = pandas.read_csv("./comparison-results/tangent_scores.csv")
    max_score = df["Max Score"]
    avg_score = df["Avg Score"]
    not_found = df["Number of Files not Found"]
    print(sum(list(not_found)))
    print(avg_df(max_score))
    print(avg_df(avg_score))


    weird = 0
    our_fault_maybe = 0
    for max, num_missing in zip(max_score, not_found):
        if max != 1:
            if num_missing == 0:
                weird += 1
            else:
                our_fault_maybe += 1
    print(weird)
    print(our_fault_maybe)


tangent_analysis()