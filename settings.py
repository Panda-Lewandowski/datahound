import logging

TOKEN = ""
GOOGLE_TOKEN = ""
BASE_URL = "https://api.vk.com/method/execute."
MEMBERS_FIELDS = "sex"  # bdate, city, country, online, online_mobile, education, last_seen, relation
PLATFORM = {1: "Mobile", 2: 'iPhone', 3: "iPad", 4: "Android",
            5: "Windows Phone", 6: "Windows 10", 7: "Web", 8: 'Unknown'}

SEX_COLORS = ['#FFD7E9', '#6495ED', '#B22222']
PLATFORM_COLORS = ['#66CDAA', '#EE5C42', '#B22222', '#1874CD']
SYSTEM_COLORS = ['#8B8386', '#FFE4C4']
LOG_LEVEL = logging.INFO


COUNTRIES = {1: 'Россия',
             2: 'Украина',
             3: 'Беларусь',
             4: 'Казахстан',
             5: 'Азербайджан',
             6: 'Армения',
             7: 'Грузия',
             8: 'Израиль',
             9: 'США',
             10: 'Канада'}


#logger = logging.getLogger('datahound')
logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s',
                    level=LOG_LEVEL, filename='datahound.log')
