import pandas
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from statistics import mean


df = pandas.read_csv("./bplus_vs_seq_results.csv")

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


# # Calculate the correlation coefficient
# correlation = np.corrcoef(operators, differences)[0, 1]
# print(f'Correlation Coefficient: {correlation}')

# Fit a line to the data
m, b = np.polyfit(operators, differences, 1)

plt.scatter(operators, differences, edgecolors='w', linewidth=0.5, label="Data Points")
plt.plot(operators, m*operators + b, color='red', label=f'Trend Line (y={m:.2f}x + {b:.2f})')
plt.xlabel("Amount of Operators")
plt.ylabel("Difference")
plt.legend()
# plt.show()

counter = 0
for result in samesies:
    if result:
        counter += 1

print(f"Percent True: {counter / len(samesies)}")


'''
Avg B+ Time: 743.073165713258
Avg Seq Time: 80398.66825241354
Correlation Coefficient: -0.2360261919465195
P-value: 0.0007430960024968117
The correlation is statistically significant.
Percent True: 0.7263681592039801
'''
print("--------------------------------------------")

df2 = pandas.read_csv("./comparison_data.csv")

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

'''
Avg B+ time: 754.9190900812101
Avg sec time: 7203.132819180465
Avg B+ score: 0.8285296726625021
Avg sec score: 0.8768250618743398
Both had at least one score of 1 for every file.
'''

'''
B-Tree and B+-Tree got the SAME results. TINIEST difference in speed.
Avg B+ time: 676.0913367066986
Avg B time: 914.8397937434297
'''