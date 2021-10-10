import matplotlib.pyplot as plt
import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cluster = -1
        self.previous_cluster = -1

    def set_cluster(self, number=-1):
        self.previous_cluster = self.cluster
        self.cluster = number


def dist(p1, p2):
    return np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def random_points(n):
    points = []
    for i in range(n):
        points.append(Point(np.random.randint(0, n), np.random.randint(0, n)))
    return points


def calculateCentroids(points, clusterCount):
    listX = list(map(lambda point: point.x, points))
    listY = list(map(lambda point: point.y, points))
    x = np.mean(listX)  # вычисляет среднее арифметическое значений элементов массива.
    y = np.mean(listY)
    R = 0
    for p in points:
        R = max(R, dist(p, Point(x, y)))  # находим радиус == самой дальней точки

    ax = plt.gca()  # стартовый круг для наглядности
    circle = plt.Circle((x, y), R, color='b', fill=False)
    ax.add_patch(circle)

    centroids = []
    for i in range(clusterCount):
        point = Point(x + R * np.cos(2 * np.pi * i / clusterCount),
                      y + R * np.sin(2 * np.pi * i / clusterCount))
        point.cluster = i
        centroids.append(point)  # центроиды по формуле
    return centroids


def initPoints(pointsAmount):
    init_points = random_points(pointsAmount)
    plt.scatter(list(map(lambda point: point.x, init_points)),
                list(map(lambda point: point.y, init_points)),
                color='k')
    return init_points


def initCentroids(points, clusterCount):
    init_centroids = calculateCentroids(points, clusterCount)
    plt.scatter(list(map(lambda point: point.x, init_centroids)),
                list(map(lambda point: point.y, init_centroids)),
                color='r')
    return init_centroids


def get_closest_cluster(point, centroids):
    min = dist(point, centroids[0])
    minIndex = 0
    for i in range(len(centroids)):
        distance = dist(point, centroids[i])
        if (min > distance):
            min = distance
            minIndex = i
    return minIndex


def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


def draw_Clusters(clusters, centroids):
    colors = get_cmap(len(centroids) + 1)

    for cluster in clusters:
        indexx = clusters.index(cluster)
        plt.scatter(list(map(lambda point: point.x, cluster)),
                    list(map(lambda point: point.y, cluster)),
                    facecolor=colors(indexx))

    for centroid in centroids:
        plt.scatter(list(map(lambda point: point.x, centroids)),
                    list(map(lambda point: point.y, centroids)),
                    color='k')


def move_Centroids(centroids, clusters):
    for i in range(len(clusters)):
        listX = list(map(lambda point: point.x, clusters[i]))
        listY = list(map(lambda point: point.y, clusters[i]))
        x = np.mean(listX)  # вычисляет среднее арифметическое значений элементов массива.
        y = np.mean(listY)

        centroids[i].x = x
        centroids[i].y = y


if __name__ == "__main__":
    points_Count = 4000  # кол-во тчк
    clusterCount = 5  # кол-во кластеров
    maxIterationCount = 10  # макс количество возможных шагов

    points = initPoints(points_Count)
    centroids = initCentroids(points, clusterCount)

    plt.show()

    for i in range(maxIterationCount):

        clusters = []
        for m in range(clusterCount):
            clusters.append([])

        for point in points:
            index = get_closest_cluster(point, centroids)
            clusters[index].append(point)

        move_Centroids(centroids, clusters)

        draw_Clusters(clusters, centroids)
        plt.show()

    #plt.show()


