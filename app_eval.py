
quer_result_dict = {}

with open("./comparison-results/Approach-0-Raw-Results", 'r', encoding='utf-8') as file:
    for line in file.readlines():
        elements = line.split()
        quer = elements[0]
        result = elements[2]
        if quer not in quer_result_dict:
            quer_result_dict[quer] = []
        quer_result_dict[quer].append(result)

print(len(quer_result_dict))