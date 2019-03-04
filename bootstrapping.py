# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 11:35:48 2019

@author: dominik.cichon
"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange
import pandas as pd






def bootstrap(test, control, q, c = .95, n_trials = 1000):
    print('[INFO] running bootstrapping with', n_trials, 'samples.')

    diffs = []
    test_list = []
    control_list = []
    test = pd.DataFrame(test)
    control = pd.DataFrame(control)

    if len(test.columns) > 1:
            print('[INFO] data has multiple columns. Calculating conversion rate (1st column / 2nd column).')
            

    
    for i in trange(0, n_trials):
        boot_test = pd.DataFrame(test).sample(int(len(test)/n_trials))
        boot_control = pd.DataFrame(control).sample(int(len(control)/n_trials))
        # If data has more than 1 column, calculate Conversion (1st column / 2nd column):
        if len(boot_test.columns) > 1:
            boot_test = sum(boot_test[boot_test.columns[0]])/sum(boot_test[boot_test.columns[1]])
            boot_control = sum(boot_control[boot_control.columns[0]])/sum(boot_control[boot_control.columns[1]])
            diffs.append(boot_test - boot_control)
            test_list.append(boot_test)
            control_list.append(boot_control)
        else:
            diffs.append(np.mean(boot_test)[0] - np.mean(boot_control)[0])
            test_list = test_list + list(boot_test[0])
            control_list = control_list + list(boot_control[0])
    
        lower_limit = np.percentile(diffs, ((1-c) / 2) * 100)
        upper_limit = np.percentile(diffs, ((1+c) / 2) * 100)

    histogram = plt.hist(diffs, bins = len(list(set(control_list))), range = (np.percentile(diffs, ((1-.99) / 2) * 100), np.percentile(diffs, ((1+.99) / 2) * 100)))
    #histogram = plt.hist(diffs, bins = len(list(set(control_list))))
    plt.axvline(0, color='lightgreen', linestyle='dashed', linewidth=1)
    plt.title('Histogram of Differences of Quantiles (99-Percentile)')
    plt.axvline(np.mean(diffs), color='m', linestyle='dashed', linewidth=1)
    plt.text(np.mean(diffs),max(histogram[0]),'Mean of Differences',rotation=0, color='m')
    plt.axvline(lower_limit, color='red', linestyle='dashed', linewidth=1)
    plt.text(lower_limit,-50, str(.95*100) + '% Confincence Interval', rotation=0, color='red')
    plt.axvline(upper_limit, color='red', linestyle='dashed', linewidth=1)
    plt.show()
    
    """
    plt.hist(test_list,label='test')
    plt.title('Distribution of test and control')
    plt.hist(control_list,label='control')
    plt.legend(loc='upper right')
    plt.show()
    """
        
    plt.plot(diffs)
    plt.title('Measured differences in each iteration')
    plt.axhline(np.mean(diffs), linewidth=1, color='m')
    plt.axhline(linewidth=1, color='r')
    plt.show()
    
    
    print('\n\n\n\n')
    print('Statistics:')
    print('------------------------------------------------')
    print('Trials:', n_trials)
    print(c, '% Confidence Intervall:', round(lower_limit, 4) ,' - ', round(upper_limit, 4))
    print('Mean of test:   ', round(np.mean(test_list), 4))
    print('Mean of control:', round(np.mean(control_list), 4))
    print('Difference:     ', round(np.mean(test_list)-np.mean(control_list), 4))
    print('Uplift:          ',round((np.mean(test_list)-np.mean(control_list)) / np.mean(control_list), 4)*100, '%')
    print(round(sum([i > 0 for i in diffs])/ len(diffs) * 100, 4), '% of trial differences > 0')
    print(round(sum([i < 0 for i in diffs])/ len(diffs) * 100, 4), '% of trial differences < 0')

    return control_list, test_list, diffs





"""
test = np.random.randint(100, size=100000) * 1.04
control = np.random.randint(100, size=100000)
n_trials = 10000
c = .95
q = .5

control_list, test_list, diffs = bootstrap(test, control, q, c = .95, n_trials = 1000)


"""