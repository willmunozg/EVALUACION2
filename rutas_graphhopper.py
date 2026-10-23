import requests
import urllib.parse

geocode_url = "http://localhost:8082/api/1/geocode?"
route_url = "http://localhost:8082/api/1/route?"
key = "01f0b30a-60bb-4430-9784-485b15a8141e"      # Replace with your GraphHopper key (column TU_KEY_GRAPHHOPPER)

def geocoding (location, key):
    while location == "":
        location = input("Introduce la ubicación de nuevo: ")
    geocode_url = "http://localhost:8082/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1", "key":key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country=""

        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state=""

        if len(state) !=0 and len(country) !=0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) !=0:
            new_loc = name + ", " + country
        else:
            new_loc = name

        print("URL de la API de geocodificación para " + new_loc + " (Tipo de ubicación " + value + ")\n" + url)
    else:
        lat="null"
        lng="null"
        new_loc=location
        if json_status == 200:
            json_status = 404
            print("Ubicación no encontrada: " + location)
        else:
            print("Estado de la API de geocodificación: " + str(json_status) + "\nError message: " + json_data["message"])
    return json_status,lat,lng,new_loc

while True:
    loc1 = input("Ubicación de inicio: ")
    if loc1 == "salir" or loc1 == "s":
        break
    orig = geocoding(loc1, key)

    loc2 = input("Destination: ")
    if loc2 == "salir" or loc2 == "s":
        break
    dest = geocoding(loc2, key)

    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op="&point="+str(orig[1])+"%2C"+str(orig[2])
        dp="&point="+str(dest[1])+"%2C"+str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key":key}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Estado de la API de enrutamiento: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)

        print("=================================================")
        print("Indicaciones desde " + orig[3] + " to " + dest[3])
        print("=================================================")
        if paths_status == 200:
            km = (paths_data["paths"][0]["distance"])/1000
            meters = paths_data["paths"][0]["distance"]
            sec = int(paths_data["paths"][0]["time"]/1000%60)
            min = int(paths_data["paths"][0]["time"]/1000/60%60)
            hr = int(paths_data["paths"][0]["time"]/1000/60/60)
            print("Distancia recorrida: {0:.2f} km / {1:.2f} m".format(km, meters))
            print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.2f} km / {2:.2f} m )".format(path, distance/1000, distance))
            print("=============================================")
        else:
            print("Mensaje de error: " + paths_data["message"])
            print("*************************************************")
