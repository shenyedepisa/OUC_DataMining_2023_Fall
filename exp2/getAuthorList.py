import ijson
import json

minNum = 100
secondNum = 20
theme = ['computer vision']
themeName = 'CV'


def brief():
    name_id = {}
    new_list = []
    with open('dblp_v14.json', 'r') as f:
        objects = ijson.items(f, 'item')  # 使用ijson.items()函数逐项读取数据
        for obj in objects:
            flag1, flag2, flag3, flag4 = 0, False, False, 0
            try:
                l1 = [element.lower() for element in obj['keywords']]  # 在关键词中查找主题词
                flag1 = len(set(l1) & set(theme))
            except KeyError:
                pass
            try:
                flag2 = theme[0] in obj['title'].lower()  # 在论文标题中查找主题词
            except KeyError:
                pass
            try:
                flag3 = theme[0] in obj['venue']['raw'].lower()  # 在期刊标题中查找主题词
            except KeyError:
                pass
            try:
                l4 = [obj['fos'][i]['name'] for i in range(len(obj['fos']))]  # 在期刊内容关键字中查找主题词
                l4 = [element.lower() for element in l4]
                flag4 = len(set(l4) & set(theme))
            except KeyError:
                pass
            if flag2 or flag3 or flag1 >= 1 or flag4 >= 1:
                authors = obj['authors']
                temp = []
                for author in authors:
                    temp.append({'id': author['id'], 'name': author['name']})
                    name_id[author['id']] = author['name']
                new_list.append({'year': obj['year'], 'authors': temp})

    with open(f'briefAuthorList_{themeName}.json', 'w', encoding='utf-8') as f:
        json.dump(new_list, f, ensure_ascii=False)


def countAuthor():
    num_id = {}
    i = 0
    with open(f'briefAuthorList_{themeName}.json', 'r', encoding='utf-8') as f:
        objects = ijson.items(f, 'item')
        for obj in objects:
            i += 1
            if len(obj['authors']) > 1 and 2013 <= obj['year'] <= 2022:
                authors = obj['authors']
                for author in authors:
                    if author['id'] != "":
                        try:
                            num_id[author['id']] += 1
                        except KeyError:
                            num_id[author['id']] = 1

    print(f'Number of {themeName} papers:\t{i}')
    print(f'{themeName} papers select by year:\t{len(num_id)}')
    with open(f'frequency_{themeName}.json', 'w', encoding='utf-8') as f:
        json.dump(num_id, f, ensure_ascii=False)


def getAuthor():
    new_list = []
    secondSet, author_set = set(), set()
    with open(f'frequency_{themeName}.json', 'r', encoding='utf-8') as f:
        fre = json.load(f)
        for key in fre.keys():
            if fre[key] >= secondNum:
                secondSet.add(key)
                if fre[key] >= minNum:
                    author_set.add(key)

    print(f'Author with over {minNum} papers:\t{len(author_set)}')
    print(f'Author with over {secondNum} papers:\t{len(secondSet)}')

    with open(f'briefAuthorList_{themeName}.json', 'r', encoding='utf-8') as f:
        objects = ijson.items(f, 'item')
        for obj in objects:
            if len(obj['authors']) > 1 and 2013 <= obj['year'] <= 2022:
                authors = set(obj['authors'][i]['id'] for i in range(len(obj['authors'])))
                if not author_set.isdisjoint(authors):
                    if len(secondSet & authors) >= 2:
                        new_list.append(obj)

    with open(f'{themeName}_namelist2013-2022_{minNum}_{secondNum}.json', 'w', encoding='utf-8') as f:
        json.dump(new_list, f, ensure_ascii=False)

    print(f'selective papers:\t{len(new_list)}')


if __name__ == "__main__":
    brief()
    countAuthor()
    getAuthor()
