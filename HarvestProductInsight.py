import requests
import json
import time
import datetime

year  = "2018"
month = "08"
day   = "21"

outfilename = "outfile.{1}.{0}.{2}.json".format(month, year, day)
date_time_start = '{0}.{1}.{2} 00:00:01'.format(day, month, year)
pattern = '%d.%m.%Y %H:%M:%S'
epoch_start = int(time.mktime(time.strptime(date_time_start, pattern)))
epoch_start_ms = int(round(epoch_start * 1000)) + 1

print (epoch_start_ms)

date_time_end = '{0}.{1}.{2} 23:59:59'.format(day, month, year)
epoch_end = int(time.mktime(time.strptime(date_time_end, pattern)))
epoch_end_ms = int(round(epoch_end * 1000)) + 1
print (epoch_end_ms)

cookies = {
    '__qca': 'P0-54468861-1506957397263',
    'cs_thomsonreuters_com_astate_prod': 'John',
    'cs_thomsonreuters_com_firm_info_prod': '199910%7c14172022%7c1347419',
    'LastInteractionDate': '1511989281331$0',
    '_ga': 'GA1.2.1475314366.1505834663',
    'SMSESSION': 'LOGGEDOFF',
    'check': 'true',
    'tr_ewp_dismissiblebanner': '1',
    'AMCVS_A7D63BC75245AE300A490D4D%40AdobeOrg': '1',
    's_cc': 'true',
    'mbox': 'PC#3e79723f972449a58a535269dba7dd5c.20_56#1581089920|session#04138eb3ff2e42a3922d8e24b739936d#1523551704',
    'AMCV_A7D63BC75245AE300A490D4D%40AdobeOrg': '1406116232%7CMCIDTS%7C17634%7CMCMID%7C77569248223938459970690641414512458149%7CMCAAMLH-1524154642%7C9%7CMCAAMB-1524154642%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1523557042s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-17641%7CvVersion%7C2.5.0',
    'pi_auth': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkc3QiOiJwcm9kdWN0LWluc2lnaHQiLCJleHAiOjE1NTgxMjAyMjAsImlhdCI6MTUyNjU4NDIyMCwiaXNzIjoicHJvZHVjdC1pbnNpZ2h0Iiwic3ViIjoiM2NlMjljMTAtYWI2Ni00MjQ5LTg3MzQtOWViODkyOGU0YTE5Iiwic3ViX2VtYWlsIjoiam9obi53eW1hbkB0aG9tc29ucmV1dGVycy5jb20iLCJzdWJfZ3JhdmF0YXIiOiI0ZWY5OGZiYTcwZDM3MzIyNDg1MDI4NzgwN2UwYjVjZSIsInN1Yl9uYW1lIjoiSm9obiBXeW1hbiIsInN1Yl9wcm92aWRlci1pZCI6IjQ1MDAwNDQiLCJzdWJfcHJvdmlkZXItbmFtZSI6InNhZmUiLCJ0aWQiOiIxM2VjZmUzMC1hMzM3LTQwMGEtNWFjYS05OGFmYzY2ZjFhOTMifQ.0CHTfCDNqw4X4z0ufau3x43rDQNeiBETmXysVqG0P7k',
    '__unam': '3ff306d-1627763661d-425b98-34',
}

headers = {
    'Origin': 'https://product-insight.thomsonreuters.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://product-insight.thomsonreuters.com/blue-moon/',
    'Connection': 'keep-alive',
    'kbn-xsrf-token': 'kibana',
}

params = (
    ('timeout', '0'),
    ('ignore_unavailable', 'true'),
    ('preference', '1533120393636'),
)

#data1 = '{"index":"blue-moon-{0}.{1}","ignore_unavailable":true}'.format(year, month)
data1 = '{"index":"' +  "blue-moon-{0}.{1}".format(year, month) + '","ignore_unavailable":true}'

outfile = open(outfilename, "w+") 
outfile.write("[")

start_date_ms = epoch_start_ms
total_items = 0
while(start_date_ms < epoch_end_ms):
    end_date_ms = start_date_ms+900*1000

    print("start " + datetime.datetime.fromtimestamp(start_date_ms/1000).strftime('%Y-%m-%d %H:%M:%S'))
    print("end "   + datetime.datetime.fromtimestamp(end_date_ms/1000).strftime('%Y-%m-%d %H:%M:%S'))

    data2 = '{"size":50000,"sort":[{"#_traac-timestamp":{"order":"desc","unmapped_type":"boolean"}}],"query":{"filtered":{"query":{"query_string":{"query":"*","lowercase_expanded_terms":false,"analyze_wildcard":true}},"filter":{"bool":{"must":[{"query":{"match":{"c-product-m-app_s":{"query":"Onvio Center","type":"phrase"}}}},{"range":{"#_traac-timestamp":{"gte":'+str(start_date_ms)+',"lte":'+str(end_date_ms)+'}}}],"must_not":[]}}}},"highlight":{"pre_tags":["@kibana-highlighted-field@"],"post_tags":["@/kibana-highlighted-field@"],"fields":{"*":{}},"fragment_size":2147483647},"aggs":{"2":{"date_histogram":{"field":"#_traac-timestamp","interval":"1m","pre_zone":"-04:00","pre_zone_adjust_large_interval":true,"min_doc_count":0,"extended_bounds":{"min":'+str(start_date_ms)+',"max":'+str(end_date_ms)+'}}}},"fields":["*","_source"],"script_fields":{"clock-difference-computed_n":{"script":"doc[\'event-timestamp_n\'].value - doc[\'#_traac-timestamp_milli\'].value / 1000","lang":"expression"}},"fielddata_fields":["#_traac-timestamp","#_traac-collected_time_date","c-product-m-device-utc_s","m-startDate_s","m-endDate_s"]}'
    
    j1 = json.loads(data1)
    j2 = json.loads(data2)

    d = json.dumps(j1) + "\n" + json.dumps(j2) + "\n"
    response = requests.post('https://product-insight.thomsonreuters.com/blue-moon/elasticsearch/_msearch', headers=headers, params=params, cookies=cookies, data=d)
 
    jsonResponse = json.loads(response.content)

    items = len(jsonResponse["responses"][0]["hits"]["hits"])
    print(str(items) + " items discovered")
    total_items += items

    show_time = True
    for o in jsonResponse["responses"][0]["hits"]["hits"]:
        jout = {}
        if show_time == True:
            show_time = False
            print( o["_source"]["#_traac-timestamp"] + "\n")

        for key in o.keys():
            if(key == "fields"): continue
            elif(key == "sort"): continue
            elif(key == "_source"):
                for key2 in o[key].keys():
                    jout[key2] = o["_source"][key2] 
            else:
                jout[key] = o[key]

        outfile.write(json.dumps(jout) + ",\n")
    start_date_ms = end_date_ms
outfile.write("]")
print(str(total_items) + " total items discovered")
