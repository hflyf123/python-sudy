from urllib import request
import re
# 断点调试


class Spider:
    '''
    this is Spider class
    '''
    # 网址
    url = 'https://www.panda.tv/cate/lol'
    # 正则表达式
    root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    name_pattern = '</i>([\s\S]*?)</span>'
    number_pattern = '<span class="video-number">([\s\S]*?)</span>'

    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        # bytes
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8')
        return htmls

# 1，唯一表示符做标签
# 2. 最接近数据的标签
# 3. 选择可以闭合的标签
# 逐渐精细化信息
    # 数据分析
    def __analysis(self, htmls):
        root_html = re.findall(Spider.root_pattern, htmls)
        achors = []
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            number = re.findall(Spider.number_pattern, html)
            achor = {'name': name, 'number': number}
            achors.append(achor)
        # print(achors[1])
        return achors
    # 数据精炼

    def __refine(self, anchors):
        def l(anchor): return {
            'name': anchor['name'][0].strip(),
            'number': anchor['number'][0]
        }
        return map(l, anchors)

    def __sort(self, anchors):
        # filter
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)
        return anchors

    def __sort_seed(self, anchor):
        r = re.findall('\d*', anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number

    def __show(self, anchors):
        for rank in range(0, len(anchors)):
            print('rank '+str(rank+1) + ':' +
                  anchors[rank]['name']+':' + anchors[rank]['number'])

    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)


spider = Spider()
spider.go()
