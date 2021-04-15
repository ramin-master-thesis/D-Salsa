from enum import Enum
from random import randrange, uniform

from graph.bipartite_graph import get_left_node_neighbors, get_right_node_neighbors


class Side(Enum):
    LEFT = True,
    RIGHT = False


class Salsa:
    def __init__(self, root_node, limit, walks, walks_length, reset_probability):
        self.root_node = root_node
        self.limit = limit
        self.walks = walks
        self.walks_length = walks_length
        self.reset_probability = reset_probability
        self.total_visits = 0

        self.current_left_node_visits = {}
        self.current_right_node_visits = {}
        self.total_right_node_visits = {}

    def compute(self, for_user=True):
        starting_side = Side.LEFT if for_user else Side.RIGHT
        return self.__compute(starting_side)

    def __compute(self, starting_side):
        if starting_side == Side.LEFT:
            self.current_left_node_visits[self.root_node] = self.walks
        else:
            self.current_right_node_visits[self.root_node] = self.walks

        switch_side = True

        for _ in range(self.walks_length):
            if switch_side:
                self.__iterate_current_side(self.root_node, self.reset_probability, starting_side)
            else:
                self.__iterate_other_side(starting_side)
            switch_side = not switch_side

        # for edge, visits in self.total_right_node_visits.items():
            # visit_percentage = visits / self.total_visits
            # print(f"Visited {edge} {visits} times, %{visit_percentage}")

        if starting_side == Side.LEFT:
            known_nodes = set(get_left_node_neighbors(self.root_node))
        else:
            known_nodes = {self.root_node}

        return self.__clean_recommendations(known_nodes)

    def __iterate_current_side(self, root_node, reset_probability, start_left=True):
        total_resets = 0
        (current_node_visits, get_node_neighbors, current_other_side_node_visits) = self.__get_side_package(start_left)

        for node in current_node_visits.keys():
            visits = current_node_visits.get(node)
            walks = 0
            resets = 0
            for i in range(visits):
                if uniform(0, 1) > reset_probability:
                    walks += 1
                else:
                    resets += 1

            edges = get_node_neighbors(node)

            if len(edges) > 0:
                for i in range(walks):
                    random_position = randrange(0, len(edges))
                    edge = edges[random_position]
                    current_other_side_node_visits[edge] = current_other_side_node_visits.get(edge, 0) + 1
                    if start_left:
                        self.total_right_node_visits[edge] = self.total_right_node_visits.get(edge, 0) + 1

            self.total_visits += walks

            total_resets += resets

        current_node_visits.clear()
        current_node_visits[root_node] = total_resets

    def __iterate_other_side(self, start_left=True):
        (current_node_visits, get_node_neighbors, current_other_side_node_visits) = self.__get_side_package(
            not start_left)

        for node, visits in current_node_visits.items():
            edges = get_node_neighbors(node)

            if len(edges) > 0:
                for i in range(visits):
                    random_position = randrange(0, len(edges))
                    edge = edges[random_position]
                    current_other_side_node_visits[edge] = current_other_side_node_visits.get(edge, 0) + 1
                    if not start_left:
                        self.total_right_node_visits[edge] = self.total_right_node_visits.get(edge, 0) + 1

        current_node_visits.clear()

    def __get_side_package(self, start_left=True):
        if start_left:
            return self.current_left_node_visits, get_left_node_neighbors, self.current_right_node_visits
        else:
            return self.current_right_node_visits, get_right_node_neighbors, self.current_left_node_visits

    def __clean_recommendations(self, known_nodes):
        not_visited_nodes = {k: v for k, v in self.total_right_node_visits.items() if k not in known_nodes}
        sorted_nodes = dict(sorted(not_visited_nodes.items(), key=lambda item: item[1], reverse=True))
        return list(sorted_nodes.items())[:self.limit]
