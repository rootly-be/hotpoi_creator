import csv
from pykml.factory import KML_ElementMaker as KML
from lxml import etree
from geopy.distance import geodesic
from shapely.geometry import LineString

def merge_close_points(points, threshold):
    merged_points = []

    while points:
        current_point = points.pop(0)
        merged = False

        for merged_point in merged_points:
            if geodesic(merged_point[0:2], current_point[0:2]).meters <= threshold:
                merged_geometry = LineString([merged_point[0:2], current_point[0:2]])
                merged_center = merged_geometry.centroid
                merged_point[0] = merged_center.x
                merged_point[1] = merged_center.y
                merged_point[2] += 1
                merged = True
                break

        if not merged:
            merged_points.append(current_point)

    return merged_points

def create_kml_file(routes):
    kml_doc = KML.kml(
        KML.Document(
            KML.Folder(
                KML.name('Points chauds')
            )
        )
    )

    all_points = []

    for route in routes:
        coordinates = route.replace('LINESTRING (', '').replace(')', '').split(', ')
        for coordinate in coordinates:
            lon, lat = coordinate.split(' ')
            all_points.append([float(lon), float(lat), 1])

    merged_points = merge_close_points(all_points, 25)

    for point in merged_points:
        lon, lat, count = point
        if count > 1:  # Ignorer les points seuls
            color = get_color(count)
            placemark = KML.Placemark(
                KML.Style(
                    KML.IconStyle(
                        KML.Icon(
                            KML.href('http://maps.google.com/mapfiles/ms/icons/{0}-dot.png'.format(color))
                        )
                    )
                ),
                KML.Point(
                    KML.coordinates(f"{lon},{lat}")
                ),
                KML.name('Point chaud'),
                KML.description('Lieu de passage à fort trafic')
            )
            kml_doc.Document.Folder.append(placemark)

    kml_root = etree.ElementTree(kml_doc)
    kml_root.write('points_chauds.kml', pretty_print=True)

def get_color(count):
    if count < 10:
        return 'green'
    elif count < 50:
        return 'yellow'
    else:
        return 'red'

if __name__ == '__main__':
    routes = []

    with open('routes.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Ignorer l'en-tête du fichier CSV
        for row in csv_reader:
            routes.append(row[0])

    create_kml_file(routes)