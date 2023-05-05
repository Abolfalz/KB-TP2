from tkinter import N
from turtle import st
from typing_extensions import Self
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
import time
import copy

data = pd.read_csv("C:\\Users\\AM\\Desktop\\T2\\groceries.csv", header=None)

# Market_Basket_Optimisation
# groceries

# cr = count row
cr = data.shape[0]

# list_all = all transaction
list_all = []

for i in range(cr):
    j = 0
    li = []
    try:
        while not pd.isna(data[j][i]):
            li.append(data[j][i])
            j = j + 1
    except:
        pass
    list_all.append(li)

min_support = int(0.005 * cr)


class Arules:
    def get_frequent_item_sets(self, transactions, min_support):
        list_k_itemset = []
        dic_item_set = {}
        sorted_key_dic = []
        list_not_dup = []
        min_support = int(min_support * len(transactions))
        all_kala = {}
        for sub_lst in transactions:
            for item in sub_lst:
                if item in all_kala:
                    all_kala[item] += 1
                else:
                    all_kala[item] = 1

        # k1_item_set = {}
        for key, value in all_kala.items():
            if value >= min_support:
                dic_item_set[key] = value
        list_k_itemset.append(dic_item_set)
        dic_item_set = {}

        # k2_item_set = {}
        for i, (key1, value1) in enumerate(list_k_itemset[0].items()):
            for key2, value2 in list(list_k_itemset[0].items())[i+1:]:
                if key1 != key2:
                    count = 0
                    for sublist in transactions:
                        if key1 in sublist and key2 in sublist:
                            count += 1
                    if count >= min_support:
                        dic_item_set[tuple(sorted([key1, key2]))] = count
        list_k_itemset.append(dic_item_set)
        dic_item_set = {}

        # k3-4-5 item_set = {}
        k = 3
        stp = True
        while stp:
            sorted_key_dic = []
            dic_item_set = {}
            sorted_key_dic = sorted(list_k_itemset[k-2].keys())
            myd = {}
            lp = []
            for item in sorted_key_dic:
                if len(item) == 2:
                    key, value = item
                    if key in myd:
                        myd[key].add(value)
                    else:
                        myd[key] = {value}
                elif len(item) > 2:
                    lp = item
                    value = lp[-1]
                    if tuple(lp[:k-2]) in myd:
                        myd[tuple(sorted(lp[:k-2]))].add(value)
                    else:
                        myd[tuple(sorted(lp[:k-2]))] = {value}
            for key in myd:
                if k > 3:
                    l = list(key)
                else:
                    l = key
                values = myd[key]
                if len(values) >= 1:
                    if k > 3:
                        triple = l + sorted(list(values))
                    else:
                        triple = [l] + sorted(list(values))
                    combinations_list = list(combinations(triple, k))
                    for ls in combinations_list:
                        a = sorted(ls)
                        if a not in list_not_dup:
                            list_not_dup.append(a)
                            count = 0
                            for sublist in list_all:
                                if all(elem in sublist for elem in a):
                                    count += 1
                            if count >= min_support:
                                dic_item_set[tuple(sorted(a))] = count
            list_k_itemset.append(dic_item_set)
            if len(list_k_itemset[-1]) == 0:
                list_k_itemset.pop()
                stp = False
            k += 1
        sorted_dict=[]
        for t in list_k_itemset:
            sorted_dict.append(dict(sorted(t.items(), key=lambda x: x[1], reverse = True))) 

        return list_k_itemset, sorted_dict

    def get_arules(self, fre, count_tranc, min_support=None, min_confidence=None, min_lift=None, sort_by='lift'):
        rules = []
        count_result = 0
        count_moghadam = 0
        all = 0
        for k in fre[1:]:
            l = list(k.keys())
            for kis in l:
                kis = list(kis)
                list_koli = copy.deepcopy(kis)
                for i in range(0, len(list_koli)):
                    result = kis[i]
                    del kis[i]
                    moghadam = kis
                    count_result = fre[0][result]
                    if len(list_koli) == 2:
                        count_moghadam = fre[0][moghadam[0]]
                    else:
                        count_moghadam = fre[len(list_koli)-2][tuple(moghadam)]
                    kis = copy.deepcopy(list_koli)
                    all = fre[len(list_koli)-1][tuple(kis)]
                    sup = all/count_tranc
                    conf = all/count_moghadam
                    lift = sup/((count_moghadam/count_tranc)*(count_result/count_tranc))
                    if conf >= min_confidence:
                        rules.append([moghadam,result,sup,conf,lift])
        sorted_list = sorted(rules, key=lambda x: x[-1], reverse=True)
        return sorted_list


ccl = Arules()

start = time.time()
frequent_item_set, sortdic = ccl.get_frequent_item_sets(list_all, min_support = 0.005)
done = time.time()
elapsed = done - start
print('Time Run get_frequent_item_sets:   ',elapsed)

ck = 1
for i in sortdic:
    #print(i)
    #df = pd.DataFrame.from_dict(i)
    print('Item set:\t',ck)
    df = pd.DataFrame(data=i.items(), columns=['Item Set', 'Count'])
    df['Support'] = df['Count'] /cr
    #df = df.reset_index()
    pd.set_option('display.max_colwidth', None)
    print(df.head(10))
    print('Total Number of Item set is:\t',len(i))
    print('\n')
    '''if ck == 1:
        df.to_csv('C:\\Users\\AM\\Desktop\\T2\\frequent_item_sets.csv', index=False)
    else:
        df.to_csv('C:\\Users\\AM\\Desktop\\T2\\frequent_item_sets.csv', mode = 'a', header = False, index = False)'''
    ck +=1

start = time.time()
ass_ru = ccl.get_arules(frequent_item_set, cr, min_support = 0.005, min_confidence = 0.2)
done = time.time()
elapsed = done - start
print('Time Run get_arules:   ',elapsed)
print(len(ass_ru))

dfr = pd.DataFrame(ass_ru, columns=['IF', 'THEN', 'Support','Confidence','Lift'])
#dfr.to_csv('C:\\Users\\AM\\Desktop\\T2\\rulse.csv', index=False)
print(dfr.head(50))