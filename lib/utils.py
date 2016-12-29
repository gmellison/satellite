from shapely.wkt import loads as wkt_loads
import tifffile as tiff
import matplotlib.pyplot as plt
import descartes

def read_train(filepath):
    f = open(filepath, 'r')
    EMPTY = 'MULTIPOLYGON EMPTY\n'
    FIRST = 'ImageId,ClassType,MultipolygonWKT\n'    

    data = {}
    for line in f.readlines():
        if line == FIRST:
            continue

        img_id, class_type, raw_wkt = line.split(',', 2)

        if img_id not in data:
            data[img_id] = {}

        if raw_wkt.replace('"', '') == EMPTY:
            continue

        multi_polygon = wkt_loads(raw_wkt.replace('\n', '').replace('"',''))
        data[img_id][class_type] = multi_polygon 

    return data

def read_grid_sizes(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    line_split = map(lambda line: line.replace('\n', '').split(',') , lines) 
    return {l[0]: (float(l[1]), float(l[2])) for l in line_split[1:]}


