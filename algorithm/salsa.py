from random import randrange, uniform

from graph.graph import get_left_node_neighbors, get_right_node_neighbors


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

    def compute(self):
        is_left_to_right = True

        self.current_left_node_visits[self.root_node] = self.walks

        for i in range(self.walks_length):
            if is_left_to_right:
                self.__lef_iteration(self.root_node, self.reset_probability)
            else:
                self.__right_iteration()
            is_left_to_right = not is_left_to_right

        for edge, visits in self.total_right_node_visits.items():
            visit_percentage = visits / self.total_visits
            print(f"Visited {edge} {visits} times, %{visit_percentage}")

        known_nodes = set(get_left_node_neighbors(self.root_node))

        not_visited_nodes = {k: v for k, v in self.total_right_node_visits.items() if k not in known_nodes}
        sorted_nodes = dict(sorted(not_visited_nodes.items(), key=lambda item: item[1], reverse=True))

        return list(sorted_nodes.keys())[:self.limit]

    def __lef_iteration(self, root_node, reset_probability):
        total_resets = 0

        for node in self.current_left_node_visits.keys():
            visits = self.current_left_node_visits.get(node)
            walks = 0
            resets = 0

            for i in range(visits):
                if uniform(0, 1) > reset_probability:
                    walks += 1
                else:
                    resets += 1

            edges = get_left_node_neighbors(node)

            for i in range(walks):
                if len(edges) > 0:
                    random_position = randrange(0, len(edges))
                    edge = edges[random_position]
                    self.current_right_node_visits[edge] = self.current_right_node_visits.get(edge, 0) + 1
                    self.total_right_node_visits[edge] = self.total_right_node_visits.get(edge, 0) + 1

            self.total_visits += walks

            total_resets += resets

        self.current_left_node_visits.clear()
        self.current_left_node_visits[root_node] = total_resets

    def __right_iteration(self):
        for node, visits in self.current_right_node_visits.items():

            edges = get_right_node_neighbors(node)

            for i in range(visits):
                if len(edges) > 0:
                    random_position = randrange(0, len(edges))
                    edge = edges[random_position]
                    self.current_left_node_visits[edge] = self.current_left_node_visits.get(edge, 0) + 1

        self.current_right_node_visits.clear()
