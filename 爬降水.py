# @Author  : Jacob-ZHANG
import requests
import time
headers={'Cookie': 'PHPSESSID=rgrm5la754bmt220larii1o5faifhkik; token=1596764374','User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36'}
for i in range(160):
    number=i+1
    print(number)
    url='https://cmdp.ncc-cma.net//160/160.php?station_id='+str(number)+'&type=prec&fromYear=1960&toYear=2005&posMonth=&predMonth=&avgPeriod=&submit=%B2%E9%D1%AF%CA%FD%BE%DD&dump_search_data=1'
    response=requests.get(url=url,headers=headers).text
    with open('降水.txt','a',encoding='utf-8') as f:
        f.write(response)
        time.sleep(2)