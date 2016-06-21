import requests
import xmltodict
import collections



class Station:
    
    def __init__(self, stationId):
        self.stationId = stationId
        
    def getDailyTemp(self, fromDate, toDate):
        url='http://eklima.met.no/met/MetService'
        params = collections.OrderedDict()
        params['invoke'] = 'getMetDataValues' 
        params['timeserietypeID'] = '0' 
        params['format'] =''
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
        
    
    
if __name__ == '__main__':
    metDataValues = Station('19710')
    print metDataValues.getDailyTemp('2016-05-19', '2016-06-20')
