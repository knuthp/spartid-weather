import requests
import xmltodict
import collections


class MetHistory:
    def __init__(self):
        None        
        
    def getStationsActive(self):
        url = 'http://eklima.met.no/met/MetService'
        params = collections.OrderedDict()
        params['invoke'] = 'getStationsProperties' 
        params['stations'] = ''
        params['username'] = ''
        r = requests.get(url=url, params=params)
        print r.url
        # print r.text
        resp = xmltodict.parse(r.text)
        ret = self.stationFromMetToSimple(resp, 'getStationsProperties')
        return ret
        
    def getStationsWithHourlyTemperature(self):
        url = 'http://eklima.met.no/met/MetService'
        params = collections.OrderedDict()
        params['invoke'] = 'getStationsFromTimeserieTypeStationsElemCode' 
        params['timeserietype'] = '2'
        params['stations'] = ''
        params['elem_code'] = 'TAX'
        params['username'] = ''
        r = requests.get(url=url, params=params)
        print r.url
        # print r.text
        resp = xmltodict.parse(r.text)
        ret = self.stationFromMetToSimple(resp, 'getStationsFromTimeserieTypeStationsElemCode')
        return ret

    def stationFromMetToSimple(self, resp, methodName):
        arr = resp['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:' + methodName + 'Response']['return']['item']
        ret = []
        for i in arr:
            if i['toYear']['#text'] == "0":
                ret.append({'id':i['stnr']['#text'], 'name':i['name']['#text'], 'county':i['department'].get('#text'), 'pos_utm':{'east':i['utm_e']['#text'], 'north':i['utm_n']['#text'], 'amsl':i['amsl']['#text'], 'zone':i['utm_zone']['#text']}})
        
        print "{0} Stations total={1}, active={2}".format(methodName, len(arr), len(ret))
        return ret
    

class Station:
    
    def __init__(self, stationId):
        self.stationId = stationId
        
    def getProperties(self):
        url = 'http://eklima.met.no/met/MetService'
        params = collections.OrderedDict()
        params['invoke'] = 'getStationsProperties' 
        params['stations'] = self.stationId
        params['username'] = ''
        r = requests.get(url=url, params=params)
        print r.url
        print r.text
        resp = xmltodict.parse(r.text)        
        ret = self.stationFromMetToSimple(resp, 'getStationsProperties')
        return ret
        
        
    def getDailyTemp(self, fromDate, toDate):
        url = 'http://eklima.met.no/met/MetService'
        params = collections.OrderedDict()
        params['invoke'] = 'getMetDataValues' 
        params['timeserietypeID'] = '0' 
        params['format'] = ''
        params['from'] = fromDate
        params['to'] = toDate
        params['stations'] = self.stationId
        params['elements'] = 'tan,tam,tax',
        params['hours'] = ''
        params['months'] = ''
        params['username'] = ''
        r = requests.get(url=url, params=params)
        print r.url
        print r.text
        resp = xmltodict.parse(r.text)
        arr = resp['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:getMetDataValuesResponse']['return']['Metdata']['timeStamp']
        ret = []
        for i in arr:
            time = i['@from']
            minimum = 0.0
            maximum = 0.0
            mean = 0.0
            for j in  i['location']['weatherElement']:
                if j['@id'] == 'TAN':
                    minimum = float(j['value'])
                elif j['@id'] == 'TAX':
                    maximum = float(j['value'])
                elif j['@id'] == 'TAM':
                    mean = float(j['value'])
            ret.append({'time': time, 'values' : {'minimum' : minimum, 'maximum' : maximum, 'mean' : mean}})
        return ret

    def getHourlyTemp(self, date):
        url = 'http://eklima.met.no/met/MetService'
        params = collections.OrderedDict()
        params['invoke'] = 'getMetDataValues' 
        params['timeserietypeID'] = '2' 
        params['format'] = ''
        params['from'] = date
        params['to'] = date
        params['stations'] = self.stationId
        params['elements'] = 'tan,tax',
        params['hours'] = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23'
        params['months'] = ''
        params['username'] = ''
        r = requests.get(url=url, params=params)
        print r.url
        print r.text
        resp = xmltodict.parse(r.text)
        arr = resp['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:getMetDataValuesResponse']['return']['Metdata']['timeStamp']
        ret = []
        for i in arr:
            time = i['@from']
            minimum = 0.0
            maximum = 0.0
            for j in  i['location']['weatherElement']:
                if j['@id'] == 'TAN':
                    minimum = float(j['value'])
                elif j['@id'] == 'TAX':
                    maximum = float(j['value'])
            ret.append({'time': time, 'values' : {'minimum' : minimum, 'maximum' : maximum}})
        return ret
        

    def stationFromMetToSimple(self, resp, methodName):
        item = resp['SOAP-ENV:Envelope']['SOAP-ENV:Body']['ns1:' + methodName + 'Response']['return']['item']
        return {'id':item['stnr']['#text'], 
                'name':item['name']['#text'], 
                'county':item['department'].get('#text'), 
                'pos_utm':{'east':item['utm_e']['#text'], 
                           'north':item['utm_n']['#text'], 
                           'amsl':item['amsl']['#text'], 
                           'zone':item['utm_zone']['#text']
                           }
                }
        

    
    
if __name__ == '__main__':
    # print MetHistory().getStationsActive()
    # print MetHistory().getStationsWithHourlyTemperature()
    metDataValues = Station('19710')
    # print metDataValues.getDailyTemp('2016-05-19', '2016-06-20')
    # print metDataValues.getHourlyTemp('2016-06-20')
    # print metDataValues.getHourlyTemp('2016-06-20')
    print metDataValues.getProperties()
    
