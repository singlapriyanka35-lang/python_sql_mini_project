
# Import and Make a Simple GET Request
import requests

baseurl = "https://api.harvardartmuseums.org/"
apiKey = "c0abf07b-66e2-402c-8148-a3ef744344df"

def fetchClassification(): 
    url = baseurl+"classification"
    param = {
                "apikey" : apiKey,
                "size"   : 100 
            }
    response = requests.get(url, param)

    # check Status
    print("Status code : ", response.status_code)

    data = response.json()
    print("data : ", data)
    return True



# second Rest API

def fetchSpecificClasi(classiName):
    url = baseurl+"object"  # API URL
    all_records = []
    limit = 100
    # request data
    for i in range(1,26):
        param = {
                    "apikey" : apiKey,
                    "size": limit,
                    "page":i,
                    "hasimage": 1,
                    "classification":classiName
                }

    # Send the API request and get the response
        response = requests.get(url, param)

        # check Status
        #print("Status code : ", response.status_code)
        if response.status_code == 200:
            data = response.json()
            records = data.get('records', [])
            all_records.extend(records)
            return all_records
        else:
            return response.message
        

def makeRecordsDic(records):
       # print("data : ", records)
        artifacts = []
        media = []
        colors = []
        for i in records:
            
            artifacts.append(dict(
                id = i['id'],
                title = i['title'],
                culture = i['culture'],
                dated = i['dated'],
                period = i.get('period'), 
                century = i['century'],
                division = i['division'],
                medium = i.get('medium'),
                dimensions = i.get("dimensions"),
                department = i.get("department"),
                description = i.get('description'),
                classification = i['classification'],
                accessionyear = i['accessionyear'],
                accessionmethod = i['accessionmethod']
                )

            )

            media.append(dict(
                objectid   = i['objectid'],
                imagecount = i['imagecount'],
                mediacount = i['mediacount'],
                colorcount = i['colorcount'],
                rank       = i['rank'],
                datebegin  = i['datebegin'],
                dateend    = i['dateend']
            ))

            sub_list = i.get('colors')  
            if sub_list:   # only if colors exist
                #print("data:", sub_list)
                for j in sub_list:
                    colors.append(dict(
                        objectid   = i['objectid'],
                        color   = j.get('color'),
                        spectrum= j.get('spectrum'),
                        hue     = j.get('hue'),
                        percent = j.get('percent'),
                        css3     = j.get('css3')
                    )) 
        return artifacts, media, colors




    
    