import json

# 定义书籍列表的JSON变量
data = [
 {"book_name":"Finite and Infinite Games - A Vision of Life as Play and Possibility 1986"},
 {"book_name":"有限与无限的游戏 - 一个哲学家眼中的竞技世界 1986"},
 {"book_name":"Flow - The Psychology of Optimal Experience 1990"},
 {"book_name":"心流 - 最优体验心理学 2017"},
 {"book_name":"The Art of Impossible - A Peak Performance Primer 2020"},
 {"book_name":"跨越不可能 - 如何完成高且有难度的目标 2021"},
 {"book_name":"Tiny Habits - The Small Changes That Change Everything 2020"},
 {"book_name":"福格行为模型 -  2021"},
 {"book_name":"The Almanack of Naval Ravikant - A Guide to Wealth and Happiness 2020"},
 {"book_name":"纳瓦尔宝典 - 财富与幸福指南 2022"},
 {"book_name":"Empire of Cotton - A Global History 2014"},
 {"book_name":"枢纽 - 3000年的中国 2018"},
 {"book_name":"可能性的艺术 - 比较政治学30讲 2022"},
 {"book_name":"The Sovereign Individual - Mastering the Transition to the Information Age 2020"},
 {"book_name":"Boom and Bust - A Global History of Financial Bubbles 2020"},
 {"book_name":"Central Banking 101 - 2020"},
 {"book_name":"Layered Money - From Gold and Dollars to Bitcoin and Central Bank Digital Currencies 2021"},
 {"book_name":"货币金字塔 - 从黄金 美元到比特币和央行数字货币 2021"},
 {"book_name":"Thinking in Systems - A Primer 2008"},
 {"book_name":"系统之美 - 决策者的系统思考 2013"},
 {"book_name":"Complexity Theory - An Overview 2016"},
 {"book_name":"Complex Adaptive Systems - An Overview 2016"},
 {"book_name":"Network Theory - An Overview 2016"},
 {"book_name":"Nonlinear Systems - An Overview 2016"}
 ]

# 将JSON数据序列化为文本文件
with open('books-list.json', 'w') as f:
    json.dump(data, f)

# 从文本文件中读取JSON数据并反序列化
with open('books-list.json', 'r') as f:
    data = json.load(f)

# 打印反序列化后的JSON数据
print(data)
