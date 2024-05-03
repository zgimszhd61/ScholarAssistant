# !pip install PyPDF2
# !pip install openai
from PyPDF2 import PdfReader
import os
from openai import OpenAI
import requests
postwordsLab = "\n----\n使用40字以内的中文通顺地重写上面文字内容."

def main(url):
  response = requests.get(url)
  with open('temp.pdf', 'wb') as f:
      f.write(response.content)
  pdf_path = 'temp.pdf'
  reader = PdfReader(pdf_path)

  number_of_pages = len(reader.pages)
  # print(number_of_pages)  # 打印页数

  # 提取第一页的文字
  page = reader.pages[0]
  text = page.extract_text()
  try:
    text = text.replace("\n"," ").replace("- ","").lower().strip().replace(" —","").replace("^ ","").replace("\n ","")
    text = text.split("abstract")[1].split("introduction")[0].split(". 1")[0]
  # .split("abstract")[1].split("introduction")[0].split("ntroduction")[0].split()
    # print(text)  # 提取出第一页的文字
    realtimeQuestion(text)
  except:
    print("ERROR")

os.environ["OPENAI_API_KEY"] = "sk-"

def realtimeQuestion(question):
    client = OpenAI()
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    temperature=0,
    messages=[
            {
                "role": "system",
                "content": (
                    "你是一位精通简体中文的专业翻译，尤其擅长将专业学术论文翻译成浅显易懂的科普文章。请你帮我将以下英文段落翻译成中文，风格与中文科普读物相似。"
                    "规则："
                    "- 翻译时要准确传达原文的事实和背景。"
                    "- 即使上意译也要保留原始段落格式，以及保留术语，例如 FLAC，JPEG 等。保留公司缩写，例如 Microsoft, Amazon, OpenAI 等。"
                    "- 人名不翻译"
                    "- 同时不要保留引用的论文，例如 [20] 这样的引用。"
                    "- 对于 Figure 和 Table，翻译的同时保留原有格式，例如：“Figure 1: ”翻译为“图 1: ”，“Table 1: ”翻译为：“表 1: ”。"
                    "- 全角括号换成半角括号，并在左括号前面加半角空格，右括号后面加半角空格。"
                    "- 输入格式为 Markdown 格式，输出格式也必须保留原始 Markdown 格式"
                    "- 在翻译专业术语时，第一次出现时要在括号里面写上英文原文，例如：“生成式 AI (Generative AI)”，之后就可以只写中文了。"
                    "- 以下是常见的 AI 相关术语词汇对应表（English -> 中文）："
                    "  * Transformer -> Transformer"
                    "  * Token -> Token"
                    "  * LLM/Large Language Model -> 大语言模型"
                    "  * Zero-shot -> 零样本"
                    "  * Few-shot -> 少样本"
                    "  * AI Agent -> AI 智能体"
                    "  * AGI -> 通用人工智能"
                ),
            },
            {"role": "user", "content": question},
        ],
    )
    print(response.choices[0].message.content.replace("。","。\n\n"))
    return(response.choices[0].message.content.replace("。","。\n\n"))


lines = [
"https://arxiv.org/pdf/2404.08511.pdf",
"https://arxiv.org/pdf/2404.08634.pdf",
"https://arxiv.org/pdf/2404.08555.pdf",
"https://arxiv.org/pdf/2404.08517.pdf"
          ]

for item in lines:
  query = item
  main(query+postwordsLab)
  print("原文地址："+query)

# with open('文件路径', 'r') as f:
  # lines = f.readlines()
  # for line in lines:
    # print(line, end='')

# line = "https://arxiv.org/pdf/2403.05318.pdf"
# # query = line.replace("/abs/","/pdf/").strip()+".pdf"
# query = line
# main(query+postwordsLab)
# print("原文地址："+query)
