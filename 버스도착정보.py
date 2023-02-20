import requests
import json
import xmltodict

def busStation(station_name:str): # 정류장 아이디 불러오는 함수
    url = 'http://apis.data.go.kr/6410000/busstationservice/getBusStationList'
    params ={
        'serviceKey' : '공공데이터 포털에서 받은 서비스 키 입력',
        'keyword' : station_name
        }

    response = requests.get(url, params=params)

    jsonString = json.dumps(xmltodict.parse(response.text), indent=4,ensure_ascii=False)
    json_object = json.loads(jsonString)
    a = json_object["response"]
    b = a["msgBody"]
    c = b["busStationList"] 
    sum = 0
    stations = []
    print("조회를 원하시는 정류장의 숫자를 입력해 주세요.")
    for i in c:
        stations.insert(sum,i["stationId"])
        sum = sum + 1
        print(sum,i["mobileNo"],i["stationName"],i["stationId"])
    a = int(input())
    if sum < a:
        print("조회가 불가 합니다.")
        return
    else :
        return stations[a-1]
    
def routeId(routeId:str): # 노선 정보 불러오는 함수 
    url = 'http://apis.data.go.kr/6410000/busrouteservice/getBusRouteInfoItem'
    params ={
        'serviceKey' : '공공데이터 포털에서 받은 서비스 키 입력',
        'routeId' : routeId
        }

    response = requests.get(url, params=params)

    jsonString = json.dumps(xmltodict.parse(response.text), indent=4,ensure_ascii=False)
    json_object = json.loads(jsonString)
    a = json_object["response"]
    b = a["msgBody"]
    c = b["busRouteInfoItem"]
    return c["routeName"] # 노선 번호 값 반환

def busArrival():  # 버스 도착 정보 불러오는 함수
    station_name = str(input())
    stationId = busStation(station_name)
    url = 'http://apis.data.go.kr/6410000/busarrivalservice/getBusArrivalList'
    params ={
        'serviceKey' : '공공데이터 포털에서 받은 서비스 키 입력', 
        'stationId' : stationId 
        }

    responses = requests.get(url, params=params)

    jsonString = json.dumps(xmltodict.parse(responses.text), indent=4,ensure_ascii=False)
    json_object = json.loads(jsonString)
    try :
        a = json_object["response"]
        b = a["msgBody"]
        c = b["busArrivalList"]
        print("\n\n귀하가 조회하신 버스 도착 정보 입니다.\n=================================")
        for i in c :
            routeName = routeId(i["routeId"])
            if str(i["remainSeatCnt1"]) == "-1":
                print(routeName+"번 버스("+str(i["plateNo1"])+")",str(i["predictTime1"])+"분 후 도착합니다.")
            else:
                print(routeName+"번 버스("+str(i["plateNo1"])+")",str(i["predictTime1"])+"분 후 도착합니다.",str(i["remainSeatCnt1"])+"석")
    except:
        print("결과를 조회할 수 없습니다.")

    return

busArrival()
