from mathml_extractor import operator_extractor, operand_extractor, structure_scores
import pickle
from statistics import mean

def get_top_matches(file_score_dict):
    '''
    This will return a list of approximately 10 files, ranked by score.
    If there are more than 10 files with the top score, all are included.
    '''
    ranked_files_with_score = sorted(file_score_dict.items(), key=lambda item: item[1], reverse=True)
    ranked_files = [file[0] for file in ranked_files_with_score[:10]]

    if len(ranked_files) == 10 and len(ranked_files_with_score) > 10:
        min_score = ranked_files_with_score[9][1]
        if min_score == ranked_files_with_score[10][1]: # There are more than 10 files with the top score, add all with this score.
            for file, score in ranked_files_with_score[10:]:
                if score == min_score:
                    ranked_files.append(file)
                else:
                    break
        
        # elif min_score == ranked_files_with_score[10][1]: # If there are more files with the same score as the tenth, remove all with that score to prevent a too long list of results.
        #     for file, score in reversed(ranked_files_with_score[:10]):
        #         if score == min_score:
        #             ranked_files.remove(file)
        #         else:
        #             break

    return ranked_files

def get_max_score(file_score_dict):
    '''
    This method takes in the dictionary of scores as an argument, and returns the maximum score.
    '''
    if file_score_dict:
        scores = file_score_dict.values()
        return max(scores)
    return 0

def get_min_score(file_score_dict, ranked_files):
    '''
    This method takes in the dictionary of scores and the list of top files.
    Returns the smallest score of the files that were returned by get_top_matches().
    '''
    ranked_files_with_score = sorted(file_score_dict.items(), key=lambda item: item[1], reverse=True)
    num_matches = len(ranked_files)
    return ranked_files_with_score[num_matches - 1][1]

def get_avg_score(file_score_dict, ranked_files):
    '''
    This method takes in the dictionary of scores and the list of top files.
    Returns the average score of the files that were returned by get_top_matches().
    '''
    if file_score_dict:
        ranked_files_with_score = sorted(file_score_dict.items(), key=lambda item: item[1], reverse=True)
        num_matches = len(ranked_files)
        scores = [score for file, score in ranked_files_with_score[:num_matches]]
        return mean(scores)
    return 0

def query_bplus_tree(filename: str) -> list[str]:
    '''
    Given the name of a MathML file, this method will return the top matches from the dataset.
    They are ranked first by number of operators in common, then by difference between number of operands.
    If the MathML cannot be parsed, returns an empty list.
    '''
    symbols = set(operator_extractor(filename, ''))
    numbers, identifiers = operand_extractor(filename, '', version=2)
    # og_above, og_sup, og_sub, og_below, og_contains, og_lsup, og_lsub = structure_scores(filename, "")

    with open('./bplus_tree_idens_extracted.txt', 'rb') as file:
        bplustree = pickle.load(file)

    counts = {}
    for symbol in symbols:
        retrieved = bplustree.retrieve(symbol)
        if retrieved:
            for tuple in retrieved:
                file = tuple[0]
                nums = tuple[1]
                idens = tuple[2]
                # above, sup, sub, below, contains, lsup, lsub = tuple[3]
                operands_diff = -abs(numbers - nums) + -abs(identifiers - idens)
                # The negative absolute value is taken so that the greater difference will be a smaller number for ranking purposes.
                # struct_diff = -abs(og_above - above) + -abs(og_sup - sup) + -abs(og_sub - sub) + -abs(og_below - below) + -abs(og_contains - contains) + -abs(og_lsup - lsup) + -abs(og_lsub - lsub)
                if file in counts:
                    counts[file][0] += 1
                else:
                    counts[file] = [1, operands_diff]

    return get_top_matches(counts)

def query_b_tree(filename):
    symbols = set(operator_extractor(filename, ""))
    num_operands = operand_extractor(filename, "")

    with open('./new_pickled_b_tree.txt', 'rb') as file:
        btree = pickle.load(file)

    counts = {}
    for symbol in symbols:
        retrieved = btree.search(symbol)
        if retrieved:
            node, idx = retrieved
            retrieved_files = node.values[idx]
            for couple in retrieved_files:
                file, operands = couple
                if file in counts:
                    counts[file][0] += 1
                else:
                    diff = -abs(num_operands - operands)
                    counts[file] = [1, diff]
    return get_top_matches(counts)


if __name__ == "__main__":
    pass
    