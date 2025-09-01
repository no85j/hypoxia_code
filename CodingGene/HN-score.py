#HN-score.ipynb改良版
#実行コマンド例 python ./HN-score.py --ratio ./data/HN-ratio.csv --threshold 1.5 2 2.5 --output ./data/HN-score.csv

import pandas as pd
import numpy as np
import argparse
import os

#引数の受け取り
parser = argparse.ArgumentParser(description='発現変動比からHN-scoreを算出するスクリプト')
parser.add_argument('--ratio', required=True, help='HN-ratioファイル(csv)')
parser.add_argument('--threshold', default=[1.5,2], type=float, nargs='+', help='閾値をスペース区切りで指定(複数可）')
parser.add_argument('--output', default='./HN-score.csv', help='出力ファイル')
args = parser.parse_args()

#入力ファイルの読み込み
df = pd.read_csv(args.ratio, sep=',')
df1=df.set_index('GeneName')

#確認用
print("入力ファイルの確認")
print(df.head())

#HN-scoreの算出
temp = pd.DataFrame()

temp["all"] = (df1>=0).sum(axis=1)

thresholds = args.threshold

for t in thresholds:
    label = str(t)
    temp[f"up{label}"] = (df1 >= t).sum(axis=1)
    temp[f"down{label}"] = (df1 <= 1/t).sum(axis=1)
    temp[f"unchange{label}"] = temp[f"all"] - temp[f"up{label}"] - temp[f"down{label}"]
    temp[f"HN{label}"] = temp[f"up{label}"] - temp[f"down{label}"]

temp=temp.reset_index()

#確認用
print("HN-score計算結果(５行)")
print(temp.head())

#出力
outdir = os.path.dirname(args.output)
os.makedirs(outdir, exist_ok=True)
temp.to_csv(args.output, sep=",", index=False)
