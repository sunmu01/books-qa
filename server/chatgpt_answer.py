from utils import get_embedding
from flask import jsonify
from config import *
from flask import current_app
import logging
import openai
import re, time

TOP_K = 5

logger = logging.getLogger(__name__)

# 判断question是中文还是英文
def is_chinese_question(text):
    chinese_pattern = re.compile('[\u4e00-\u9fa5]')
    english_pattern = re.compile('[a-zA-Z]')

    chinese_count = len(re.findall(chinese_pattern, text))
    english_count = len(re.findall(english_pattern, text))

    if chinese_count >= english_count:
        return True
    else:
        return False

def get_chatgpt_answer(summary_level, book_name, question, previous_question, previous_answer, pinecone_index):
    
    logger.info(f"Getting chatgpt answer for question: {question}")
    search_query_embedding = get_embedding(question, EMBEDDINGS_MODEL)
    
    is_chinese = is_chinese_question(question)

    try:
        if book_name == "":
            query_response = pinecone_index.query(
                namespace=summary_level,
                top_k=TOP_K,
                include_values=False,
                include_metadata=True,
                vector=search_query_embedding,
            )
        else:
            query_response = pinecone_index.query(
                namespace=summary_level,
                top_k=TOP_K,
                include_values=False,
                include_metadata=True,
                vector=search_query_embedding,
                filter={
                    "book_name": {"$in": [book_name]}
                }
            )

        logger.info(
            f"[get_chatgpt_answer] received query response from Pinecone: {query_response}")
        
        files_string = ""
        for i in range(len(query_response.matches)):
            result = query_response.matches[i]
            score = result.score
            filename = result.metadata["book_name"]
            file_text = result.metadata["chunk_text"]
            #clean_file_text = file_text.replace("\n", "; ").replace("  ", " ")

            if is_chinese:
                file_string = f"###\n[书籍名称]: {filename}\n[内容文本]: {file_text}\n"
            else:
                file_string = f"###\n[Book]: {filename}\n[Content]: {file_text}\n"

            if score < COSINE_SIM_THRESHOLD and i > 0:
                logger.info(
                    f"[get_chatgpt_answer] score {score} is below threshold {COSINE_SIM_THRESHOLD} and i is {i}, breaking")
                break
            files_string += file_string
        
        # 准备prompt
        system_prompt = ""
        user_prompt = ""
        if is_chinese:
            system_prompt = f"你是一个很有用的智能助手，可以根据下面提供的书籍中[内容文本]来回答用户提出的问题。\n\n" \
                f"如果你不能回答，只需输出“我在书籍内容中找不到和你问题相关的答案。”\n\n" \
                f"如果答案不包含在下面提供的书籍[内容文本]中，回答“我找不到和你问题相关的答案。” 如果问题不是问题，回答“这不是一个有效的问题。”\n\n" \
                f"在你可以找到答案的情况下，首先给出答案,然后解释你是如何从[书籍名称]或[内容文本]中找到答案的。" \
                f"请使用以下格式给出问题的答案：\n\n" \
                f"[问题]: <question>\n\n###\n[书籍名称]:\n书籍名称1\n[内容文本]:内容文本1###\n[书籍名称]:\n书籍名称2\n[内容文本]:内容文本2\n\n..."
            user_prompt = f"[问题]：{question}\n\n{files_string}\n[答案]："
        else:
            system_prompt = f"You are a helpful assistant. Given you a question, please try to answer it using the content of the book extracts below, " \
                f"and if you cannot answer, or find a relevant file, just output \"I couldn't find the answer to that question in the books.\".\n\n" \
                f"If the answer is not contained in the books or if there are no book extracts, respond with \"I couldn't find the answer " \
                f"to that question in the books.\" If the question is not actually a question, respond with \"That's not a valid question.\"\n\n" \
                f"In the cases where you can find the answer, first give the answer. Then explain how you found the answer from the source or sources, " \
                f"and use the exact names of the source books you mention. Do not make up the names of any other books other than those mentioned "\
                f"in the books context. Give the answer in the following format:\n\n" \
                f"[Question]: <question>\n\n###\n[Book]: book name 1 \n[Content]: book text 1 \n###\n[Book]: book name 2 \n[Content]: book text 2\n\n..."\
                f"[Answer]: <answer> or \"I couldn't find the answer to that question in the books\" or \"That's not a valid question.\">\n\n"
            
            user_prompt = f"[Question]: {question}\n\n" \
                f"{files_string}\n" \
                f"[Answer]:"

        #logger.info(f"[get_chatgpt_answer] system prompt: {system_prompt}")
        logger.info(f"[get_chatgpt_answer] user prompt: \n {user_prompt}")

        # 调用chatgpt
        start_time = time.time()
        if previous_question == "" or previous_answer == "":
            response = openai.ChatCompletion.create(
                model=GENERATIVE_MODEL,
                messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                ],
                temperature=0,
                )
        else:
            response = openai.ChatCompletion.create(
                model=GENERATIVE_MODEL,
                messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": previous_question},
                        {"role": "assistant", "content": previous_answer},
                        {"role": "user", "content": user_prompt},
                ],
                temperature=0,
                )
        logger.info(f"[get_chatgpt_answer] chatgpt response time: {time.time() - start_time}")
        #查看一下token的使用情况
        logger.info(f"[get_chatgpt_answer] response usage is: \n {response['usage']}")

        answer = response['choices'][0]['message']['content'].strip()
        logger.info(f"[get_chatgpt_answer] answer: {answer}")

        return jsonify({"answer": answer, "reference": files_string})

    except Exception as e:
        logger.info(f"[get_chatgpt_answer] error: {e}")
        return str(e)

