"""随机名字生成器"""
import random


import random
import string


class NameGenerator:
    """English Name Generator"""

    ROOTS = {
        'prefixes': ['Al', 'Bri', 'Car', 'Dan', 'El', 'Fer', 'Gar', 'Har', 'Jes', 'Kar',
                     'Lar', 'Mar', 'Nor', 'Par', 'Quin', 'Ros', 'Sar', 'Tar', 'Val', 'Wil'],
        'middles': ['an', 'en', 'in', 'on', 'ar', 'er', 'or', 'ur', 'al', 'el',
                    'il', 'ol', 'am', 'em', 'im', 'om', 'ay', 'ey', 'oy', 'ian'],
        'suffixes': ['ton', 'son', 'man', 'ley', 'field', 'ford', 'wood', 'stone', 'worth',
                     'berg', 'stein', 'bach', 'heim', 'gard', 'land', 'wick', 'shire',
                     'dale', 'brook', 'ridge'],
        'name_roots': ['Alex', 'Bern', 'Crist', 'Dav', 'Edw', 'Fred', 'Greg', 'Henr',
                       'Ivan', 'John', 'Ken', 'Leon', 'Mich', 'Nick', 'Oliv', 'Paul',
                       'Rich', 'Step', 'Thom', 'Will'],
        'name_endings': ['a', 'e', 'i', 'o', 'y', 'ie', 'ey', 'an', 'en', 'in',
                         'on', 'er', 'ar', 'or', 'el', 'al', 'iel', 'ael', 'ine', 'lyn']
    }

    PATTERNS = {
        'first_name': [
            ['prefix', 'ending'],
            ['name_root', 'ending'],
            ['prefix', 'middle', 'ending'],
            ['name_root', 'middle', 'ending']
        ],
        'last_name': [
            ['prefix', 'suffix'],
            ['name_root', 'suffix'],
            ['prefix', 'middle', 'suffix'],
            ['compound']
        ]
    }

    @classmethod
    def _generate_component(cls, pattern):
        components = []
        for part in pattern:
            if part == 'prefix':
                component = random.choice(cls.ROOTS['prefixes'])
            elif part == 'middle':
                component = random.choice(cls.ROOTS['middles'])
            elif part == 'suffix':
                component = random.choice(cls.ROOTS['suffixes'])
            elif part == 'name_root':
                component = random.choice(cls.ROOTS['name_roots'])
            elif part == 'ending':
                component = random.choice(cls.ROOTS['name_endings'])
            elif part == 'compound':
                part1 = random.choice(cls.ROOTS['prefixes'])
                part2 = random.choice(cls.ROOTS['suffixes'])
                component = part1 + part2
            else:
                component = ''

            components.append(component)

        return ''.join(components)

    @classmethod
    def _format_name(cls, name):
        return name.capitalize()

    @classmethod
    def generate(cls):
        first_name_pattern = random.choice(cls.PATTERNS['first_name'])
        last_name_pattern = random.choice(cls.PATTERNS['last_name'])

        first_name = cls._generate_component(first_name_pattern)
        last_name = cls._generate_component(last_name_pattern)

        return {
            'first_name': cls._format_name(first_name),
            'last_name': cls._format_name(last_name),
            'full_name': f"{cls._format_name(first_name)} {cls._format_name(last_name)}"
        }


# ---------------- MIT PROFILE DATA ---------------- #

MIT_MAJORS = [
    "Computer Science",
    "Artificial Intelligence",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Robotics",
    "Data Science",
    "Physics",
    "Aerospace Engineering",
    "Cybersecurity",
    "Biotechnology"
]

MIT_DORMS = [
    "Baker House, 362 Memorial Dr, Cambridge, MA 02139",
    "McCormick Hall, 320 Memorial Dr, Cambridge, MA 02139",
    "Maseeh Hall, 305 Memorial Dr, Cambridge, MA 02139",
    "Simmons Hall, 229 Vassar St, Cambridge, MA 02139",
    "Next House, 500 Memorial Dr, Cambridge, MA 02139",
    "New House, 471–476 Memorial Dr, Cambridge, MA 02139",
    "Random Hall, 290 Massachusetts Ave, Cambridge, MA 02139"
]

MIT_CAMPUSES = [
    "Cambridge Main Campus",
    "Kendall Square Campus",
    "Sloan Business Campus",
    "CSAIL Research Campus"
]


def generate_mit_email(first_name, last_name):
    """Generate MIT student email"""
    username = f"{first_name.lower()}.{last_name.lower()}"
    number = random.randint(10, 99)
    return f"{username}{number}@mit.edu"


def generate_student_id():
    """Generate MIT-style student ID"""
    year = random.randint(2021, 2025)
    rand = ''.join(random.choices(string.digits, k=5))
    return f"{year}{rand}"


def generate_birth_date():
    """Generate random birth date (1999–2005)"""
    year = random.randint(1999, 2005)
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    return f"{year}-{month}-{day}"


def generate_phone_number():
    """Generate US-style phone number"""
    area = random.choice(["617", "857", "781"])
    middle = random.randint(200, 999)
    last = random.randint(1000, 9999)
    return f"+1-{area}-{middle}-{last}"


def generate_mit_student_profile():
    """Generate full MIT student profile (fictional)"""

    name = NameGenerator.generate()
    major = random.choice(MIT_MAJORS)
    enrollment_year = random.randint(2021, 2025)

    profile = {
        "university": "Massachusetts Institute of Technology",
        "campus": random.choice(MIT_CAMPUSES),
        "first_name": name["first_name"],
        "last_name": name["last_name"],
        "full_name": name["full_name"],
        "email": generate_mit_email(name["first_name"], name["last_name"]),
        "phone": generate_phone_number(),
        "student_id": generate_student_id(),
        "major": major,
        "enrollment_year": enrollment_year,
        "birth_date": generate_birth_date(),
        "dorm_address": random.choice(MIT_DORMS)
    }

    return profile


# Example usage
if __name__ == "__main__":
    for _ in range(3):
        print(generate_mit_student_profile())
