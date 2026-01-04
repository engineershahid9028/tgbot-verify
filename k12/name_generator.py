"""
随机名字生成器（SheerID 安全版）
"""

import random


class NameGenerator:
    """
    英文名字生成器（只使用真实、常见名字）
    """

    FIRST_NAMES = [
        "John", "Michael", "David", "James", "Robert",
        "William", "Daniel", "Matthew", "Joseph", "Andrew",
        "Thomas", "Christopher", "Anthony", "Mark", "Steven"
    ]

    LAST_NAMES = [
        "Smith", "Johnson", "Brown", "Williams", "Jones",
        "Miller", "Davis", "Garcia", "Rodriguez", "Wilson",
        "Martinez", "Anderson", "Taylor", "Thomas", "Moore"
    ]

    @classmethod
    def generate(cls):
        """
        生成安全的英文名字（SheerID 友好）

        Returns:
            dict: first_name, last_name, full_name
        """
        first_name = random.choice(cls.FIRST_NAMES)
        last_name = random.choice(cls.LAST_NAMES)

        return {
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}"
        }


def generate_email(first_name: str = None, last_name: str = None):
    """
    生成安全邮箱（避免 SheerID invalidEmail）

    Returns:
        str: 邮箱地址
    """

    # 如果未提供名字，则生成
    if not first_name or not last_name:
        name = NameGenerator.generate()
        first_name = name["first_name"]
        last_name = name["last_name"]

    domains = [
        "gmail.com",
        "outlook.com",
        "yahoo.com",
        "icloud.com"
    ]

    domain = random.choice(domains)

    # 简单、真实的邮箱格式（无随机数字）
    return f"{first_name.lower()}.{last_name.lower()}@{domain}"


def generate_birth_date():
    """
    生成合理的教师生日（1970–1990）

    Returns:
        str: YYYY-MM-DD
    """
    year = random.randint(1970, 1990)
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    return f"{year}-{month}-{day}"
