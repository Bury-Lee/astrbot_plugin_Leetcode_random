
import os
import json
import requests
import random
import re
from html import unescape



def update(URL = "https://leetcode.cn/api/problems/all/",OUTPUT_FILE = "leetcode_cn_full.json"):
    """更新力扣题库数据至本地 JSON 文件"""
    response = requests.get(URL, timeout=15)
    response.raise_for_status()
    data = response.json()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # print(f"已完整保存至：{OUTPUT_FILE}")
    return data



def 随机Leetcode题目(level="all"):
    """
    随机推荐一个力扣 (LeetCode) 免费题目，并返回格式化字符串
    参数:
        level: 难度级别 (1=简单, 2=中等, 3=困难, "all"=不限)
    返回:
        str: 格式化后的题目信息字符串（仅含题目描述和约束），或错误信息
    """
    data_file = "D:/QQ机器人/工作区域/AstrBot-4.11.4/data/plugins/自用插件"
    os.makedirs(os.path.join(data_file, "Leetcode"), exist_ok=True)

    levels = {1: "简单", 2: "中等", 3: "困难"}

    # === 步骤1：读取题库 ===
    try:
        with open(os.path.join(data_file, "leetcode_cn_full.json"), "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return f"找不到文件 {os.path.join(data_file, 'leetcode_cn_full.json')}，请确认路径正确且已导出题库数据。"
    except json.JSONDecodeError as e:
        return f"JSON 解析失败：{e}"

    problems = data.get('stat_status_pairs', [])
    if not problems:
        return "无法获取题目列表"

    free_problems = [
        p for p in problems
        if not p.get('paid_only') and not p.get('stat', {}).get('question__hide')
    ]

    if not free_problems:
        return "没有找到符合条件的免费题目"

    # === 随机选题 ===
    selected = None
    attempts = 0
    max_attempts = 1000
    while attempts < max_attempts:
        candidate = random.choice(free_problems)
        diff_level = candidate['difficulty']['level']
        if level == "all" or diff_level == level:
            selected = candidate
            break
        attempts += 1

    stat = selected['stat']
    frontend_id = stat['frontend_question_id']
    title = stat['question__title']
    slug = stat['question__title_slug']
    difficulty = levels.get(selected['difficulty']['level'], "未知")
    url = f"https://leetcode.cn/problems/{slug}/"

    # === 步骤2：请求网页 ===
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html_content = response.text

        file_path = os.path.join(data_file, "Leetcode", f"{slug}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
    except requests.exceptions.RequestException as e:
        return f"请求失败: {e}"

    def parse_leetcode_html(html):
        # 提取页面标题
        title_match = re.search(r'<title data-next-head="">(.*?) - 力扣', html)
        title_parsed = title_match.group(1) if title_match else "未知题目"

        # 提取 description meta 标签内容
        desc_match = re.search(r'<meta name="description" content="([^"]+)"', html)
        if not desc_match:
            return {"error": "无法找到题目描述"}

        raw_desc = desc_match.group(1)
        full_desc = unescape(raw_desc).strip()

        # 截断从“示例”开始的部分（包括“示例 1”、“示例：”等）
        # 使用非贪婪匹配，找到第一个“示例”相关关键词就停止
        truncated_desc = re.split(r'\s*示例\s*\d*[:：]?', full_desc, maxsplit=1)[0].strip()

        # 尝试从截断后的描述中提取“提示”部分（即约束）
        constraints_match = re.search(r'提示[：:]\s*(.+)', truncated_desc, re.DOTALL | re.IGNORECASE)
        if constraints_match:
            constraints = constraints_match.group(1).strip()
            # 从描述中移除“提示”部分，只保留纯题目描述
            description_only = truncated_desc[:constraints_match.start()].strip()
        else:
            constraints = "无明确约束。"
            description_only = truncated_desc

        return {
            "title": title_parsed,
            "description": description_only,
            "constraints": constraints
        }

    result = parse_leetcode_html(html_content)
    if "error" in result:
        return f"{result['error']}"

    # === 步骤4：拼接返回字符串（仅题目描述 + 约束）===
    output = []

    output.append("=" * 5)
    output.append(f"📌 编号: {frontend_id}")
    output.append(f"📘 题目: {title}")
    output.append(f"⭐ 难度: {difficulty}")
    output.append(f"🔗 链接: {url}")
    output.append("=" * 5)

    output.append("📝 题目描述:")
    output.append(result["description"])

    return "\n".join(output)




def 完整随机Leetcode题目(level="all"):
    """
    随机推荐一个力扣 (LeetCode) 免费题目，并返回格式化字符串
    参数:
        level: 难度级别 (1=简单, 2=中等, 3=困难, "all"=不限)
    返回:
        str: 格式化后的题目信息字符串（含题目描述、约束、输入输出示例），或错误信息
    """
    data_file = "D:/QQ机器人/工作区域/AstrBot-4.11.4/data/plugins/自用插件"
    os.makedirs(os.path.join(data_file, "Leetcode"), exist_ok=True)

    levels = {1: "简单", 2: "中等", 3: "困难"}

    # === 步骤1：读取题库 ===
    try:
        with open(os.path.join(data_file, "leetcode_cn_full.json"), "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return f"找不到文件 {os.path.join(data_file, 'leetcode_cn_full.json')}，请确认路径正确且已导出题库数据。"
    except json.JSONDecodeError as e:
        return f"JSON 解析失败：{e}"

    problems = data.get('stat_status_pairs', [])
    if not problems:
        return "无法获取题目列表"

    free_problems = [
        p for p in problems
        if not p.get('paid_only') and not p.get('stat', {}).get('question__hide')
    ]

    if not free_problems:
        return "没有找到符合条件的免费题目"

    # === 随机选题 ===
    selected = None
    attempts = 0
    max_attempts = 1000
    while attempts < max_attempts:
        candidate = random.choice(free_problems)
        diff_level = candidate['difficulty']['level']
        if level == "all" or diff_level == level:
            selected = candidate
            break
        attempts += 1

    if selected is None:
        return "在指定难度下未找到合适题目，请尝试其他难度。"

    stat = selected['stat']
    frontend_id = stat['frontend_question_id']
    title = stat['question__title']
    slug = stat['question__title_slug']
    difficulty = levels.get(selected['difficulty']['level'], "未知")
    url = f"https://leetcode.cn/problems/{slug}/"

    # === 步骤2：请求网页 ===
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html_content = response.text

        file_path = os.path.join(data_file, "Leetcode", f"{slug}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
    except requests.exceptions.RequestException as e:
        return f"请求失败: {e}"

    def parse_leetcode_html(html):
        # 提取页面标题
        title_match = re.search(r'<title data-next-head="">(.*?) - 力扣', html)
        title_parsed = title_match.group(1) if title_match else "未知题目"

        # 提取 description meta 标签内容（包含完整描述+示例+提示）
        desc_match = re.search(r'<meta name="description" content="([^"]+)"', html)
        if not desc_match:
            return {"error": "无法找到题目描述"}

        raw_desc = desc_match.group(1)
        full_desc = unescape(raw_desc).strip()

        # 分离出“示例”之前的部分（纯题目描述 + 提示）
        desc_and_constraints = re.split(r'\s*示例\s*\d*[:：]?', full_desc, maxsplit=1)[0].strip()

        # 提取约束（提示）
        constraints_match = re.search(r'提示[：:]\s*(.+)', desc_and_constraints, re.DOTALL | re.IGNORECASE)
        if constraints_match:
            constraints = constraints_match.group(1).strip()
            description_only = desc_and_constraints[:constraints_match.start()].strip()
        else:
            constraints = "无明确约束。"
            description_only = desc_and_constraints

        # 提取所有示例（最多前两个）
        examples = []
        example_blocks = re.findall(r'示例\s*\d+\s*[:：]?\s*(输入[：:]?.*?)(?=示例\s*\d+|提示|$)', full_desc, re.DOTALL | re.IGNORECASE)
        for block in example_blocks[:2]:  # 最多取两个
            block = block.strip()
            # 清理多余空行和空白
            lines = [line.strip() for line in block.split('\n') if line.strip()]
            if lines:
                examples.append('\n'.join(lines))

        return {
            "title": title_parsed,
            "description": description_only,
            "constraints": constraints,
            "examples": examples
        }

    result = parse_leetcode_html(html_content)
    if "error" in result:
        return f"{result['error']}"

    # === 步骤3：拼接返回字符串 ===
    output = []

    output.append("=" * 5)
    output.append(f"📌 编号: {frontend_id}")
    output.append(f"📘 题目: {title}")
    output.append(f"⭐ 难度: {difficulty}")
    output.append(f"🔗 链接: {url}")
    output.append("=" * 5)

    output.append("📝 题目描述:")
    output.append(result["description"])

    if result["constraints"] != "无明确约束。":
        output.append("\n❗ 约束条件:")
        output.append(result["constraints"])

    if result["examples"]:
        output.append("\n🧪 输入输出示例:")
        for i, ex in enumerate(result["examples"], 1):
            output.append(f"\n示例 {i}:")
            output.append(ex)

    return "\n".join(output)
