#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 0.0.2

import urllib.request, urllib.parse, urllib.error
import argparse, re, os, sys, copy
from bs4 import BeautifulSoup


def ptStrLiterally(str):
    for i in str:
        try:
            print(i, end='')
        except UnicodeEncodeError as e:
            pass
    print('')


def puts(str):
    try:
        print(str)
    except UnicodeEncodeError as e:
        # print(e.reason)
        ptStrLiterally(str)
    else:
        pass


def searchSubStr(str, pattern_start, pattern_end, quiet=False):
    try:
        start = re.search(pattern_start, str).end()
        end = re.search(pattern_end, str[start:]).start()
    except AttributeError as e:
        if not quiet:
            print('AttributeError: Can\'t find substring')
        return ''
    substr = str[start:end+start]
    return substr


def generateOpener(auth, ua):
    opener = urllib.request.build_opener()
    if ua:
        opener.addheaders = [('User-agent', ua)]
    else:
        opener.addheaders = [('User-agent', 'Mozilla 5.0')]
    if auth:
        opener.addheaders.append(('Cookie', 'chii_auth=' + auth))
    return opener


def getHtml(url, auth, ua):
    opener = generateOpener(auth, ua)
    try:
        html = opener.open(url).read()
    except urllib.error.URLError as e:
        print(url)
        print('No response...')
        return None
    else:
        return html


def getProgress(url, auth, ua):
    opener = generateOpener(auth, ua)
    try:
        html = opener.open(url).read()
        soup = BeautifulSoup(html.decode('utf-8'))
        p = soup.find('input', id='watchedeps')['value']
    except urllib.error.URLError as e:
        print(url)
        print('No response...')
        return ''
    except TypeError as e:
        print(url)
        print('TyepError: NoneType')
        print('Error: the given auth string doesn\'t match the user id')
        return ''
    else:
        return p



def getIDnGh(li):
    idngh = li.find('p', class_='collectModify').find_all('a')[1]['onclick']
    # [subid, gh]
    return idngh[20:-2].split(", '")


def removeItem(domain, subid, auth, ua, gh):
    opener = generateOpener(auth, ua)
    rmlink = ''.join([domain, '/subject/', subid, '/remove?gh=', gh])
    try:
        response = opener.open(rmlink)
    except urllib.error.URLError as e:
        print(rmlink)
        print('Cant erase subject %s' % subid)
        return False
    else:
        return True


def export(domain, auth, ua, uid, path, wipe):
    cats = ['anime', 'game', 'music', 'book', 'real']
    types = ['do', 'collect', 'wish', 'on_hold', 'dropped']
    # types = ['do', 'wish', 'on_hold', 'dropped']
    # types = ['do', 'on_hold', 'dropped']
    cats_c = {'anime' : '动画',
              'game' : '游戏',
              'music' : '音乐',
              'book' : '书籍',
              'real' : '电视剧'}
    types_c = {'do' : '在看',
               'collect' : '看过',
               'wish' : '想看',
               'on_hold' : '搁置',
               'dropped' : '抛弃'}
    cats_types = [(c, t) for c in cats for t in types]
    for cat, type in cats_types:
        # if cat == 'anime' and type == 'collect':
        #     continue
        # print(types_c[type], '的', cats_c[cat], '\n')
        puts(types_c[type] + '的' + cats_c[cat] + '\n')
        pg = 1
        idx = 1
        items = ''
        while pg != 0:
            url = ''.join( [domain, '/', cat, '/list/', uid, '/',
                            type, '?page=', str(pg)] )
            html = getHtml(url, auth, ua)
            if not html:
                break
            # # test
            # with open("test.html",'w', encoding='utf-8') as ft:
            #     ft.write(html.decode('utf-8'))
            # # test
            soup = BeautifulSoup(html.decode('utf-8'))
            ul = soup.find(id='browserItemList')
            content = ''
            for li in ul.children:
                inner = li.find('div', class_='inner')
                collect_info = inner.find('p', class_='collectInfo')
                comment = inner.find('div', id='comment_box')
                stars = inner.find('span', class_='starsinfo')
                greyname = inner.h3.small
                href = domain + inner.h3.a['href']
                iname = str(idx) + '. ' + inner.h3.a.text.strip() + '\n'
                iurl = '地址：' + href + '\n'
                icollect_info = collect_info.text.strip() + '\n'
                if greyname:
                    igreyname = '原名：' + greyname.text.strip() + '\n'
                else:
                    igreyname = ''
                if stars:
                    istars = '评分：' + stars['class'][0][6:] + '星\n'
                else:
                    istars = ''
                if comment:
                    icomment = ('简评：'
                             + inner.find('div',
                                          id='comment_box').text.strip()
                             + '\n')
                else:
                    icomment = ''
                if ( (cat == 'anime' or cat == 'real')
                     and type == 'do'
                     and auth ):
                    iprogress = '进度：' + getProgress(href, auth, ua) + '\n'
                else:
                    iprogress = ''
                # print(iname)
                puts(iname)
                content += (iname + igreyname + iurl + istars + icomment
                         + iprogress + icollect_info + '\n')
                idx += 1
                if wipe:
                    # remove item
                    try:
                        subid, gh = getIDnGh(li)
                        removeItem(domain, subid, auth, ua, gh)
                    except:
                        print('Error: wrong auth string\n')
            if content != '':
                items += content
                pg += 1
            else:
                pg = 0
        if items == '':
            continue
        file_name = path + '/bangumi_' + cat + '_' + type + '.txt'
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(items)


