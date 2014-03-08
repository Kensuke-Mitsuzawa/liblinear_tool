# Liblinear tools

# What's this ??
Tools for liblinear.
For libsvm, there are useful tools. However, they does not fit to liblinear. We need to rewrite them for liblinear. That's very inconvenient. Thus, I opened tools for liblinear.

# Tools in this repo.
* scaling feature value
* grid searching of hyperparameter C and xi
* feature selection tuning on F-value

# Files You need
* liblinear: I confirmed at version 1.94
* svm-scale: svm-scale exists in libsvm package. svm-scale is need to scale feature values

# Usage
## scaling feature value and grid searching
use ./tools/liblin_easy.py

### 1: you have to rewrite header to change path for your environment

    #you can re-write for your environment 
    svmscale_exe='../svm-scale';
    liblinear_exe='../liblinear-1.94/train';
    grid_py='/home/kensuke-mi/opt/libsvm-3.17/tools/grid.py';
    import re, subprocess, os, sys;
    #you can re-write for your environment 
    sys.path.append('../liblinear-1.94/python/');
    import liblinear, liblinearutil;

### 2: specify path to training file and test file

    train_pathname='../heart_scale'
    test_pathname='../heart_scale'

### 3: initialize instance
    
    test01=Liblin_easy(train_pathname,test_pathname)
----
To scale feature values
    
    test01.scalling_value()
----
To parameter tuning with grid search. You can tune parameters for other files, if you rewrite argument of this method.

    test01.grid_search(train_pathname)
---
If you use `easy_tuning()`, it automatically do scaling and grid search on training file

    test01.easy_tuning()

## Acknowledgement
### I really thank to team member of liblinear and libsvm
