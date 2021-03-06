import json
from collections import Counter
from django.conf import settings
import os

json_loc = os.path.join(settings.BASE_DIR, 'nlpPipeline1/static/nlpPipeline1/js')


class PlottingData:
    def __init__(self):
        self._filenames = None
        self.n_files = None
        self._points = None
        self._colors = None
        self._n_clusters = None
        self._named_entities = None
        self._clusters = None
        self._cluster_points = None
        self._rand_dict = {'rand': 0.0, 'precision': 0.0, 'recall': 0.0, 'f1': 0.0}
        self.__color_ref = 10*['#E82C0C', '#3AFF00', '#0092FF', '#FFE800', '#FF8000', '#0DE7FF', '#E83C4B']

    def set_filenames(self, fnames):
        self._filenames = fnames
        self.n_files = len(fnames)

    def set_points(self, points_array):
        self._points = dict()
        for i, file in enumerate(self._filenames):
            self._points[file] = points_array[i]

    def set_rand(self,rand):
        self._rand_dict = rand

    def set_colors(self, labels):
        self._colors = dict()
        for i, file in enumerate(self._filenames):
            self._colors[file] = self.__color_ref[labels[i]]

    def set_clusters(self, n_clusters, clusters, cluster_points):
        self._n_clusters = n_clusters
        self._clusters = clusters
        self._cluster_points = cluster_points

    def set_named_entities(self, entities_dict):
        self._named_entities = entities_dict

    def prepare_to_plot(self):
        data = dict()
        data['fnames'] = self._filenames
        data['rand_index'] = self._rand_dict['rand']
        data['precision'] = self._rand_dict['precision']
        data['recall'] = self._rand_dict['recall']
        data['f1'] = self._rand_dict['f1']
        for file in self._filenames:
            filedata = dict()
            filedata['xy'] = self._points[file].tolist()
            filedata['color'] = self._colors[file]
            filedata['cluster'] = None
            for key, value in self._clusters.items():
                if file in self._clusters[key]:
                    filedata['cluster'] = key
            if self._named_entities is not None:
                filedata['org_entities'] =  dict(self._named_entities['file_org'])[file]

                filedata['person_entities'] = dict(self._named_entities['file_persons'])[file]

                filedata['place_entities'] = dict(self._named_entities['file_places'])[file]

                filedata['loc_entities'] =  dict(self._named_entities['file_loc'])[file]

                filedata['noun_entities'] = dict(self._named_entities['file_nouns'])[file]

            data[file] = filedata
        data['n_clusters'] = self._n_clusters
        for i in range(self._n_clusters):
            clusterdata = dict()
            clusterdata['xy'] = self._cluster_points[i].tolist()
            clusterdata['color'] = self.__color_ref[i]
            if self._named_entities is not None:
                clusterdata['org_entities'] = dict(self._named_entities['org'])[i]

                clusterdata['person_entities'] = dict(self._named_entities['persons'])[i]

                clusterdata['place_entities'] = dict(self._named_entities['places'])[i]

                clusterdata['loc_entities'] = dict(self._named_entities['loc'])[i]

                clusterdata['noun_entities'] = dict(self._named_entities['nouns'])[i]

                clusterdata['summary'] =dict(self._named_entities['summary'])[i]

            data[i] = clusterdata
        with open(os.path.join(json_loc, 'plot.json'), 'w+') as f:
            json.dump(data, f, indent=4)
        return data

    def status(self):
        print("Number of Files : " + str(self.n_files))
        print("Files : " + str(self._filenames))
        print("Points : \n", self._points)
        print("Colors : \n", self._colors)
        print("Number of CLusters : " + str(self._n_clusters))
        print("Clusters : \n", self._clusters)