#!/usr/local/bin/python3
def shend_icmp_packet(ip_address,times):
    try:
        response = os.popen('ping -c ' + str(times) + ' '+ ip_address).read()
        print(response)
        # 取出丢包率
        lost = response[response.rindex(',',0,response.index("%"))+1:response.index("%")].strip()
        #取出指定的延时字符串
        res = list(response)
        index = 0
        count = 0
        for r in res:
            count += 1
            if r == "=" :
                index = count
        response = response[index + 1:-4]

        # 取出执行的延迟
        i = 0
        j = []
        res1 = list(response)
        for r in res1:
            i += 1
            if r == "/" :
                j.append(i)

        min = response[:j[0]-1]
        avg = response[j[0]:j[1]-1]
        max = response[j[1]:j[2]-1]
        return min,avg,max,lost
    except Exception as e:
        print("ping exec error",e)
