# SheerID 验证配置文件

# SheerID API 配置
PROGRAM_ID = '67c8c14f5f17a83b745e2f82'
SHEERID_BASE_URL = 'https://services.sheerid.com'
MY_SHEERID_URL = 'https://my.sheerid.com'

# 文件大小限制
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB

# School Configuration - Harvard University Campuses

SCHOOLS = {
    '1001': {
        'id': 1001,
        'idExtended': '1001',
        'name': 'Harvard University - Main Campus',
        'city': 'Cambridge',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'HARVARD.EDU',
        'latitude': 42.377003,
        'longitude': -71.116660
    },
    '1002': {
        'id': 1002,
        'idExtended': '1002',
        'name': 'Harvard Business School',
        'city': 'Boston',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'HBS.EDU',
        'latitude': 42.365490,
        'longitude': -71.122260
    },
    '1003': {
        'id': 1003,
        'idExtended': '1003',
        'name': 'Harvard Medical School',
        'city': 'Boston',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'HMS.HARVARD.EDU',
        'latitude': 42.336590,
        'longitude': -71.102280
    },
    '1004': {
        'id': 1004,
        'idExtended': '1004',
        'name': 'Harvard Law School',
        'city': 'Cambridge',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'LAW.HARVARD.EDU',
        'latitude': 42.379620,
        'longitude': -71.118960
    },
    '1005': {
        'id': 1005,
        'idExtended': '1005',
        'name': 'Harvard Kennedy School',
        'city': 'Cambridge',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'HKS.HARVARD.EDU',
        'latitude': 42.371690,
        'longitude': -71.121060
    }
}

# 默认学校
DEFAULT_SCHOOL_ID = '2565'

