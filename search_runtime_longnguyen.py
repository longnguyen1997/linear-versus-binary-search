#!/usr/bin/env python3
# Author: Long Nguyen {lpn@mit.edu}. 2019.
import matplotlib.pyplot as plt
import numpy

from math import floor
from random import randint
from sys import maxsize
from time import time

# PRETASK: DEFINE FUNCTIONS.


def binary_search(A, n, T):
    '''
    Finds element T in sorted array
    A of size n using binary search.

    Returns -1 if index not found.
    '''
    L = 0
    R = n - 1
    while L <= R:
        m = int(floor((L + R) / 2))
        if A[m] < T:
            L = m + 1
        elif A[m] > T:
            R = m - 1
        else:
            return m
    return -1


def linear_search(A, n, T):
    '''
    Finds element T in sorted array
    A of size n with linear walkthrough.

    Returns -1 if index not found.
    '''
    L = 0
    while L < n:
        if A[L] == T:
            return L
        if A[L] > T:
            return -1
        L = L + 1
    return -1

# TASK 1: FIND THE THRESHOLD


def generate_rand_int_arr(array_size):
    return [randint(-maxsize - 1, maxsize) for i in range(array_size)]


def calculate_cpu_time(search_function, A, num_trials):
    cpu_time = 0
    for t in range(num_trials):
        before = time()
        search_function(A, len(A), A[randint(0, len(A) - 1)])
        after = time()
    cpu_time += after - before
    return cpu_time / num_trials


def run_performance_trials(num_trials=5, benchmark=False, array_size=None):
    '''
    Runs nums_trials random trials on binary vs.
    linear search runtime IN BENCHMARK MODE.

    Each random trial calculates CPU time spent
    finding a randomly selected key in an
    array of randomly generated ints.

    Returns the threshold calculated based on
    average of random trials if benchmarking.

    Returns average CPU time for both algorithms
    if not benchmarking, contingent on array_size
    being passed in.
    '''

    # Minimum 2 elements.
    # Single element is trivial.
    threshold = 2 if array_size is None else array_size

    while True:
        binary_search_perf = linear_search_perf = float('inf')
        array = generate_rand_int_arr(threshold)
        array.sort()
        '''
        I wanted to use Linux's perf stat to get better
        information regarding cache hits/misses
        and CPU time, but since this is just a
        Python script, it'll have to do.
        '''
        binary_search_perf = calculate_cpu_time(
            binary_search, array, num_trials)
        binary_search_perf /= num_trials
        linear_search_perf = calculate_cpu_time(
            linear_search, array, num_trials)
        linear_search_perf /= num_trials
        if not benchmark:
            return linear_search_perf, binary_search_perf
        if benchmark and binary_search_perf < linear_search_perf:
            return threshold
        threshold += 1


def find_threshold():
    '''
    Find the threshold at which binary performs
    better than linear search.

    Runs num_trials=250 random trials for performance trials.
    Averages over the averaged trials to account
    for wide ranges of thresholds.
    '''
    return sum(run_performance_trials(250, True) for i in range(100)) / 100

# TASK 2: PLOT


def get_model(linear, data):
    if linear:
        # Following y = mx + b model, classic slope model.
        b = min(data)
        b_index = data.index(b)
        slowest_time = max(data)
        slowest_index = data.index(slowest_time)
        m = (slowest_time - b) / (slowest_index - b_index)
        return lambda array_size: m * array_size + b
    else:
        # Following y = a + (b * lnx) model.
        # Use polyfit, taken from https://stackoverflow.com/a/3433503.
        b, a = numpy.polyfit(numpy.log(numpy.array(
            [i for i in range(1, len(data) + 1)])), numpy.array(data), 1)
        # numpy.log is natural logarithm.
        return lambda array_size: a + (b * numpy.log(array_size))


def plot_performance(max_array_size=50, num_trials=250):
    '''
    Runs performance trials based on maximum array size
    specified and plots the results.

    Returns calculated models for linear and binary search.
    '''
    linear_y = []
    binary_y = []
    for size in range(1, max_array_size + 1):
        linear_perf, binary_perf = run_performance_trials(
            num_trials, array_size=size)
        linear_y.append(linear_perf)
        binary_y.append(binary_perf)
    linear_model = get_model(True, linear_y)
    binary_model = get_model(False, binary_y)
    plt.plot(linear_y, 'o', label='Linear search')
    plt.plot(binary_y, 'o', label='Binary search')
    # Clunky code. Should be refactored to avoid performance
    # due to array gneration twice.
    plt.plot([i for i in range(1, max_array_size + 1)], [linear_model(i)
                                                         for i in range(1, max_array_size + 1)])
    plt.plot([i for i in range(1, max_array_size + 1)], [binary_model(i)
                                                         for i in range(1, max_array_size + 1)])
    plt.legend()
    plt.xlim(left=1)
    plt.title('Linear versus binary search runtime')
    plt.xlabel('Size of array')
    plt.ylabel('CPU time')
    plt.show()
    return linear_model, binary_model

# TASK 3: MODEL

linear, binary = plot_performance(350)