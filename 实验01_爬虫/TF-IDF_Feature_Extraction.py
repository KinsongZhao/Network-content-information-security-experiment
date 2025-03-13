import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import sys
import io
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 设置标准输出编码为utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 从文件读取文本数据
def read_documents(file_path):
    documents = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:  # 忽略空行
                    try:
                        # 解析JSON格式的行
                        data = json.loads(line)
                        # 获取字典中的第一个值
                        text = list(data.values())[0]
                        documents.append(text)
                    except json.JSONDecodeError:
                        # 如果不是JSON格式，直接添加文本
                        documents.append(line)
    except Exception as e:
        print(f"读取文件出错：{str(e)}")
        return []
    return documents

# 分词
def chinese_tokenizer(text):
    words = jieba.cut(text)
    return [word for word in words if word not in stop_words]

if __name__ == '__main__':
    # 读取文档 - 使用正斜杠或原始字符串
    documents = read_documents(r"D:\03_教育\00_本科_海南师范大学\05_大三下_2025.3-2025.6\课程\网络信息内容安全\AI--\数据爬取\爬虫\sentence.txt")
    
    if not documents:
        print("未能读取到任何文本")
        sys.exit(1)
    
    print(f"成功读取 {len(documents)} 条文本")
    
    # 停用词列表
    stop_words = set([
        # 基础虚词
        "的", "是", "了", "在", "和", "与", "为", "以", "于", "之",
        "而", "所", "由", "其", "或", "亦", "即", "便", "又", "将", "并",
        "才", "已", "把", "但", "去", "来", "到", "从", "向", "让", "得",
        "不必", "何必", "何须", "不如", "好似", "不能", "能", "会", "可以",
        "仍然", "已经", "不要", "要", "被", "给", "把", "让", "使", "令",
        
        # 代词和指示词
        "这", "那", "你", "我", "他", "它", "她", "谁", "什么", "哪",
        "这里", "那里", "这个", "那个", "这样", "那样", "如此", "如何",
        "自己", "别人", "他人", "对方", "其他", "某某", "此处", "何处",
        "哪里", "这些", "那些", "其中", "本身", "自身", "本人",
        
        # 数量词和程度词
        "一个", "一些", "一样", "一般", "一直", "一切", "一下", "一声",
        "个", "些", "多", "少", "来", "去", "几", "每", "各", "某",
        "一层", "一片", "一轮", "很", "更", "最", "太", "越", "再",
        "一旦", "一生", "万万", "许多", "一点", "半点", "甚至", "都",
        
        # 时间词
        "年", "月", "日", "时", "分", "秒", "今", "古", "昔", "早", "晚",
        "朝", "暮", "旦", "夕", "昼", "夜", "当今", "此时", "此刻",
        "已经", "曾经", "将来", "过去", "现在", "后来", "从前", "一向",
        "暮春", "三月", "一夜", "片刻", "瞬间", "永远", "短暂", "刹那",
        
        # 情态词和语气词
        "可惜", "不过", "只是", "就是", "难道", "竟然", "居然", "确实",
        "必须", "应该", "可能", "大概", "也许", "差不多", "恐怕", "似乎",
        
        # 连词和关联词
        "因为", "所以", "如果", "虽然", "但是", "然而", "不过", "况且",
        "不仅", "而且", "以及", "并且", "或者", "还是", "就是", "正是",
        "不但", "何况", "否则", "此外", "另外", "然后", "接着", "随后",
        
        # 其他常用词
        "不会", "没有", "可以", "那么", "这么", "如何", "怎么", "怎样",
        "为何", "何以", "何必", "何须", "多少", "几时", "哪些", "谁人",
        "不能", "无法", "不可", "未必", "一定", "肯定", "确定", "必定"
    ])

    
    

    
   
    
    # 修改分词函数位置和实现
    def chinese_tokenizer(text):
        # 使用精确模式分词
        words = jieba.cut(text, cut_all=False)
        # 过滤停用词和空白字符
        return [word.strip() for word in words 
                if word.strip() and word.strip() not in stop_words 
                and len(word.strip()) > 1]  # 过滤单字词
    
    # 创建 TF-IDF 向量化器
    tfidf_vectorizer = TfidfVectorizer(tokenizer=chinese_tokenizer)

    # 计算 TF-IDF
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    # 获取特征名
    try:
        features = tfidf_vectorizer.get_feature_names_out()
    except AttributeError:
        features = tfidf_vectorizer.get_feature_names()

    # 创建数据框，查看结果
    df = pd.DataFrame(tfidf_matrix.toarray(), columns=features)

    print("TF-IDF 特征：")
    print(df)

    # 提取关键词
    top_keywords = {}
    for i, doc in enumerate(documents):
        tfidf_scores = tfidf_matrix[i, :].toarray().flatten()
        top_keywords[i] = sorted(zip(features, tfidf_scores), key=lambda x: -x[1])[:5]
        print(f"文档 {i+1} 的关键词：", [keyword[0] for keyword in top_keywords[i]])

    # 生成词云
    # 将所有文档合并成一个字符串
    text = ' '.join([' '.join(chinese_tokenizer(doc)) for doc in documents])
    
    # 创建词云对象
    wordcloud = WordCloud(
        font_path='C:/Windows/Fonts/simhei.ttf',  # 设置中文字体
        width=800,
        height=400,
        background_color='white'
    )
    
    # 生成词云
    wordcloud.generate(text)
    
    # 显示词云图
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    
    # 保存词云图
    plt.savefig('d:/wordcloud.png', dpi=300, bbox_inches='tight')
    print("词云图已保存至 d:/wordcloud.png")
    
    # 显示图像
    plt.show()
