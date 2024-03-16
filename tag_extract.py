import os
import sys
import json

# pip install mecab-python3
# pip install unidic-lite
import MeCab
mecab = MeCab.Tagger("mecabrc")

def ma_parse(sentence):
  noun_count = {}
  node = mecab.parseToNode(sentence)
  while node:
      word = node.surface
      hinshi = node.feature.split(",")[0]
      if word in noun_count.keys() and hinshi == "名詞":
          noun_freq = noun_count[word]
          noun_count[word] = noun_freq + 1
      elif hinshi == "名詞":
          noun_count[word] = 1
      else:
          pass
      node = node.next
      
  noun_count = sorted(noun_count.items(), key=lambda x:x[1], reverse=True)
  return noun_count

def extract(text):
  words = [pair[0] for pair in ma_parse(sentence)[:100]]
  print(words)
  return words

if __name__ == '__main__':

  sentence = "ここに述べる理論は、今日一般に「相対性理論」と呼ばれている理論*3の、考えうる限り一般化したものである。以下ではこの新しい理論を「相対性理論」と呼び以前の「特殊相対性理論」とは区別するとともに、後者の知識を前提とする。相対性理論の一般化は、ミンコフスキーにより与えられた特殊相対論の形式によって、大いに容易となった。かの数学者は空間座標と時間座標の等価性を初めて見出し、私の理論に使いやすい形にしてくれた。一般相対論に必要な数学的道具は、ガウス、リーマン、クリストッフェルによる非ユークリッド的*4な多様体*5の研究に基づき、リッチ、レヴィ・チヴィタにより統合され、既に理論物理学の問題に利用されている、絶対微分幾何学の中で既に完成されている。この論文の理解のために数学書を勉強する必要が無いよう、私はチャプターB*6の中で、我々に必要だが、物理学者にとって当然の前提とはされない数学的道具を全て、できる限り簡単にそして見通しの良い形で構築した。最後にこの場を借りて私の友人であり数学者のグロスマンに感謝したい。彼のおかげで関連する数学書の勉強を省くことができたし、彼は私が重力場の方程式*7を見つけるのも助けてくれた。"
  words = [pair[0] for pair in ma_parse(sentence)[:100]]
  print(words)
