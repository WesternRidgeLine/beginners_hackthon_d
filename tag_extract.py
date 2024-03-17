"""
extract_tag_chatgpt ：chatGPTを用いてタグ生成を行う関数
引数：("テキストかurlの文字列", [既存のタグのリスト])
戻り値：[生成したタグのリスト]
"""
"""
extract_tag ：Mecabを用いてタグ生成を行う関数
引数：("テキストかurlの文字列")
戻り値：[生成したタグのリスト]
"""
"""
generate_summary_chatgpt ：chatGPTを用いて要約生成を行う関数
引数：("テキストかurlの文字列")
戻り値："要約の文字列"
"""

import os
import sys
import re

# pip install mecab-python3
# pip install unidic-lite
import MeCab
mecab = MeCab.Tagger("mecabrc")

# pip install beautifulsoup4
import requests
from bs4 import BeautifulSoup

#pip install openai==0.28.1
import openai
# export OPENAI_API_KEY=[YOUR_API_KEY]
openai.api_key = os.getenv("OPENAI_API_KEY")

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

def extract_url(url):
  r = requests.get(url) 
  soup = BeautifulSoup(r.content, "html.parser")

  for script in soup(["script", "style"]):
      script.decompose()
  #print(soup)
  text=soup.get_text()
  #print(text)
  lines= [line.strip() for line in text.splitlines()]
  text="\n".join(line for line in lines if line)
  return text

def extract_tag(text_or_url):
  if "http" in text_or_url:
    input_text = extract_url(text_or_url)
  else:  
    input_text = text_or_url
  if len(input_text) > 5000: input_text = input_text[:5000]
  reccomend_tag_list = [pair[0] for pair in ma_parse(input_text)][:10]
  # print(reccomend_tag_list)
  return reccomend_tag_list

def extract_tag_chatgpt(text_or_url, tag_list=[]):
  if "http" in text_or_url:
    input_text = extract_url(text_or_url)
  else:  
    input_text = text_or_url
  if len(input_text) > 500: input_text = input_text[:500]

  conversation=[{"role": "system", "content": "あなたは優秀なアシスタントです。"}]

  user_input = "以下にある文章の冒頭を提示します。この文章をカテゴリー分けするためのタグを作成したいので、候補となる文字列を既存のタグの中から１０個教えてください。なお関連する既存のタグがない場合は新たに作成して教えて下さい。\n文章の冒頭「"+input_text+"」\n既存の文字列「"+"、".join(tag_list)+"」\nフォーマット：1. タグ"
  conversation.append({"role": "user", "content": user_input})

  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo", # The deployment name you chose when you deployed the GPT-35-turbo or GPT-4 model.
      messages=conversation,
      temperature=0.7,
      max_tokens=800,
      top_p=0.95,
      frequency_penalty=0,
      presence_penalty=0,
      n = 1,
      stop=None,
  )

  answer = response["choices"][0]["message"]["content"]
  conversation.append({"role": "assistant", "content": answer})
  answer = re.findall(r'\d*\. .*?\n', answer)
  reccomend_tag_list = [re.sub(r'\d*\. (.*?)', '\\1', i).replace("\n", "") for i in answer]
  # print(reccomend_tag_list)
  return reccomend_tag_list

def generate_summary_chatgpt(text_or_url):
  if "http" in text_or_url:
    input_text = extract_url(text_or_url)
  else:  
    input_text = text_or_url
  if len(input_text) > 500: input_text = input_text[:500]

  conversation=[{"role": "system", "content": "あなたは優秀なアシスタントです。"}]

  user_input = "以下にある文章の冒頭を提示します。この文章の要約文を100文字程度で作成して教えて下さい。\n文章の冒頭「"+input_text+"」\n"
  conversation.append({"role": "user", "content": user_input})

  response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo", # The deployment name you chose when you deployed the GPT-35-turbo or GPT-4 model.
      messages=conversation,
      temperature=0.7,
      max_tokens=800,
      top_p=0.95,
      frequency_penalty=0,
      presence_penalty=0,
      n = 1,
      stop=None,
  )

  answer = response["choices"][0]["message"]["content"]
  conversation.append({"role": "assistant", "content": answer})
  answer = re.sub(r'要約「(.*)」', "\\1", answer)
  answer = re.sub(r'要約：(.*)', "\\1", answer)
  # print(answer)
  return answer

if __name__ == '__main__':

  sentence = "ここに述べる理論は、今日一般に「相対性理論」と呼ばれている理論*3の、考えうる限り一般化したものである。以下ではこの新しい理論を「相対性理論」と呼び以前の「特殊相対性理論」とは区別するとともに、後者の知識を前提とする。相対性理論の一般化は、ミンコフスキーにより与えられた特殊相対論の形式によって、大いに容易となった。かの数学者は空間座標と時間座標の等価性を初めて見出し、私の理論に使いやすい形にしてくれた。一般相対論に必要な数学的道具は、ガウス、リーマン、クリストッフェルによる非ユークリッド的*4な多様体*5の研究に基づき、リッチ、レヴィ・チヴィタにより統合され、既に理論物理学の問題に利用されている、絶対微分幾何学の中で既に完成されている。この論文の理解のために数学書を勉強する必要が無いよう、私はチャプターB*6の中で、我々に必要だが、物理学者にとって当然の前提とはされない数学的道具を全て、できる限り簡単にそして見通しの良い形で構築した。最後にこの場を借りて私の友人であり数学者のグロスマンに感謝したい。彼のおかげで関連する数学書の勉強を省くことができたし、彼は私が重力場の方程式*7を見つけるのも助けてくれた。"
  url = "https://note.nkmk.me/python-re-match-search-findall-etc/"

  generate_summary_chatgpt(sentence)
  generate_summary_chatgpt(url)

  extract_tag_chatgpt(sentence, ["物理学", "数学", "正規表現"])
  extract_tag_chatgpt(url, ["物理学", "数学", "正規表現"])

  extract_tag(sentence)
  extract_tag(url)