def getAuth(domain, auth, ua, authfile, uid, password):
    if auth and ua:
        return uid, auth, ua
    elif authfile:
        with open(authfile, 'r') as af:
            user_agent = af.readline()
            auth = af.readline()
        return uid, auth.strip(), user_agent.strip()
    elif not password:
        # print('Error: No auth string, no auth file, no password\n')
        return uid, auth, ua
    url = domain + '/login'
    # url = domain + '/FollowTheRabbit'
    data = {'cookietime': '2592000',
            'email': uid,
            'password': password,
            'loginsubmit': '登录'}
    user_agent = 'Mozilla/5.0 (Elephant 3) Midori 3.5'
    data = urllib.parse.urlencode(data).encode('utf-8')
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', user_agent)]
    urllib.request.install_opener(opener)
    res = urllib.request.urlopen(url, data)
    # print(res.getheaders())
    # print(res.getheader('Set-Cookie'))
    cookie = res.getheader('Set-Cookie')
    # -- use searchSubStr() --
    # start = re.search('chii_auth=', cookie).end()
    # end = re.search('(;|$)', cookie[start:]).start()
    # # print(cookie[start:end+start])
    # auth = cookie[start:end+start]
    # -- use searchSubStr() --
    auth = searchSubStr(cookie, 'chii_auth=', '(;|$)')
    return uid, auth, user_agent


def post(url, data, auth, ua):
    opener = generateOpener(auth, ua)
    post_data = urllib.parse.urlencode(data).encode('utf-8')
    urllib.request.install_opener(opener)
    res = urllib.request.urlopen(url, post_data)
    return res


def getGH(domain, auth, ua):
    opener = generateOpener(auth, ua)
    html = opener.open(domain).read().decode('utf-8')
    pattern = '<a href="http://(bangumi.tv|bgm.tv|chii.in)/logout/'
    # -- use searchSubStr() --
    # start = re.search(pattern, html).end()
    # end = re.search('"', html[start:]).start()
    # return html[start:end+start]
    # -- use searchSubStr() --
    return searchSubStr(html, pattern, '"')


def addItem(domain, subid, type, rating, tags,
            comment, watchedeps, gh, auth, ua):
    # print(domain, subid, type, rating, tags,
    #       comment, watchedeps, gh, auth, ua)
    # on == on_hold
    types_table = {
        'wish'    : 1,
        'collect' : 2,
        'do'      : 3,
        'on'      : 4,
        'dropped' : 5
    }
    item_action = ''.join( [domain, '/subject/', subid,
                            '/interest/update?gh=', gh] )
    item_data = {
        'referer'  : 'subject',
        'interest' : types_table[type],
        'rating'   : rating,
        'tags'     : tags,
        'comment'  : comment,
        'update'   : '保存'
    }
    item_res = post(item_action, item_data, auth, ua)
    if watchedeps:
        eps_action = ''.join( [domain, '/subject/set/watched/', subid] )
        eps_data = {
            'referer'    : 'subject',
            'subject'    : '更新',
            'watchedeps' : watchedeps
        }
        eps_res = post(eps_action, eps_data, auth, ua)
    return item_res


