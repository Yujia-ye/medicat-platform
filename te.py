# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

def change(df):
    if type(df['概述']) == float:
        df['概述'] = '无'
    else:
        df['概述'] = df['概述'].replace('\n', '')
        df['概述'] = df['概述'].replace('\t', '')
        df['概述'] = df['概述'].replace('\r', '')
        df['概述'] = df['概述'].replace(' ', '')
    return df['概述']


ill = pd.read_csv('ill_book.csv')
print(ill.head())
ill['概述'] = ill.apply(lambda x: change(x), axis=1)
print(ill['概述'])
ill.to_csv('ill_book_.csv', index=False)
