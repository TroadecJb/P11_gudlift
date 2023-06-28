dicoBookedPlaces = {
    "comp1": [
        {"club1": "2"},
        {"club2": "3"},
    ],
    "comp2": [
        {"club3": "5"},
    ],
}


# print(dicoBookedPlaces)

compToGet = "comp2"
clubToGet = "club3"

print("aaaa", dicoBookedPlaces[compToGet][0])
if dicoBookedPlaces.get(compToGet) is not None:
    comp = dicoBookedPlaces[compToGet][0]
    print(comp)
    if comp.get(clubToGet) is not None:
        val = int(comp[clubToGet])
        print(val)
    else:
        dicoBookedPlaces[compToGet].append({clubToGet: "9"})
else:
    dicoBookedPlaces[compToGet] = [{clubToGet: "10"}]

print(dicoBookedPlaces)

# dicoBookedPlaces[compToGet][0][clubToGet] = str(999)

# print(dicoBookedPlaces)

# print(dicoBookedPlaces["comp1"]["club2"])
