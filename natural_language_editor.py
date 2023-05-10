import spacy

POS = {'ADJ': 'прилагательное',
       'ADP': 'адлог',
       'ADV': 'наречие',
       'AUX': 'вспомогательный глагол',
       'CONJ': 'союз',
       'CCONJ': 'сочиниельный союз',
       'INTJ': 'междометие',
       'NOUN': 'существительное',
       'NUM': 'числительное',
       'PART': 'частица',
       'PRON': 'местоимение',
       'PROPN': 'имя собственное',
       'PUNCT': 'знак препинания',
       'SCONJ': 'подчинительный союз',
       'SYM': 'символ',
       'VERB': 'глагол',
       'X': 'не определено',
       'SPACE': 'пробел',
       'DET': 'детерминатив'
       }

DEP = {'ROOT': 'корень дерева зависимостей',
        'dobj': 'прямое дополнение',
        'popj': 'объект предлога',
        'subjpass': 'подлежащее страдательного залога',
        'relcl': 'относительное предложение',
        'acomp': 'определение существительного',
        'agent': 'агенс',
        'amod': 'определение прилагательного',
        'attr': 'предикатив',
        'auxpass': 'вспомогательный глагол "быть" в качестве залога "страдательный"',
        'cop': 'глагол "быть" в роли связки',
        'dep': 'некатегоризированная зависимость',
        'expl': 'эмфатическое вводное слово',
        'INTJ': 'междометие',
        'meta': 'мета-описание',
        'neg': 'отрицание',
        'nmod': 'определение существительного, наречие, числительного',
        'nounmod': 'существительное в роли определения',
        'npadvmod': 'наречие в роли определения',
        'nummod': 'числительное как определение',
        'obj': 'прямое дополнение',
        'obl': 'обстановочное дополнение',
        'para': 'пара',
        'pcomp': 'инфинитивная клауза',
        'pobj': 'препозиционное прямое дополнение',
        'poss': 'притяжательное местоимение',
        'preconj': 'предварительный союз',
        'predet': 'предопределяющий артикль',
        'prep': 'предлог',
        'prt': 'частица',
        'punct': 'знаки препинания',
        'quantmod': 'кванторное определение',
        "acl": 'клауза, модифицированная относительной или относительной фразой',
        "advcl": 'клауза, модифицированная наречием',
        "advmod": 'модификатор наречия',
        "appos": 'клауза, определяемая или объясняемая именной фразой',
        "aux": 'вспомогательный глагол',
        "case": 'падежный модификатор',
        "cc": 'союз сочинения',
        "ccomp": 'главный глагол в клаузе с зависимыми компонентами',
        "compound": 'составное словосочетание',
        "conj": 'соединительный союз',
        "csubj": 'клауза с подлежащим, зависимым от другой клаузы',
        "det": 'определитель',
        "fixed": 'соединение слов в составном слове',
        "flat": 'сокращение слов или объединение коротких слов в составное слово',
        "goeswith": 'общая ошибка в идентификации словосочетаний',
        "iobj": 'косвенный объект',
        "list": 'элемент списка',
        "mark": 'маркер условия или связующий элемент',
        "nsubj": 'подлежащее',
        "orphan": 'оставшаяся словоформа, не связанная с остальной устройчивой конструкцией',
        "parataxis": 'конструкция типа "мыслительные прерывания", где конструкции разделены запятыми',
        "reparandum": 'слово, исправляемое или заменяемое',
        "root": 'корневой элемент',
        "vocative": 'вызов, обращение к кому-то',
        "xcomp": 'незавершенный глагол или предикативное выражение внутри главной клаузы'}


def parser(text):
    nlp = spacy.load("ru_core_news_sm")
    doc = nlp(text)
    words = {}
    for token in doc:
        lemma = token.lemma_.lower()
        if token.pos_ in POS:
            token_pos = POS[token.pos_]
        else:
            token_pos = token.pos_
        if token.dep_ in DEP:
            token_dep = DEP[token.dep_]
        else:
            token_dep = token.dep_
        tags = token_pos + '; ' + token_dep
        form = token.text.lower()
        if lemma not in words:
            words.update({lemma: {'count': 1, 'form': {form: {'count': 1, 'tags': tags}}}})
        else:
            if form not in words[lemma]['form']:
                words[lemma]['form'].update({form: {'count': 1, 'tags': tags}})
            else:
                words[lemma]['form'][form]['count'] += 1
            values = words.get(lemma)
            values['count'] += 1
    return sorted(words.items())


def correct_dict(word_form, info, dictionary):
    print(dictionary)
    new_dictionary = dict(dictionary)
    nlp = spacy.load("ru_core_news_sm")
    word = nlp(word_form)
    word_lemma = word[0].lemma_.lower()
    if word_lemma in new_dictionary:
        if word_form in new_dictionary[word_lemma]['form']:
            new_dictionary[word_lemma]['form'][word_form]['tags'] = info
        else:
            new_dictionary[word_lemma]['form'].update({word_form: {'count': 1, 'tags': info}})
            new_dictionary[word_lemma]['count'] += 1
    else:
        new_dictionary.update({word_lemma: {'count': 1, 'form': {word_form: {'count': 1, 'tags': info}}}})

    return sorted(new_dictionary.items())
