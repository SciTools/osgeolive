import io

from cartopy.io.img_tiles import GoogleTiles
import matplotlib.pyplot as plt
import tornado.ioloop
import tornado.web


def tile_server(draw_callback=None, port=8888, debug=False):
    tiler = GoogleTiles()
    figure = plt.figure(figsize=(4, 4))
    ax = plt.axes([0, 0, 1, 1], projection=tiler.crs)
    ax.set_global()
    ax.outline_patch.set_visible(False)
    ax.background_patch.set_visible(False)

    if draw_callback:
        draw_callback(ax)

    class TileHandler(tornado.web.RequestHandler):
        def get(self, z, y, x):
            print 'Requested tile: ', x, y, z
            self.set_header('Content-Type', 'image/png')
            x_lim, y_lim = tiler.tile_bbox(int(x), int(y), int(z))
            ax.set_xlim(x_lim)
            ax.set_ylim(y_lim)
            buff = io.BytesIO()
            figure.canvas.print_figure(buff, format='png', dpi=64,
                                       facecolor='none', edgecolor='none')
            self.write(buff.getvalue())
            print 'Done'

    application = tornado.web.Application([
        (r"/tile/z([0-9]+)_y([0-9]+)_x([0-9]+).png", TileHandler),
    ], debug=debug)
    application.listen(port)
    print 'Server ready.'
    tornado.ioloop.IOLoop.instance().start()


def draw(geoaxes):
    import iris
    import iris.plot as iplt

    # Add some high-resolution coastlines so we can produce nice results
    # even when zoomed a long way in.
    geoaxes.coastlines('10m')

    fname = iris.sample_data_path('rotated_pole.nc')
    temperature = iris.load_cube(fname)
    iplt.pcolormesh(temperature)

    # Do the initial draw so that the coastlines are projected
    # (the slow part).
    plt.draw()


if __name__ == "__main__":
    tile_server(draw)
