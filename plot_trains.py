from shapely.wkt import loads as wkt_loads
import tifffile as tiff
import matplotlib.pyplot as plt
import descartes
from lib.utils import read_train, read_grid_sizes


def plot_image(img_id):
    """Plots Tiff image, with polygons overlaid.
    """
    COLORS = {
        1 : '0.7',
        2 : '0.4',
        3 : '#b35806',
        4 : '#dfc27d',
        5 : '#1b7837',
        6 : '#a6dba0',
        7 : '#74add1',
        8 : '#4575b4',
        9 : '#f46d43',
        10: '#d73027',
        }
    img = tiff.imread('{0}{1}.tif'.format(figure_dir, img_id))
    
    grid_size = grids[img_id]
    polygons =  shapes[img_id]
    
    xmin, xmax = 0, grid_size[0]
    ymin, ymax = grid_size[1], 0

    fig, ax, img = tiff.imshow(img)
    ax.set_xlim(0, xmax)
    ax.set_ylim(ymin, 0)    

    for cat in polygons.keys():
        for polygon in polygons[cat].geoms:
            ax.add_patch(descartes.PolygonPatch(polygon, color = COLORS[int(cat)], lw = 0, alpha = 0.7)) 

    return (fig, ax, img)

if __name__ == '__main__':
    data_dir = 'data/'
    figure_dir = 'data/three_band/'

    shapes = read_train('data/train_wkt_v4.csv')
    grids = read_grid_sizes('data/grid_sizes.csv')

    train_imgs = shapes.keys()

    for img in train_imgs:
        plot_image(img)
        plt.savefig('figures/{0}'.format(img))
