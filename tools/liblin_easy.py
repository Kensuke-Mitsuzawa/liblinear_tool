#! /usr/bin/python
# -*- coding:utf-8 -*-
__date__='2014/03/06';
__author__='Kensuke Mitsuzawa';

#you can re-write for your environment 
svmscale_exe='../svm-scale';
liblinear_exe='../liblinear-1.94/train';
grid_py='/home/kensuke-mi/opt/libsvm-3.17/tools/grid.py';
import re, subprocess, os, sys;
#you can re-write for your environment 
sys.path.append('../liblinear-1.94/python/');
import liblinear, liblinearutil;

class Liblin_easy:
    def __init__(self,train_pathname,test_pathname):
        self.train_pathname=train_pathname
        self.test_pathname=test_pathname

    def __call__(self):
        print 'Use grid_search(train_pathname) method for grid_search.'
        print 'You can scale feature values with scalling_value(train_pathname,test_pathname)' 

    def grid_search(self,target_file):
        #To check the C parameter for LIBLINEAR, use following command. "python grid.py -log2c -3,0,1 -log2g null -svmtrain ./train heart_scale"
        # from LIBLINEAR FAQ page: http://www.csie.ntu.edu.tw/~cjlin/liblinear/FAQ.html
        self.cmd='python {0} -log2c -3,0,1 -log2g null -svmtrain "{1}" "{2}"'.format(grid_py,liblinear_exe,target_file)
        print 'command for grid search is following:\n{}'.format(self.cmd);
        print('Cross validation...')
        self.f=subprocess.Popen(self.cmd,shell = True,stdout=subprocess.PIPE).stdout
        self.line=''
        while True:
            self.last_line=self.line
            self.line=self.f.readline()  
            if not self.line: break
        
        #outline format is [local] 0.0 92.7184 (best c=0.125, rate=94.0543)
        self.processed_line=re.sub(ur'\[local\]\s\.+\(best\sc=(.+),\srate=(.+)\)', ur'\1 \2',self.last_line);
        self.c,self.rate=map(float,self.processed_line.split());
        print('The result of grid search is Best c={0}, rate={1}'.format(self.c,self.rate));
        return self.c,self.rate;

    def scalling_value(self):
        assert os.path.exists(self.train_pathname),"training file not found"
        #self.file_name=os.path.basename(self.train_pathname);
        self.scaled_file=self.train_pathname+".scale"
        self.model_file=self.train_pathname+".model"
        self.range_file=self.train_pathname+".range"
        
        assert os.path.exists(self.test_pathname),"testing file not found"
        self.scaled_test_file=self.test_pathname + ".scale"
        self.predict_test_file=self.test_pathname + ".predict"
        
        self.cmd='{0} -s "{1}" "{2}" > "{3}"'.format(svmscale_exe,self.range_file,self.train_pathname,self.scaled_file)
        print('Scaling training data...')
        self.p=subprocess.Popen(self.cmd, shell = True, stdout = subprocess.PIPE).communicate() 
        
        self.cmd='{0} -r "{1}" "{2}" > "{3}"'.format(svmscale_exe,self.range_file,self.test_pathname,self.scaled_test_file)
        print('Scaling testing data...')
        self.p=subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE).communicate() 

        return self.scaled_file,self.scaled_test_file;

    def easy_tuning(self):
        #Do both of scalling and grid_search
        #grid_search is done on train_pathname file
        self.scaled_file,self.scaled_test_file=self.scalling_value()

        #Do grid_search on scalled training file
        self.c,self.xi=self.grid_search(self.scaled_test_file)

        return self.c,self.xi

if __name__=='__main__':
    #train_pathname=sys.argv[1];
    #test_pathname=sys.argv[2];
    #This is sample code
    #If train_pathname and test_pathname are same, no problem
    train_pathname='../heart_scale'
    test_pathname='../heart_scale'

    test01=Liblin_easy(train_pathname,test_pathname)
    
    #for scalling feature value
    #test01.scalling_value()

    #for grid_search of hyperparameter C and xi
    #You can tune to other files if you change argument of this method 
    #test01.grid_search(train_pathname)

    #do both of scalling and grid_search on scalled training file
    test01.easy_tuning()
