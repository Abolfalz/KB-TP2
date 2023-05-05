from multiprocessing import Value
from turtle import st
from typing_extensions import Self
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
import time
import copy

data = pd.read_csv("C:\\Users\\AM\\Desktop\\pkn2\\groceries.csv", header = None)

# Market_Basket_Optimisation
# groceries

# cr = count row
cr = data.shape[0]
print(data.isna())

print('\n\n')
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

# dic have all kala
all_kala = {}

for sub_lst in list_all:
    for item in sub_lst:
        if item in all_kala:
            all_kala[item] += 1
        else:
            all_kala[item] = 1

# ------------------------------------------------------------------


# ------------------------------------------------------------------
# ماکزیمم و مینیمم تعداد کالا در خریدها و همچنین تعداد کل تراکنش هاس
# Length, Minimum length, Maximum length
minmax = [len(lst) for lst in list_all]
min_length = min(minmax)
max_length = max(minmax)
print(f"Length - Rows Count:\t {len(list_all)}\n")
print(f"Minimum Buy Item in each Transaction:\t {min_length}")
print(f"Maximum Buy Item in each Transaction:\t {max_length}")
print('\n\n')
# ------------------------------------------------------------------


# ------------------------------------------------------------------
#  میانگین تعداد کالا در هر تراکنش‌ها
# Mean
total_items = sum(len(lst) for lst in list_all)
avg_items = total_items / len(list_all)
print("Mean Item in Transactions:\t ", avg_items)
print('\n\n')
# ------------------------------------------------------------------


# ------------------------------------------------------------------
# میانه تعداد کالا در هر تراکنش‌ها
# Median
sorted_list = sorted(list_all, key=len)
n = len(sorted_list)
if n % 2 == 0:
    m1 = sorted_list[n//2 - 1]
    m2 = sorted_list[n//2]
    median = (len(m1) + len(m2)) / 2
else:
    median = len(sorted_list[n//2])
print("Median Item in Transactions:\t ", median)
print('\n\n')
# ------------------------------------------------------------------


# ------------------------------------------------------------------

# کالاهایی که کمترین و بیشترین تعداد فروش را داشته‌اند
smallest_value = min(all_kala.values())
smallest_keys = [key for key, value in all_kala.items() if value == smallest_value]

largest_value = max(all_kala.values())
largest_keys = [key for key, value in all_kala.items() if value == largest_value]

print("Minimum sell of commodity:", smallest_value)
print("commodity is:", smallest_keys)
print("Maximum sell of commodity:", largest_value)
print("commodity is:", largest_keys)
print('\n\n')
# ------------------------------------------------------------------


# ------------------------------------------------------------------
# نمودار تعداد کالا در هر خرید به همراه فراوانی آن
list_n_buy = {}
len_tran = [len(lst) for lst in list_all]
for i in len_tran:
        if i in list_n_buy:
            list_n_buy[i] += 1
        else:
            list_n_buy[i] = 1

list_n_buy = dict(sorted(list_n_buy.items(), key=lambda item: item[0]))
x = list(list_n_buy.keys())
y = list(list_n_buy.values())
plt.bar(x, y)
plt.xlabel('Number of Items in Transaction')
plt.ylabel('Frequency')

for i in range(len(x)):
    plt.text(x[i], y[i], str(y[i]), ha='center', va='bottom')
plt.show()
# ------------------------------------------------------------------


# ------------------------------------------------------------------
# نمودار تعداد کالا در هر خرید به همراه فراوانی آن
data_list = [v for k, v in list_n_buy.items()]
plt.boxplot(data_list)
plt.show()
# ------------------------------------------------------------------



sorted_dict = dict(sorted(all_kala.items(), key=lambda item: item[1], reverse = True))
values = []
keys = list(sorted_dict.keys())

for i,j in sorted_dict.items():
    values.append(j/cr)

plt.bar(keys, values)
plt.show()