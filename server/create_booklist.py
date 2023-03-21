import json

# 定义书籍列表的JSON变量
data = [
 {"book_name":"Boom and Bust"},
 {"book_name":"Central Banking 101"},
 {"book_name":"枢纽-施展"}
]

# 将JSON数据序列化为文本文件
with open('books-list.json', 'w') as f:
    json.dump(data, f)

# 从文本文件中读取JSON数据并反序列化
with open('books-list.json', 'r') as f:
    data = json.load(f)

# 打印反序列化后的JSON数据
print(data)
