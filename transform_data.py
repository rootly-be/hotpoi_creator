import csv
import re
from shapely.geometry import LineString

lines = []

try:
    with open('chemins.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # pour ignorer l'en-tête
        for row in reader:
            wkt = row[0]
            # extraire les points
            points_str = re.findall(r'\((.*?)\)', wkt)[0].split(', ')
            # convertir les points en tuple de flottants
            points = [(float(point.split(' ')[0]), float(point.split(' ')[1])) for point in points_str]
            line = LineString(points)
            lines.append(line)

    with open('resultat.txt', 'w') as f:
        for i, line in enumerate(lines):
            coords = str([list(point) for point in list(line.coords)])
            coords = coords.replace('[', '(', 1)  # remplace le premier crochet ouvrant par une parenthèse ouverte
            coords = coords[::-1].replace(']', ')', 1)[::-1]  # remplace le dernier crochet fermant par une parenthèse fermée
            if i != len(lines) - 1:  # si ce n'est pas la dernière ligne
                f.write('LineString' + coords + ',\n')
            else:  # si c'est la dernière ligne
                f.write('LineString' + coords)





except Exception as e:
    print(f'Une erreur est survenue : {e}')
