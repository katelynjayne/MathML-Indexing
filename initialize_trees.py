from bplustree_with_visualizer import GraphableBPlusTree
import os
from mathml_extractor import operator_extractor, operand_extractor
import pickle
from B_Tree import BTree

dataset_path = "./../../Downloads/dataset_full/dataset_full/math/"
ntcir_path = "./../../Downloads/NTCIR-12_Data/MathArticles/"

def bplustree_builder():
    '''
    This method must be run first on any new machine in order to create and pickle the B+ tree.
    For it to function properly, please change the dataset_path variable above to the location of the math folder within the dataset on your machine.
    The tree will be saved in the binary file pickled_bplus_tree.txt
    '''
    bplustree = GraphableBPlusTree(order=3)
    all_the_folders = os.listdir(dataset_path)

    for folder in all_the_folders:
        if ".DS_Store" not in folder:
            question_path = f"{dataset_path}{folder}/question/"
            answer_path = f"{dataset_path}{folder}/answers/"
            for file in os.listdir(question_path):
                whole_path = question_path + file
                num_operands = operand_extractor(whole_path)
                indexes = operator_extractor(whole_path)
                for index in indexes:
                    bplustree.insert(index, (whole_path, num_operands))
            for file in os.listdir(answer_path):
                whole_path = answer_path + file
                num_operands = operand_extractor(whole_path)
                indexes = operator_extractor(whole_path)
                for index in indexes:
                    bplustree.insert(index, (whole_path, num_operands))

    with open('./pickled_bplus_tree.txt', 'wb') as file:
        pickle.dump(bplustree,file)
    # bplustree.show_all_data()

def btree_builder():
    '''
    This method must be run first on any new machine in order to create and pickle the B tree.
    For it to function properly, please change the dataset_path variable above to the location of the math folder within the dataset on your machine.
    The tree will be saved in the binary file pickled_b_tree.txt
    '''
    btree = BTree(3)
    all_the_folders = os.listdir(dataset_path)

    for folder in all_the_folders:
        if ".DS_Store" not in folder:
            question_path = f"{dataset_path}{folder}/question/"
            answer_path = f"{dataset_path}{folder}/answers/"
            for file in os.listdir(question_path):
                whole_path = question_path + file
                num_operands = operand_extractor(whole_path)
                indexes = operator_extractor(whole_path)
                for index in set(indexes):
                    btree.insert(index, (whole_path, num_operands))
            for file in os.listdir(answer_path):
                whole_path = answer_path + file
                num_operands = operand_extractor(whole_path)
                indexes = operator_extractor(whole_path)
                for index in set(indexes):
                    btree.insert(index, (whole_path, num_operands))

    with open('./pickled_b_tree.txt', 'wb') as file:
        pickle.dump(btree, file)
    # btree.printTree(btree.root)

def bplus_tree_add():
    with open("./pickled_bplus_tree.txt", "rb") as file:
        bplustree = pickle.load(file)

    folders = os.listdir(ntcir_path)
    for folder in folders:
        articles = os.listdir(f"{ntcir_path}{folder}")
        for article in articles:
            path_to_article = f"{ntcir_path}{folder}/{article}/"
            for file in os.listdir(path_to_article):
                whole_path = path_to_article + file
                num_operands = operand_extractor(whole_path, "")
                indexes = operator_extractor(whole_path, "")
                for index in indexes:
                    bplustree.insert(index, (whole_path, num_operands))

    with open('./new_pickled_bplus_tree.txt', 'wb') as file:
        pickle.dump(bplustree, file)
    

def b_tree_add():
    with open("./pickled_b_tree.txt", "rb") as file:
        btree = pickle.load(file)

    folders = os.listdir(ntcir_path)
    for folder in folders:
        articles = os.listdir(f"{ntcir_path}{folder}")
        for article in articles:
            path_to_article = f"{ntcir_path}{folder}/{article}/"
            for file in os.listdir(path_to_article):
                whole_path = path_to_article + file
                num_operands = operand_extractor(whole_path, "")
                indexes = operator_extractor(whole_path, "")
                for index in set(indexes):
                    btree.insert(index, (whole_path, num_operands))

    with open('./new_pickled_b_tree_2.txt', 'wb') as file:
        pickle.dump(btree, file)

if __name__ == "__main__":
    # print("Editing B+ tree...")
    # bplus_tree_add()
    # print("B+ tree finished!")
    print("Editing B tree...")
    b_tree_add()
    print("B tree finished!")

    with open("./new_pickled_b_tree.txt", 'rb') as file:
        btree = pickle.load(file)

    # btree.printTree(btree.root)
    node, idx = btree.search("succ")
    print(len(node.values[idx])) # should be 21!
