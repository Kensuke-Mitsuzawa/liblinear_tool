#! /usr/bin/python
# -*- coding:utf-8 -*-
__author='Kensuke Mitsuzawa'
__date__='2014/1/21'

"""
libsvm toolのfselect.pyを使って，有意な特徴量のみを取り出すスクリプト
usage:python f_based_feature_selection.py path_to_trainfile
RETURN:有意な特徴量だけで構成されたtrainファイル
"""

import os,codecs,re,sys,subprocess

def excute_fselect(trainfile_path):
    """
    fselect.pyを実行して，F値をベースに素性選択をさせる．
    RETURN:NONE
    """
    cwd='./'
    args=['python', 'fselect.py', trainfile_path]
    subproc_args = {'stdin': subprocess.PIPE,
                    'stdout': subprocess.PIPE,
                    'stderr': subprocess.STDOUT,
                    'cwd': cwd,
                    'close_fds' : True,}
    try:
        p=subprocess.Popen(args, shell=False, **subproc_args);
    
    except OSError:
        print "Failed to execute command: %s" % args[0];
        sys.exit(1);

    (stdouterr, stdin) = (p.stdout, p.stdin)
    print "-" * 80
    while True:
        line = stdouterr.readline()
        if not line:
            break
        print line.rstrip()

    return True;

def check_selected_feat(trainfile_path):
    """
    選択された素性番号のみをファイルから読み込み
    RETURN: list selected_features[ float feature_number ]
    """
    selecetfile=os.path.basename(trainfile_path)+'.select';
    with codecs.open(selecetfile, 'r', 'utf-8') as lines:
        for line in lines:
            if re.search(ur'select\sfeatures\:\s\[.+\]', line):
                processed_line=line.strip().strip(u'select features: [').strip(u']');
                selected_features=[float(t) for t in processed_line.split(u',')];
    return selected_features;

def preprocess_original_inputfile(trainfile_path):
    """
    元の訓練ファイルを構造化してデータにしておく
    RETURN: list original_data [ tuple one_instance (unicode label,list feature_and_value [float feature_number,float feature_value])]
    """
    train_data=[];
    with codecs.open(trainfile_path, 'r', 'utf-8') as lines:
        for line in lines:
            elements=line.split();
            label=elements[0];
            features=[[float(e) for e in  f.split(u':')] for f in elements[1:]] 
            train_data.append((label,features));
    return train_data;

def cutoff_unwanted_features(train_data,selected_features):
    after_data=[];
    for one_instance in train_data:
        label=one_instance[0];
        features=[];
        for feature_tuple in one_instance[1]:
            if feature_tuple[0] in selected_features:
                features.append(feature_tuple); 
        after_data.append([label, features]) 
   
    return after_data

def out_after_data(after_data,trainfile_path):
    outpath=os.path.basename(trainfile_path)+'.after'
    with codecs.open(outpath, 'w', 'utf-8') as f:
        for one_instance in after_data:
            #特徴量と特徴量の値を文字型に直して，libsvm formatに書き換える作業
            features=u' '.join([str(f_tuple[0]).strip(u'.0')+u':'+str(f_tuple[1]) for f_tuple in one_instance[1]])
            label=one_instance[0];
            
            f.write(label+u' '+features+u'\n');

if __name__=='__main__':
    trainfile_path=sys.argv[1];
    excute_fselect(trainfile_path);
    selected_features=check_selected_feat(trainfile_path);
    train_data=preprocess_original_inputfile(trainfile_path);
    after_data=cutoff_unwanted_features(train_data,selected_features);
    out_after_data(after_data,trainfile_path)
