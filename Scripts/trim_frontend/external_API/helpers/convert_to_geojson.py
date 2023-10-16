import os
import json


class GeoJson:
    def __init__(self, parcel_json=None, fp=None):
        self.fp = fp
        self.parcel_json = parcel_json
        if fp:
            self.fp_geojson = os.path.join(os.path.dirname(self.fp), "output.geojson")
        else:
            self.fp_geojson = os.path.join(os.path.dirname(__file__), "output.geojson")

    def _create_polygon_feature(self, coordinates):
        # Swap the order of longitude and latitude for each coordinate
        swapped_coordinates = [[lon, lat] for lat, lon in coordinates]

        return {
            "type": "Feature",
            "geometry": {"type": "Polygon", "coordinates": [swapped_coordinates]},
            "properties": {},
        }

    def _convert_to_geojson(self, json_data):
        features = []
        for key, coordinates in json_data.items():
            feature = self._create_polygon_feature(coordinates)
            feature["properties"]["title"] = key
            features.append(feature)

        return {"type": "FeatureCollection", "features": features}

    def convert_json(self):
        if self.fp:
            with open(self.fp, "r") as file:
                self.parcel_json = json.load(file)

        geojson_data = self._convert_to_geojson(self.parcel_json)

        with open(self.fp_geojson, "w") as outfile:
            json.dump(geojson_data, outfile)
        return self.fp_geojson
