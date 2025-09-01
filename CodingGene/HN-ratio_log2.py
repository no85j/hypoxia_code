#HN-ratio_log2.ipynb改良版
#実行コマンド例 python ./HN-ratio_log2.py --expression ./data/TPM.tsv --pair ./data/HN-pair.tsv --output ./data/HN-ratio
#上記コマンドで実行した際出力ファイルはHN-ratio.csv,HN-ratio_log2.csvの２つ

import pandas as pd
import numpy as np
import argparse
import os

#引数の受け取り
parser = argparse.ArgumentParser(description='腫瘍と正常のTPMデータから発現比とlog2比を計算するスクリプト')
parser.add_argument('--expression', required=True, help='遺伝子発現データファイル(tsv)')
parser.add_argument('--pair', required=True, help='腫瘍-正常ペアの対応ファイル(tsv)')
parser.add_argument('--output', default='./HN-ratio', help='出力ファイル(拡張子は不要)')
args = parser.parse_args()

#入力ファイルの読み込み
df = pd.read_csv(args.expression, sep='\t', index_col=0)
HN = pd.read_csv(args.pair ,sep='\t')

#確認用
print("TPM 値の確認")
h = HN.iloc[0, 0]
n = HN.iloc[0, 1]
print(f"{h} の TPM 値:")
print(df[h].head(5))
print(f"{n} の TPM 値:")
print(df[n].head(5))

print("ペアファイルの確認")
print("HN head:")
print(HN.head())

#H/N比の計算
results = {}

for i in range(len(HN)):
    h = str(HN.iloc[i,0])
    n = str(HN.iloc[i,1])
    if h in df.columns and n in df.columns:
        colname = f"{h} VS {n}"
        results[colname] = (df.loc[:,h] + 1)/(df.loc[:,n]+1)
    else:
        print(f"Warning: {h} または {n} が df に存在しません")

HNratio = pd.DataFrame(results)
HNratio.insert(0, "GeneName", df.index)

#確認用
print("HNratio の計算結果(5行):")
print(HNratio.head())

#log2変換
HNratio_ = HNratio.set_index('GeneName')
HNratiolog2 = HNratio_.apply(np.log2)
HNratiolog2 = HNratiolog2.reset_index()

#確認用
print("HNratiolog2 の計算結果(5行):")
print(HNratiolog2.head())

#出力
outdir = os.path.dirname(args.output)
os.makedirs(outdir, exist_ok=True)
HNratio_.to_csv((f"{args.output}.csv"), sep=",")
HNratiolog2.set_index('GeneName').to_csv((f"{args.output}_log2.csv"), sep=",")
