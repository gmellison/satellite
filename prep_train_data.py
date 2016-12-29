import pandas as pd 
import numpy as np
from shapely.wkt import loads as wkt_loads
from shapely.geometry import Point
from shapely.prepared import prep
from lib.utils import read_train, read_grid_sizes
import tifffile as tiff
from itertools import product, compress
from __future__ import division


def polygon_pixel_ranges(polygon, W, H, xmax, ymin):
 
    l, b, r, t = polygon.bounds    
    prepared_polygon = prep(polygon)

    x_range = np.array(range(int(W * (l / xmax)), int(W * (r / xmax))))
    y_range = np.array(range(int(H * (t / ymin)), int(H * (b / ymin))))
  
    x_trans = (x_range / W) * xmax
    y_trans = (y_range / H) * ymin

    prepared_polygon = prep(polygon) 
    points = map(Point, product(x_trans, y_trans))
    hits = map(prepared_polygon.contains, points)

    return list(compress(list(product(x_range, y_range)), hits))        

def multipolygon_to_pixels(multipolygon, W, H, xmax, ymin):

    polygon_pixels = np.array([], dtype = 'int64')

    i = 0
    for p in multipolygon.geoms:
        polygon_pixels = np.append(polygon_pixels,  polygon_pixel_ranges(p, W, H, xmax, ymin))

        i += 1
        print('{0} polygons processed'.format(i))
        
    return polygon_pixels

def category_pixels(img_id):

    out = {}

    xmax, ymin = grid_sizes[img_id]
    img = tiff.imread('{0}{1}.tif'.format(img_dir, img_id))
    H, W = img.shape[1:]
    polygons = shapes[img_id] 
 
    for cat in polygons.keys():
        print("working on image {0}, category {1}".format(img_id, cat))
        multipolygon = polygons[cat]
        pixels = multipolygon_to_pixels(multipolygon, W, H, xmax, ymin) 
        out[cat] = pixels
    
    return out


if __name__ == '__main__':
    
    data_dir = 'data/'
    img_dir = 'data/three_band/'

    shapes = read_train('data/train_wkt_v4.csv')
    imgs = shapes.keys()
    grid_sizes = read_grid_sizes('data/grid_sizes.csv')

    img_id = imgs[0]

    
