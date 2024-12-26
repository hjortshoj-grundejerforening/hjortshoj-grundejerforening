import json
import string

# Matrikelnumre 4b samt 4ax til og med 4ei (å anvendes ikke, så aå eller då eksistere ikke)
# Vi tilføjer 4b for Løvagervej, 4fp for Georgsmindevej og Bygbjerg, samt 4fq for Sastrupvej
matrikelnumre = []
matrikelnumreveje = ['4b', '4fp', '4fq']

dkAlfabet = string.ascii_lowercase + 'æø'
# index of 1 and index of 2
firstIndex = 0 # Indeks for 'a' -> vi vil maksimum nå til 4 (== 'e')
secondIndex = 23 # Indeks for 'x'

while firstIndex < 5:
    matrikelnummer = '4' + dkAlfabet[firstIndex] + dkAlfabet[secondIndex]
    matrikelnumre.append(matrikelnummer)

    secondIndex += 1
    if secondIndex >= len(dkAlfabet):
        firstIndex += 1
        secondIndex = 0

    if matrikelnummer == '4ei':
        break

matrikelIder = []
vejIder = []

matrikelFeatureCollection = {
"type": "FeatureCollection",
"name": "jordstykke",
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
"features":[]
}

vejFeatureCollection = {
"type": "FeatureCollection",
"name": "jordstykke",
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
"features":[]
}

jordstykkeFeatureCollection = {
"type": "FeatureCollection",
"name": "veje",
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
"features":[]
}

with open('matrikel.kilde.geojson') as f:
    d = json.load(f)
    features = d['features']
    for feature in features:
        
        matrikelnummer = feature['properties']['matrikelnummer']
        if matrikelnummer in matrikelnumre:
            lokalId = feature['properties']['jordstykkelokalid'] 
            matrikelIder.append(lokalId)
            matrikelFeatureCollection['features'].append(feature)

        if matrikelnummer in matrikelnumreveje:
            lokalId = feature['properties']['jordstykkelokalid'] 
            vejIder.append(lokalId)
            matrikelFeatureCollection['features'].append(feature)

with open('matrikel.renset.geojson', 'w', encoding='utf-8') as f:
    json.dump(matrikelFeatureCollection, f, ensure_ascii=False, indent=4)

with open('jordstykke.kilde.geojson') as f:
    d = json.load(f)
    features = d['features']
    for feature in features:
        id = feature['properties']['id_lokalid']
        if id in matrikelIder:
            jordstykkeFeatureCollection['features'].append(feature)
        
        if id in vejIder:
            vejFeatureCollection['features'].append(feature)

with open('jordstykke.renset.geojson', 'w', encoding='utf-8') as f:
    json.dump(jordstykkeFeatureCollection, f, ensure_ascii=False, indent=4)

with open('geodata.renset.js', 'w', encoding='utf-8') as f:
    s = f'\n\n /* Geodata fra matrikel.renset.geojson*/\n\n let vejData = {json.dumps(vejFeatureCollection, ensure_ascii=False, indent=4)}\n\n /* Geodata fra jordstykke.renset.geojson*/\n\n let jordstykkeData = {json.dumps(jordstykkeFeatureCollection,  ensure_ascii=False, indent=4)}'
    f.write(s)
