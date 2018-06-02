import os

import numpy as np
from sklearn import svm
from sklearn.model_selection import ShuffleSplit, cross_val_score

from kernels.MLG import MLGKernel
from kernels.glocalwl import GlocalWLKernel
from kernels.GraKeL import GrakelKernel

def read_label_matrix(line):
    return line.strip()


def read_kernel_matrix(line):
    return line.strip().split(' ')


def read_matrix(file_path, formatter):
    def read():
        with open(file_path, 'r') as f:
            for line in f:
                yield formatter(line)
    return np.array(list(read()))


def score_n_fold(train, test, n, c):
    cv = ShuffleSplit(n_splits=n, test_size=0.33)
    clf = svm.SVC(kernel='precomputed', C=c, class_weight='balanced')
    return cross_val_score(clf, train, test, cv=cv).mean(), c


def evaluate(kernel, dataset_name, output_path, data_dir):
    #kernel = kernel_class(dataset_name, output_path, data_dir)
    kernel.compile()
    kernel.load_data()
    kernel_matrices_paths = kernel.compute_kernel_matrices()
    kernel_matrices_path = kernel_matrices_paths[0]
    label_path = os.path.join(data_dir, dataset_name,
                              '{}_graph_labels.txt'.format(dataset_name))
    kernel_matrices = read_matrix(kernel_matrices_path, read_kernel_matrix)
    labels = read_matrix(label_path, read_label_matrix)
    penalties = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
    scores = [score_n_fold(kernel_matrices, labels, 10, c) for c in penalties]
    return scores


if __name__ == '__main__':
    kernels = [MLGKernel]
    dataset_name = 'MUTAG'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(current_dir, 'tmp')):
        os.makedirs(os.path.join(current_dir, 'tmp'))
    output_path = os.path.join(current_dir, 'tmp', 'results')
    data_dir = os.path.join(current_dir, 'datasets')
    kernels = []
    #kernels.append(MLGKernel(dataset_name, output_path, data_dir))
    #those parameters might not be ideal, especiialy 1
    #kernels.append(GlocalWLKernel(dataset_name, output_path, data_dir, [["-l", "1", "-i"]], "WL3L"))
    #kernels.append(GlocalWLKernel(dataset_name, output_path, data_dir, [["-l", "2", "-i"]], "WL3L"))
    #kernels.append(GlocalWLKernel(dataset_name, output_path, data_dir, [["-l", "1", "-i"]], "WL2L")) #high runtime
    #kernels.append(GlocalWLKernel(dataset_name, output_path, data_dir, [["-l", "1", "-i"]], "WL3G"))
    #kernels.append(GlocalWLKernel(dataset_name, output_path, data_dir, [["-l", "1", "-i"]], "WL2G"))
    #kernels.append(GlocalWLKernel(dataset_name, output_path, data_dir, [["-l", "1", "-i"]], "ShortestPath")) #old, high runtime
    #kernels.append(GlocalWLKernel(dataset_name, output_path, data_dir, [["-l", "1", "-i"]], "ColorRefinement"))
    #kernels.append(GlocalWLKernel(dataset_name, output_path, data_dir, [["-l", "1", "-i"]], "Graphlet"))
    kernels.append(GrakelKernel(dataset_name, output_path, data_dir, [], "Propagation"))
    for kernel in kernels:            
        print(evaluate(kernel, dataset_name, output_path, data_dir))

