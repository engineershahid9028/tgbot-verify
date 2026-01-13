# SheerID 验证配置文件

# SheerID API 配置
PROGRAM_ID = '67c8c14f5f17a83b745e2f82'
SHEERID_BASE_URL = 'https://services.sheerid.com'
MY_SHEERID_URL = 'https://my.sheerid.com'

# 文件大小限制
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB

# School Configuration - Harvard University (using original IDs)

SCHOOLS = {
    '2565': {
        'id': 2565,
        'idExtended': '2565',
        'name': 'Harvard University - Main Campus',
        'city': 'Cambridge',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'HARVARD.EDU',
        'latitude': 42.377003,
        'longitude': -71.116660
    },
    '651379': {
        'id': 651379,
        'idExtended': '651379',
        'name': 'Harvard University - Online Division',
        'city': 'Cambridge',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'ONLINE.HARVARD.EDU',
        'latitude': 42.373611,
        'longitude': -71.109733
    },
    '8387': {
        'id': 8387,
        'idExtended': '8387',
        'name': 'Harvard Business School',
        'city': 'Boston',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'HBS.EDU',
        'latitude': 42.365490,
        'longitude': -71.122260
    },
    '8382': {
        'id': 8382,
        'idExtended': '8382',
        'name': 'Harvard Law School',
        'city': 'Cambridge',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'LAW.HARVARD.EDU',
        'latitude': 42.379620,
        'longitude': -71.118960
    },
    '8396': {
        'id': 8396,
        'idExtended': '8396',
        'name': 'Harvard Medical School',
        'city': 'Boston',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'HMS.HARVARD.EDU',
        'latitude': 42.336590,
        'longitude': -71.102280
    },
    '8379': {
        'id': 8379,
        'idExtended': '8379',
        'name': 'Harvard Kennedy School',
        'city': 'Cambridge',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'HKS.HARVARD.EDU',
        'latitude': 42.371690,
        'longitude': -71.121060
    },
    '2560': {
        'id': 2560,
        'idExtended': '2560',
        'name': 'Harvard School of Engineering',
        'city': 'Cambridge',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'SEAS.HARVARD.EDU',
        'latitude': 42.378110,
        'longitude': -71.117480
    },
    '650600': {
        'id': 650600,
        'idExtended': '650600',
        'name': 'Harvard Extension School',
        'city': 'Cambridge',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'EXTENSION.HARVARD.EDU',
        'latitude': 42.374420,
        'longitude': -71.118960
    },
    '8388': {
        'id': 8388,
        'idExtended': '8388',
        'name': 'Harvard Graduate School of Education',
        'city': 'Cambridge',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'GSE.HARVARD.EDU',
        'latitude': 42.372850,
        'longitude': -71.120350
    },
    '8394': {
        'id': 8394,
        'idExtended': '8394',
        'name': 'Harvard School of Public Health',
        'city': 'Boston',
        'state': 'MA',
        'country': 'US',
        'type': 'UNIVERSITY',
        'domain': 'HSPH.HARVARD.EDU',
        'latitude': 42.335400,
        'longitude': -71.102900
    }
}

# 默认学校
DEFAULT_SCHOOL_ID = '2565'

