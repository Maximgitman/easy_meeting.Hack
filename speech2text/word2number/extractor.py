from natasha.extractors import Extractor
from yargy.parser import Match



from yargy import rule, or_
from yargy.pipelines import morph_pipeline, caseless_pipeline
from yargy.interpretation import fact, const
from yargy.predicates import eq, caseless, normalized, type

Number = fact('Number', ['int', 'multiplier'])
NUMS_RAW = {
    'ноль': 0,
    'нуль': 0,
    'один': 1, 
    'два': 2, 
    'три': 3, 
    'четыре': 4, 
    'пять': 5,
    'шесть': 6,
    'семь': 7,
    'восемь': 8,
    'девять': 9,
    'десять': 10,
    'одиннадцать': 11,
    'двенадцать': 12,
    'тринадцать': 13,
    'четырнадцать': 14,
    'пятнадцать': 15,
    'шестнадцать': 16,
    'семнадцать': 17,
    'восемнадцать': 18,
    'девятнадцать': 19,
    'двадцать': 20,
    'тридцать': 30,
    'сорок': 40,
    'пятьдесят': 50,
    'шестьдесят': 60,
    'семьдесят': 70,
    'восемьдесят': 80,
    'девяносто': 90,
    'сто': 100,
    'двести': 200,
    'триста': 300,
    'четыреста': 400,
    'пятьсот': 500,
    'шестьсот': 600,
    'семьсот': 700,
    'восемьсот': 800,
    'девятьсот': 900,
    'тысяча': 10**3,
    'миллион': 10**6,
    'миллиард': 10**9,
    'триллион': 10**12,
}
DOT = eq('.')
INT = type('INT')
THOUSANDTH = rule(caseless_pipeline(['тысячных', 'тысячная'])).interpretation(const(10**-3))
HUNDREDTH = rule(caseless_pipeline(['сотых', 'сотая'])).interpretation(const(10**-2))
TENTH = rule(caseless_pipeline(['десятых', 'десятая'])).interpretation(const(10**-1))
THOUSAND = or_(
    rule(caseless('т'), DOT),
    rule(caseless('тыс'), DOT.optional()),
    rule(normalized('тысяча')),
    rule(normalized('тыща'))
).interpretation(const(10**3))
MILLION = or_(
    rule(caseless('млн'), DOT.optional()),
    rule(normalized('миллион'))
).interpretation(const(10**6))
MILLIARD = or_(
    rule(caseless('млрд'), DOT.optional()),
    rule(normalized('миллиард'))
).interpretation(const(10**9))
TRILLION = or_(
    rule(caseless('трлн'), DOT.optional()),
    rule(normalized('триллион'))
).interpretation(const(10**12))
MULTIPLIER = or_(
    THOUSANDTH,
    HUNDREDTH,
    TENTH,
    THOUSAND,
    MILLION,
    MILLIARD,
    TRILLION
).interpretation(Number.multiplier)
NUM_RAW = rule(morph_pipeline(NUMS_RAW).interpretation(Number.int.normalized().custom(NUMS_RAW.get)))
NUM_INT = rule(INT).interpretation(Number.int.custom(int))
NUM = or_(
    NUM_RAW,
    NUM_INT
).interpretation(Number.int)
NUMBER = or_(
    rule(NUM, MULTIPLIER.optional())
).interpretation(Number)


class NumberExtractor(Extractor):
    def __init__(self):
        super(NumberExtractor, self).__init__(NUMBER)

    def replace(self, text):
        """
        Замена чисел в тексте без их группировки

        Аргументы:
            text: исходный текст

        Результат:
            new_text: текст с замененными числами
        """
        if text:
            new_text = ""
            start = 0

            for match in self.parser.findall(text):
                if match.fact.multiplier:
                    num = match.fact.int * match.fact.multiplier
                else:
                    num = match.fact.int
                new_text += text[start: match.span.start] + str(num)
                start = match.span.stop
            new_text += text[start:]

            if start == 0:
                return text
            else:
                return new_text
        else:
            return None
    
    def replace_groups(self, text):
        """
        Замена сгруппированных составных чисел в тексте

        Аргументы:
            text: исходный текст

        Результат:
            new_text: текст с замененными числами
        """
        if text:
            start = 0
            matches = list(self.parser.findall(text))
            groups = []
            group_matches = []

            for i, match in enumerate(matches):
                if i == 0:
                    start = match.span.start
                if i == len(matches) - 1:
                    next_match = match
                else:
                    next_match = matches[i + 1]
                group_matches.append(match.fact)
                if text[match.span.stop: next_match.span.start].strip() or next_match == match:
                    groups.append((group_matches, start, match.span.stop))
                    group_matches = []
                    start = next_match.span.start
            
            new_text = ""
            start = 0

            for group in groups:
                num = 0
                nums = []
                new_text += text[start: group[1]]
                for match in group[0]:
                    curr_num = match.int * match.multiplier if match.multiplier else match.int
                    if match.multiplier:
                        num = (num + match.int) * match.multiplier
                        nums.append(num)
                        num = 0
                    elif num > curr_num or num == 0:
                        num += curr_num
                    else:
                        nums.append(num)
                        num = 0
                if num > 0:
                    nums.append(num)
                new_text += str(sum(nums))
                start = group[2]
            new_text += text[start:]

            if start == 0:
                return text
            else:
                return new_text
        else:
            return None
            