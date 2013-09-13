
import StringIO
import urllib2

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps

import cartopy.crs as ccrs
import iris
import iris.experimental.raster
import iris.quickplot as qplt


class RequestPut(urllib2.Request):
    def get_method(self):
        return 'PUT'


def connect_to_server(server, username, password):
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, server, username, password)
    handler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)


def exists_workspace(server, workspace):
    url = server + "/rest/workspaces/{}".format(workspace)
    headers = {'Content-type': 'text/xml'}
    request = urllib2.Request(url=url, headers=headers)
    try:
        result = urllib2.urlopen(request)
    except:
        return False
    return True


def create_workspace(server, workspace):
    url = server + "/rest/workspaces"
    headers = {'Content-type': 'text/xml'}
    data = '<workspace><name>{name}</name></workspace>'\
           '<enabled>true</enabled>'.format(name=workspace)
    request = urllib2.Request(url=url, data=data, headers=headers)
    result = urllib2.urlopen(request)
   

def exists_coveragestore(server, workspace, coveragestore):
    url = server + "/rest/workspaces/{}/coveragestores/{}".format(workspace, coveragestore)
    headers = {'Content-type': 'text/xml'}
    request = urllib2.Request(url=url, headers=headers)
    try:
        result = urllib2.urlopen(request)
    except:
        return False
    return True


def create_coveragestore(server, workspace, coveragestore):
    url = server + "/rest/workspaces/{}/coveragestores".format(workspace)
    headers = {'Content-type': 'text/xml'}
    
    #'<type>GeoTIFF</type>'\
    data = '<coverageStore>'\
               '<name>{name}</name>'\
               '<workspace>{workspace}</workspace>'\
               '<enabled>true</enabled>'\
           '</coverageStore>'.format(name=coveragestore, workspace=workspace)
    request = urllib2.Request(url=url, data=data, headers=headers)
    result = urllib2.urlopen(request)


def upload_file(server, workspace, coveragestore, filename, data):
    # The coverage will be given the same name as the coverage store.
    url = server + "/rest/workspaces/{}/coveragestores/{}/{}".format(workspace, coveragestore, filename)
    headers = {'Content-type': 'image/tiff'}
    request = RequestPut(url=url, data=data, headers=headers)
    result = urllib2.urlopen(request)


def update_coverage(server, workspace, coveragestore, coverage, data):
    url = server + "/rest/workspaces/{}/coveragestores/{}/coverages/{}".format(workspace, coveragestore, coverage)
    headers = {'Content-type': 'text/xml'}
    request = RequestPut(url=url, data=data, headers=headers)
    result = urllib2.urlopen(request)


def wms_image(server, layers):
    """ Retrieve and plot a WMS image.
    Hard-coded for a single WMS server and PlateCarre() images.
    Can plot on any projection"""
    
    xlim = plt.gca().get_xlim()
    ylim = plt.gca().get_ylim()
    bbox = [xlim[0], ylim[0], xlim[1], ylim[1]]
    
    # Construct the query string
    request = server
    request += "&version=1.1.0"
    request += "&request=GetMap"
    request += "&layers={}".format(layers)
    request += "&bbox={}".format(",".join([str(i) for i in bbox]))
    request += "&styles="
    request += "&width={}&height={}".format(512, 512)
    request += "&srs=EPSG:4326"
    request += "&format=image/jpeg"

    # Get jpeg from server.
    jpeg_bytes = urllib2.urlopen(request).read()
    pil_img = Image.open(StringIO.StringIO(jpeg_bytes))
    pil_img = ImageOps.flip(pil_img)
    
    # Turn the pil image into rgb array, to workaround a cartopy bug.
    img_array = np.array(list(pil_img.getdata())).reshape((pil_img.size[0], pil_img.size[1], -1)) / 256.0
    img_array = img_array.squeeze()

    # Plot the platecaree image in the current plot projection. 
    plt.gca().imshow(img_array, origin="lower",
                     extent=[bbox[0], bbox[2], bbox[1], bbox[3]],
                     transform=ccrs.PlateCarree())


def runme():

    # Load a cube into Iris
    filename = iris.sample_data_path("A1B.2098.pp")
    cube = iris.load_cube(filename)
    cube.coord(axis="x").guess_bounds()
    cube.coord(axis="y").guess_bounds()

    # Plot the cube with Iris, just to see it.
    qplt.contourf(cube)
    qplt.plt.gca().coastlines()
    qplt.show()
    
    # Export as GeoTIFF (shouldn't have to write to a physical file)
    iris.experimental.raster.export_geotiff(cube, 'temp.geotiff')
    data = open('temp.geotiff', "rb").read()

    # Publish to geoserver
    server = "localhost:8082"
    username, password = 'admin', 'geoserver'
    connect_to_server(server, username, password)

    workspace = "iris_test_ws"
    if not exists_workspace(server, workspace):
        create_workspace(server, workspace)
    
    coveragestore = "iris_test_cs"
    if not exists_coveragestore(server, workspace, coveragestore):
        create_coveragestore(server, workspace, coveragestore)

    filename = "file.geotiff"
    upload_file(server, workspace, coveragestore, filename, data)
    
    # Tell geoserver it's global EPSG:4326. Shouldn't need this eventually.
    coverage = coveragestore  # (they get the same name from geoserver)
    data = '<coverage>'\
                '<srs>EPSG:4326</srs>'\
                '<nativeCRS>EPSG:4326</nativeCRS>'\
                ' <nativeBoundingBox>'\
                    '<minx>-180.0</minx>'\
                    '<maxx>180.0</maxx>'\
                    '<miny>-90.0</miny>'\
                    '<maxy>90.0</maxy>'\
                    '<crs>EPSG:4326</crs>'\
                '</nativeBoundingBox>'\
                '<enabled>true</enabled>'\
            '</coverage>'
    update_coverage(server, workspace, coveragestore, coverage, data)

    # Use the new WMS service as a background image!
    wms_server = '{server}/{workspace}/wms?service=WMS'.format(server=server, workspace=workspace)
    layers = '{workspace}:{coveragestore}'.format(workspace=workspace, coveragestore=coveragestore)
    
    plt.axes(projection=ccrs.PlateCarree())
    plt.gca().set_extent([-40, 40, 20, 80])
    wms_image(wms_server, layers)
    plt.gca().coastlines()
    plt.show()


if __name__ == "__main__":
    runme()

