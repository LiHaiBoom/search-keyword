import os
import fitz
import re  # 精确匹配

# 统计关键词
def count_keywords_in_pdfs(folder_path, keywords):

    if not os.path.isdir(folder_path):
        print(f"找不到文件夹 '{folder_path}' 或它不是一个有效的文件夹。")
        return None
    lower_keywords = [kw.lower() for kw in keywords if kw]
    keyword_counts = {kw: 0 for kw in lower_keywords}

    processed_files = 0  # 成功处理的文件数量
    failed_files = []  # 处理失败的文件名

    print(f"开始处理文件夹 '{folder_path}' 中的 PDF 文件...")
    print(f"要查找的关键词 (忽略大小写): {', '.join(lower_keywords)}")

    # 遍历指定文件夹中的所有文件和子文件夹名
    for filename in os.listdir(folder_path):
        # 检查文件名是否以 ".pdf" 结尾
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            print(f"\n正在处理文件: {filename}") # 打印换行符让输出更清晰
            try:
                with fitz.open(file_path) as doc:
                    full_text = ""  # 初始化一个空字符串，存储整个 PDF 的文本内容
                    for page_num, page in enumerate(doc):
                        full_text += page.get_text("text")

                    # 将提取到的整个 PDF 文本转换为小写，以便进行不区分大小写的关键词匹配
                    full_text_lower = full_text.lower()

                    # 开始在当前 PDF 的文本中计数关键词
                    print("  计字数中...")
                    # 遍历我们之前准备好的小写关键词列表
                    for keyword in lower_keywords:
                        # 使用字符串的 count() 方法计算当前关键词在小写文本中出现的次数
                        # 注意：这是子字符串匹配，如 'art' 会匹配 'start', 'article' 等

                        # 匹配完整单词
                        pattern = r'\b' + re.escape(keyword) + r'\b' 
                        count = len(re.findall(pattern, full_text_lower)) # 查找所有匹配项并计算数量

                        # 如果找到了这个关键词
                        if count > 0:
                            print(f"    找到 '{keyword}' {count} 次") # 打印找到的次数
                            # 将当前文件中的计数值累加到总计数字典中
                            keyword_counts[keyword] += count

                processed_files += 1  # 成功处理完一个文件，计数器加 1

            except Exception as e:
                print(f"  **错误**：处理文件 '{filename}' 时发生错误: {e}")
                failed_files.append(filename)

    print("\n--- 处理完成 ---")
    print(f"共处理 {processed_files} 个 PDF 文件。")
    if failed_files:
        print(f"以下文件处理失败: {', '.join(failed_files)}")

    return keyword_counts


if __name__ == "__main__":
    while True:
        pdf_folder = input("请输入包含 PDF 论文的文件夹路径：")
        if os.path.isdir(pdf_folder):
            break # 如果路径有效，跳出循环
        else:
            print("输入的路径无效或不存在，请重新输入。")

    # 获取用户输入的关键词
    keywords_input = input("输入要查找的关键词, 用英文逗号分隔：")

    keywords_list = [kw.strip() for kw in keywords_input.split(',') if kw.strip()]

    if not keywords_list:
        print("错误：未输入有效关键词。")
    else:
        results = count_keywords_in_pdfs(pdf_folder, keywords_list)

        if results is not None:
            print("\n--- 统计结果 ---")
            if not any(results.values()):
                 print("没找到关键词。")
            else:
                for keyword_lower, count in results.items():
                    original_keyword = next((k for k in keywords_list if k.lower() == keyword_lower), keyword_lower)
                    print(f"关键词 '{original_keyword}' 总共出现: {count} 次")