def restore(domain, auth, ua, path):
    basic_dict = {
        'title'      : '',
        'subid'      : '',
        'type'       : '',
        'rating'     : '',
        'tags'       : '',
        'comment'    : '',
        'watchedeps' : '',
    }
    m_dict = {
        '简评' : 'comment',
        '进度' : 'watchedeps',
    }
    part_a = '_(anime|game|music|book|real)'
    part_b = '_(do|collect|wish|on_hold|dropped)'
    files_name_pattern = 'bangumi' + part_a + part_b + '.txt$'
    files = filter(lambda x : re.match(files_name_pattern, x), os.listdir(path))
    gh = getGH(domain, auth, ua)
    for file in files:
        print(file, '\n')
        items_dict = {}
        counter = 0
        with open(path + file, 'r', encoding='utf-8') as f:
            items = f.readlines()
        for line in items:
            # print(line)
            line = line.strip()
            if re.match('\d+\. ', line):
                counter += 1
                items_dict[counter] = copy.deepcopy(basic_dict)
                items_dict[counter]['title'] = line
                type = file.split('.')[0].split('_')[2]
                items_dict[counter]['type'] = type
            elif re.match('\d{4}-\d{1,2}-\d{1,2}', line):
                tags = searchSubStr(line, '标签: ', '$', True)
                items_dict[counter]['tags'] = tags
            elif line.startswith('地址'):
                subid = searchSubStr(line, '\.(tv|in)/subject/', '$')
                # print('subid', subid)
                # print('counter', counter)
                items_dict[counter]['subid'] = subid
            elif line.startswith('评分'):
                items_dict[counter]['rating'] = line[3:-1]
            else:
                m = m_dict.get(line[:2])
                items_dict[counter][m] = line[3:]
        n = len( items_dict.keys() )
        for i in range(n, 0, -1):
            # print(items_dict[i]['subid'],
            #       items_dict[i]['type'],
            #       items_dict[i]['rating'],
            #       items_dict[i]['tags'],
            #       items_dict[i]['comment'],
            #       items_dict[i]['watchedeps'],
            #       gh,
            #       auth,
            #       ua)
            puts(items_dict[i]['title'] + '\n')
            addItem(domain,
                    items_dict[i]['subid'],
                    items_dict[i]['type'],
                    items_dict[i]['rating'],
                    items_dict[i]['tags'],
                    items_dict[i]['comment'],
                    items_dict[i]['watchedeps'],
                    gh,
                    auth,
                    ua)



def main():
    '''Main function'''
    # parse argv start
    parser = argparse.ArgumentParser(prog="tenkou.py")
    parser.add_argument("-d", "--domain",
                        default="bgm.tv",
                        choices=["chii.in", "bgm.tv", "bangumi.tv"],
                        help="choose domain, default is bgm.tv")
    parser.add_argument("-u", "--uid",
                        help="your id")
    parser.add_argument("--password",
                        help="give me your password")
    parser.add_argument("-p", "--path",
                        default="./",
                        help="change the directory "\
                             "where you save files")
    parser.add_argument("--auth",
                        help="your auth string")
    parser.add_argument("--useragent",
                        help="your user-agent")
    parser.add_argument("--authfile",
                        help="specify the location of "\
                             "your auth file")
    parser.add_argument("-r", "--restore",
                        action="store_true",
                        help="restore your data")
    parser.add_argument("--wipe",
                        action="store_true",
                        help="tenkou")
    parser.add_argument("-v", "--version",
                        action='version',
                        version='v0.0.2')
    args = parser.parse_args()
    # parse argv end
    if not os.path.isdir(args.path):
        print("Error: Local path doesn't exist")
        return
    if not args.uid:
        print('Error: Please tell me your id')
        return
    path = args.path + "/"
    domain = 'http://' + args.domain
    wipe = args.wipe
    # print(wipe==True)
    uid, auth, ua = getAuth(domain,
                            args.auth,
                            args.useragent,
                            args.authfile,
                            args.uid,
                            args.password)
    if not args.restore:
        export(domain, auth, ua, uid, path, wipe)
    else:
        restore(domain, auth, ua, path)
    print("Complete")

main()
