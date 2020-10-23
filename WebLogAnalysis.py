import re,sys,xlwt,requests
weblog_dir=sys.argv[1]
weblog = open(weblog_dir)
reobj=re.compile(r'(?P<ip>.*?) - - \[(?P<time>.*?)\] "(?P<request>.*?)" (?P<status>.*?) (?P<bytes>.*?) "(?P<referer>.*?)" "(?P<ua>.*?)"')
workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet("LessSafe安全团队web日志分析")
worksheet.write(0, 0, "城市")
worksheet.write(0, 1, "ip地址")  # 写入行，列，内容
worksheet.write(0, 2, "时间")
worksheet.write(0, 3, "请求体")
worksheet.write(0, 4, "相应状态")
worksheet.write(0, 5, "字节")
worksheet.write(0, 6, "来源")
worksheet.write(0, 7, "客户端")
def search(search_key,search_value):
    row=0
    for line in weblog:
        re_result=reobj.match(line)
        re_arry=re_result.groupdict()
        ip_add=requests.get("http://whois.pconline.com.cn/ipJson.jsp?ip="+re_arry['ip'])
        re_ipadd = re.findall(r'"addr":"(.*?)","regionNames"', ip_add.text)
        if search_key == 'request':
            if search_value in re_arry['request']:
                row=row+1
                write_xls(re_ipadd,re_arry['ip'],re_arry['time'],re_arry['request'],re_arry['status'],re_arry['bytes'],re_arry['referer'],re_arry['ua'],row)
        else:
            if re_arry[search_key]==search_value:
                row = row + 1
                write_xls(re_ipadd,re_arry['ip'],re_arry['time'],re_arry['request'],re_arry['status'],re_arry['bytes'],re_arry['referer'],re_arry['ua'],row)
    workbook.save("lesssafe.xls")
def write_xls(re_ipadd,ip,time,request,status,bytes,referer,ua,row):
    worksheet.write(row, 0, re_ipadd)
    worksheet.write(row, 1, ip)  # 写入行，列，内容
    worksheet.write(row, 2, time)
    worksheet.write(row, 3, request)
    worksheet.write(row, 4, status)
    worksheet.write(row, 5, bytes)
    worksheet.write(row, 6, referer)
    worksheet.write(row, 7, ua)

if __name__ == '__main__':
    print("————LessSafe安全团队web日志分析工具————")
    print("———————请选择你输入需要搜索的选项———————")
    print("——————————————ip———————————————————")
    print("—————————————request————————————————")
    print("——————————————status————————————————")
    print("————————————————UA——————————————————")
    search_key=input("请输入选项：")
    search_value=input("请输入要搜索的内容：")
    search(search_key,search_value)
    print("已分析完成")