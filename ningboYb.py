import re
import urllib
import urllib.parse
import urllib.request

import xmltodict


def get_html_content(url) -> str:
    # col=1&appid=1&webid=3520&path=%2F&columnid=1229214899&sourceContentType=1&unitid=6179039
    params = {'col': 1, 'appid': 1, 'webid': 3520, 'path': '/', 'columnid': 1229214899, 'sourceContentType': 1, 'unitid': 6179039}
    print("data:" + urllib.parse.urlencode(params))
    req = urllib.request.Request(url, data=urllib.parse.urlencode(params).encode('utf-8'))
    # req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36')
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')


def get_page_result(record_set):
    if len(record_set) == 0:
        print("格式不正确，退出...")
        exit(0)
    if len(record_set['record']) == 0:
        print("格式不正确，退出...")
        exit(0)
    records = record_set['record']
    results: dict = {}
    for record in records:
        # print(record)
        # print("\n")
        # example = '<tr>  <td class="biaoge" width="280px" height="30" align="left" bgcolor="#F6FAFE" >宁波市四季康来医药有限公司甬上民生上街店</td>  <td class="biaoge" width="300px" height="30" align="center" bgcolor="#F6FAFE" >浙江省宁波市北仑区大碶上街8号1幢（1)（2）</td>  <td class="biaoge" width="70px" height="30" align="left" bgcolor="#F6FAFE" >北仑区</td>  <td class="biaoge" width="100px" height="30" align="center" bgcolor="#F6FAFE" >600620</td>  </tr>'
        # regex the '<td class="biaoge" width="280px" height="30" align="left" bgcolor="#F6FAFE" >*</td>' in example
        pattern = re.compile(r'<td class="biaoge" width="280px" height="30" align="left" bgcolor="#F6FAFE" >(.*?)</td>')
        result_name = pattern.findall(record)
        if len(result_name) == 0:
            print("格式不正确，退出...")
            exit(0)
        # regex the '<td class="biaoge" width="300px" height="30" align="center" bgcolor="#F6FAFE" >*</td>' in record
        pattern = re.compile(r'<td class="biaoge" width="300px" height="30" align="center" bgcolor="#F6FAFE" >(.*?)</td>')
        result_addr = pattern.findall(record)
        if len(result_addr) == 0:
            print("格式不正确，退出...")
            exit(0)
        results[result_name[0]] = result_addr[0]
        print(result_name[0] + "," + result_addr[0])
    return results


pageId = 0
pageSize = 100

print("探测宁波医保报销定点零售记录总数...")
url = "http://ybj.ningbo.gov.cn/module/jpage/dataproxy.jsp?startrecord=0&endrecord=3&perpage=3"
html = get_html_content(url)
xml = xmltodict.parse(html)
print("医保报销定点零售记录总数:" + xml['datastore']['totalrecord'])
total_records = int(xml['datastore']['totalrecord'])

total_results: dict = {}

for i in range(1, 999):
    if (i - 1) * pageSize > total_records:
        print("no more records after " + str(i - 1) + " pages")
        break
    pageId = i
    url = "http://ybj.ningbo.gov.cn/module/jpage/dataproxy.jsp?startrecord=" + str((i - 1) * pageSize) + "&endrecord=" + str(i * pageSize) + "&perpage=" + str(
        pageSize)
    print(url)
    html = ""
    while html is None or html == "":
        try:
            html = get_html_content(url)
        except Exception as e:
            print(e)
            continue
    print("html content: " + str(html))
    if html is None:
        continue

    xml = xmltodict.parse(html)
    xml_content_of_recordset = xml['datastore']['recordset']
    results = get_page_result(xml_content_of_recordset)
    # for item in results
    for key in results:
        total_results[key] = results[key]

# writes dict to file
with open('ningboYb.txt', 'w', encoding='utf-8') as f:
    for key in total_results:
        while total_results[key].find(",") >= 0:
            total_results[key] = total_results[key].replace(",", "，")
        f.write(key + "," + total_results[key] + "\n")
print("done")
