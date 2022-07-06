import overpass
import geojson
import geopy.distance

BBOX_KM = 0.05
BBOX = [45, 135, 225, 315]
CENTRE = [-36.570628, 143.865551]
OUT_BBOX = "box.geojson"
OUT_ROAD = "road.geojson"


def point(centre, bearing, km):
    d = geopy.distance.distance(
        kilometers=km)
    return d.destination(point=centre, bearing=bearing)


p = [point(CENTRE, a, BBOX_KM) for a in BBOX]
pg_points = [(p[-1].longitude, p[-1].latitude)]
for pp in p:
    pg_points.append((pp.longitude, pp.latitude))


with open(OUT_BBOX, mode="w") as f:
    geojson.dump(
        geojson.FeatureCollection(
            [
                geojson.Feature(geometry=geojson.Polygon([pg_points])),
                geojson.Feature(geometry=geojson.Point((CENTRE[1], CENTRE[0])))
            ]
        ), f, indent=2)

pp = f'({p[2].latitude},{p[2].longitude},{p[0].latitude},{p[0].longitude})'
api = overpass.API()

overpass_url = f"""
(
  way["highway"="motorway"]{pp};
  way["highway"="trunk"]{pp};
  way["highway"="primary"]{pp};
);
out geom;
"""

print(overpass_url)

res = api.get(overpass_url)

with open(OUT_ROAD, mode="w") as f:
    geojson.dump(res, f, indent=2)
