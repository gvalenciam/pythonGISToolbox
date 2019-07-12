# Base code for river processing Python toolbox
# Reclassification and size filter threshold used
# Input: GeoTiff image (obtained from Google Earth Engine for this case)
# Output: GeoJSON file with polygon outline data

import json
import rasterio
import numpy as np
import rasterio.features
from skimage import io
import matplotlib.pyplot as plt
from skimage import morphology
import png

box = []
shape_array = []
minSizeThreshold = 800
reclassiffyThreshold = 0.9
imageFile = 'Pucallpa1997.tif'
outputFileName = 'polygon.geojson'

# Read tif image
lista = io.imread(imageFile)

# Get the image box bounds
with rasterio.open(imageFile) as src:
    box = src.transform

# Reclassification using a numeric threshold
lista[np.where(lista < reclassiffyThreshold)] = 0
lista[np.where(lista >= reclassiffyThreshold)] = 1

# Size filter using a min size number threshold
first = morphology.remove_small_objects(lista.astype(bool), min_size=minSizeThreshold, connectivity=4)
first_int = first.astype(np.int16)

# Extract shapes from the size filtered image (one of the shapes is the river polygon)
for shape, value in rasterio.features.shapes(first_int, transform=box, connectivity=8):
    if value == 1:
        shape_array.append(shape)

# JSON structure for polygon
data = {"type": "FeatureCollection",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}}
feature_array = []
feature_ex = {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": []}}

# Add coordinates for each shape
for shape in shape_array:
    feature_ex['geometry']['coordinates'] = shape['coordinates']
    feature_array.append(feature_ex)
    feature_ex = {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": []}}

data['features'] = feature_array

# Save JSON in file
with open(outputFileName, 'w') as fout:
    json.dump(data, fout)



