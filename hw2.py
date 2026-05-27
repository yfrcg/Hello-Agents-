import re
import random

# 定义规则库:模式(正则表达式) -> 响应模板列表
rules = {
    r'I need (.*)': [
        "Why do you need {0}?",
        "Would it really help you to get {0}?",
        "Are you sure you need {0}?"
    ],
    r'Why don\'t you (.*)\?': [
        "Do you really think I don't {0}?",
        "Perhaps eventually I will {0}.",
        "Do you really want me to {0}?"
    ],
    r'Why can\'t I (.*)\?': [
        "Do you think you should be able to {0}?",
        "If you could {0}, what would you do?",
        "I don't know -- why can't you {0}?"
    ],
    r'I am (.*)': [
        "Did you come to me because you are {0}?",
        "How long have you been {0}?",
        "How do you feel about being {0}?"
    ],
    r'.* mother .*': [
        "Tell me more about your mother.",
        "What was your relationship with your mother like?",
        "How do you feel about your mother?"
    ],
    r'.* father .*': [
        "Tell me more about your father.",
        "How did your father make you feel?",
        "What has your father taught you?"
    ],
    r'I work as (.*)': [
        "Do you enjoy working as {0}?",
        "How long have you been working as {0}?",
        "What do you like most about your job?"
    ],
    r'I study (.*)': [
        "What made you choose to study {0}?",
        "Do you find studying {0} rewarding?",
        "How do you feel about your studies?"
    ],
    r'I (like|love|enjoy) (.*)': [
        "Why do you {0} {1}?",
        "How does {1} make you feel?",
        "When did you start to {0} {1}?"
    ],
    r'I feel (.*)': [
        "Why do you feel {0}?",
        "How long have you felt {0}?",
        "What do you think is causing you to feel {0}?"
    ],
    r'.*': [
        "Please tell me more.",
        "Let's change focus a bit... Tell me about your family.",
        "Can you elaborate on that?"
    ]
}

# [新增] 上下文记忆：存储用户在对话中提到的关键信息
context_memory = {}

# [新增] 个人信息提取规则：匹配用户自我介绍的模式，用于存入记忆
info_patterns = {
    r'(?:my name is|i am|call me) (\w+)': 'name',
    r'i am (\d+) years? old': 'age',
    r'i work (?:as|at|for) (.+)': 'job',
}

# 定义代词转换规则
pronoun_swap = {
    "i": "you", "you": "i", "me": "you", "my": "your",
    "am": "are", "are": "am", "was": "were", "i'd": "you would",
    "i've": "you have", "i'll": "you will", "yours": "mine",
    "mine": "yours"
}

def swap_pronouns(phrase):
    """
    对输入短语中的代词进行第一/第二人称转换
    """
    words = phrase.lower().split()
    swapped_words = [pronoun_swap.get(word, word) for word in words]
    return " ".join(swapped_words)

def respond(user_input):
    """
    根据规则库生成响应，支持上下文记忆
    """
    # [新增] 第一步：尝试提取个人信息并存入记忆
    for pattern, key in info_patterns.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            context_memory[key] = match.group(1).strip()

    # 第二步：按规则库匹配生成响应
    for pattern, responses in rules.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            # 捕获匹配到的部分
            captured_group = match.group(1) if match.groups() else ''
            # 进行代词转换
            swapped_group = swap_pronouns(captured_group)
            # 从模板中随机选择一个并格式化
            response = random.choice(responses).format(swapped_group)

            # [新增] 第三步：如果记忆中有姓名，在回复前加上称呼
            if 'name' in context_memory:
                response = f"{context_memory['name']}, {response[0].lower() + response[1:]}"

            return response
    # 如果没有匹配任何特定规则，使用最后的通配符规则
    response = random.choice(rules[r'.*'])
    # [新增] 通配符回复也加上称呼
    if 'name' in context_memory:
        response = f"{context_memory['name']}, {response[0].lower() + response[1:]}"
    return response

# 主聊天循环
if __name__ == '__main__':
    print("Therapist: Hello! How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Therapist: Goodbye. It was nice talking to you.")
            break
        response = respond(user_input)
        print(f"Therapist: {response}")
        
