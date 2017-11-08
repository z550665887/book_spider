import traceback
import re
import os
chs_arabic_map = {u'零':0, u'一':1, u'二':2, u'三':3, u'四':4,
        u'五':5, u'六':6, u'七':7, u'八':8, u'九':9,
        u'十':10, u'百':100, u'千':10 ** 3, u'万':10 ** 4,
        u'〇':0, u'壹':1, u'贰':2, u'叁':3, u'肆':4,
        u'伍':5, u'陆':6, u'柒':7, u'捌':8, u'玖':9,
        u'拾':10, u'佰':100, u'仟':10 ** 3, u'萬':10 ** 4,
        u'亿':10 ** 8, u'億':10 ** 8, u'幺': 1,
        u'０':0, u'１':1, u'２':2, u'３':3, u'４':4,
        u'５':5, u'６':6, u'７':7, u'８':8, u'９':9}

def change_to_GBK(url_title):
    if isinstance(url_title,list):
        for x in range(len(url_title)):
            url_title[x]= url_title[x].encode('latin-1').decode('GBK')
        return url_title
    elif isinstance(url_title,str):
        url_title= url_title.encode('latin-1').decode('GBK')
        return url_title

def sort_title(url_title,url_date):
    num = 0
    print(len(url_title))
    for x in range(len(url_title)):
        y = re.search(r'第(\w{1,7})章',str(url_title[x]))

        if y:
            num += 1
            url_title[x] = num
            # url_title[x] = convertChineseDigitsToArabic(re.search(r'第(\w{1,7})章',url_title[x]).group()[1:][:-1])
        else:
            url_date[x] = -1
            url_title[x] = -1
    return(url_title)

def merge_txt(path,name):
    try:
        for x in range(1,99999):
            if os.path.exists("{0}/{1}/{2}.txt".format(path,name,x)):
                with open("{0}/{1}/{2}.txt".format(path,name,x),'r',encoding='utf-8') as e ,open("{0}/{1}/{2}.txt".format(path,name,name),'a',encoding='utf-8') as f:
                    for line in e.readlines():
                        f.write(line+'\n')
            else:
                break
        return "success"
    except:
        traceback.print_exc()

def convertChineseDigitsToArabic (chinese_digits, encoding="utf-8"):
    try:
        chinese_digits = int(chinese_digits)
        return chinese_digits
    except:
        if isinstance (chinese_digits, str):
            chinese_digits = chinese_digits

        result  = 0
        tmp     = 0
        hnd_mln = 0
        for count in range(len(chinese_digits)):
            curr_char  = chinese_digits[count]
            curr_digit = chs_arabic_map.get(curr_char, None)
            # meet 「亿」 or 「億」
            if curr_digit == 10 ** 8:
                result  = result + tmp
                result  = result * curr_digit
                # get result before 「亿」 and store it into hnd_mln
                # reset `result`
                hnd_mln = hnd_mln * 10 ** 8 + result
                result  = 0
                tmp     = 0
            # meet 「万」 or 「萬」
            elif curr_digit == 10 ** 4:
                result = result + tmp
                result = result * curr_digit
                tmp    = 0
            # meet 「十」, 「百」, 「千」 or their traditional version
            elif curr_digit >= 10:
                tmp    = 1 if tmp == 0 else tmp
                result = result + curr_digit * tmp
                tmp    = 0
            # meet single digit
            elif curr_digit is not None:
                tmp = tmp * 10 + curr_digit
            else:
                return result
        result = result + tmp
        result = result + hnd_mln
        return result


# print (convertChineseDigitsToArabic("一百零一"))