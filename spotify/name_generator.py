# MIT Student Profile Generator (Fictional Test Data)

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
        parts = []
        for part in pattern:
            if part == 'prefix':
                parts.append(random.choice(cls.ROOTS['prefixes']))
            elif part == 'middle':
                parts.append(random.choice(cls.ROOTS['middles']))
            elif part == 'suffix':
                parts.append(random.choice(cls.ROOTS['suffixes']))
            elif part == 'name_root':
                parts.append(random.choice(cls.ROOTS['name_roots']))
            elif part == 'ending':
                parts.append(random.choice(cls.ROOTS['name_endings']))
            elif part == 'compound':
                parts.append(random.choice(cls.ROOTS['prefixes']) + random.choice(cls.ROOTS['suffixes']))

        return ''.join(parts)

    @classmethod
    def generate(cls):
        first_pattern = random.choice(cls.PATTERNS['first_name'])
        last_pattern = random.choice(cls.PATTERNS['last_name'])

        first = cls._generate_component(first_pattern).capitalize()
        last = cls._generate_component(last_pattern).capitalize()

        return {
            "first_name": first,
            "last_name": last,
            "full_name": f"{first} {last}"
        }


# ---------------- MIT DATA ---------------- #

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
    "New House, 471 Memorial Dr, Cambridge, MA 02139",
    "Random Hall, 290 Massachusetts Ave, Cambridge, MA 02139"
]

MIT_CAMPUSES = [
    "Cambridge Main Campus",
    "Kendall Square Campus",
    "Sloan Business Campus",
    "CSAIL Research Campus"
]


def generate_mit_email(first_name, last_name):
    return f"{first_name.lower()}.{last_name.lower()}{random.randint(10,99)}@mit.edu"


def generate_student_id():
    return f"{random.randint(2021,2025)}{''.join(random.choices(string.digits, k=5))}"


def generate_birth_date():
    return f"{random.randint(1999,2005)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"


def generate_phone_number():
    return f"+1-{random.choice(['617','857','781'])}-{random.randint(200,999)}-{random.randint(1000,9999)}"


def generate_mit_student_profile():
    name = NameGenerator.generate()

    return {
        "university": "Massachusetts Institute of Technology",
        "campus": random.choice(MIT_CAMPUSES),
        "first_name": name["first_name"],
        "last_name": name["last_name"],
        "full_name": name["full_name"],
        "email": generate_mit_email(name["first_name"], name["last_name"]),
        "phone": generate_phone_number(),
        "student_id": generate_student_id(),
        "major": random.choice(MIT_MAJORS),
        "enrollment_year": random.randint(2021, 2025),
        "birth_date": generate_birth_date(),
        "dorm_address": random.choice(MIT_DORMS)
    }