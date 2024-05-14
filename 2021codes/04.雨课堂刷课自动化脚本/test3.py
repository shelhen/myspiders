from difflib import SequenceMatcher


a = '所谓“科学”，它包括自然科学、社会科学和人文科学等，它们属于（）范畴。'
b = 'We may choose tables or graphs when presenting numerical data.()'

# 引用ratio方法，返回序列相似性的度量
rate = SequenceMatcher(None, a, b).ratio()

print(rate)