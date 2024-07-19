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

def wiki_data_analysis():
    df = pandas.read_csv("./comparison-results/all_approaches_updated_1_NTCIR-12.csv")
    bplus_time = df["B+ Execution Time"]
    print(avg_df(bplus_time))
    seq_time = df["Sequential Execution Time"]
    print(avg_df(seq_time))
    sec_time = df["Secondary Execution Time"]
    b_time = df["B-Tree Execution Time"]
    print(avg_df(b_time))
    clus_time = df["Clustering Execution Time"]

    bplus_avg = df["B+ Average Score"]
    print(avg_df(bplus_avg))
    seq_avg = df["Sequential Average Score"]
    print(avg_df(seq_avg))
    sec_avg = df["Secondary Average Score"]
    print(avg_df(sec_avg))
    b_avg = df["B-Tree Average Score"]
    print(avg_df(b_avg))
    clus_avg = df["Clustering Average Score"]
    print(avg_df(clus_avg))

    bplus_max = df["B+ Max Score"]
    print(avg_df(bplus_max))
    seq_max = df["Sequential Max Score"]
    print(avg_df(seq_max))
    sec_max = df["Secondary Max Score"]
    print(avg_df(sec_max))
    b_max = df["B-Tree Max Score"]
    print(avg_df(b_max))
    clus_max = df["Clustering Max Score"]
    print(avg_df(clus_max))

    sec_times_cleaned = list(sec_time)
    for time, score in zip(sec_time,sec_max):
        if time == 0 and score == 0:
            sec_times_cleaned.remove(0)

    print(f"SEC: {mean(sec_times_cleaned)}")
        
    clus_times_cleaned = list(clus_time)
    for time, score in zip(clus_time,clus_max):
        if time == 0 and score == 0:
            clus_times_cleaned.remove(0)

    print(f"CLUS: {mean(clus_times_cleaned)}")

    labels = ["Secondary","B+-Tree","B-Tree","Clustering"]
    frequency = [0,0,0,0]
    for times in zip( list(sec_time), list(bplus_time), list(b_time), list(clus_time)):
        fastest = min(times)
        if fastest == 0:
            continue
        idx = times.index(fastest)
        frequency[idx] += 1
    
    _, _, autotexts = plt.pie(frequency, labels=labels, autopct='%1.2f%%', colors=["black","dimgray","darkgray","lightgray"])
    for autotext in autotexts[:2]:
        autotext.set_color('white')
    # plt.savefig("./comparison-results/fastest-pie-NTCIR.png")
    plt.show()

wiki_data_analysis()