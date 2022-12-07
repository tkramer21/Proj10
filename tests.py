import os
import unittest, string, math, random, cProfile
from xml.dom import minidom
from numpy import matrix

from solution import Graph, Vertex, tollway_algorithm_again


class GraphTests(unittest.TestCase):
    """
    Begin Graph Part 1 Tests
    """

    def test_deg(self):

        # (1) test a-->b and a-->c
        vertex = Vertex('a')
        vertex.adj['b'] = 1
        self.assertEqual(1, vertex.deg())
        vertex.adj['c'] = 3
        self.assertEqual(2, vertex.deg())

        # (2) test a-->letter for all letters in alphabet
        vertex = Vertex('a')
        for i, char in enumerate(string.ascii_lowercase):
            self.assertEqual(i, vertex.deg())
            vertex.adj[char] = i

    def test_get_outgoing_edges(self):

        # (1) test a-->b and a-->c
        vertex = Vertex('a')
        expected = {('b', 1), ('c', 2)}
        vertex.adj['b'] = 1
        vertex.adj['c'] = 2
        actual = vertex.get_outgoing_edges()
        self.assertEqual(expected, actual)

        # (2) test empty case
        vertex = Vertex('a')
        expected = set()
        actual = vertex.get_outgoing_edges()
        self.assertEqual(expected, actual)

        # (3) test a-->letter for all letters in alphabet
        for i, char in enumerate(string.ascii_lowercase):
            vertex.adj[char] = i
            expected.add((char, i))
        actual = vertex.get_outgoing_edges()
        self.assertEqual(expected, actual)

    def test_get_vertex_by_id(self):

        graph = Graph()

        # (1) test basic vertex object
        vertex_a = Vertex('a')
        graph.vertices['a'] = vertex_a
        actual = graph.get_vertex_by_id('a')
        self.assertEqual(vertex_a, actual)

        # (2) test empty case
        actual = graph.get_vertex_by_id('b')
        self.assertIsNone(actual)

        # (3) test case with adjacencies
        vertex_b = Vertex('b')
        for i, char in enumerate(string.ascii_lowercase):
            vertex_b.adj[char] = i
        graph.vertices['b'] = vertex_b
        actual = graph.get_vertex_by_id('b')
        self.assertEqual(vertex_b, actual)

    def test_get_all_vertices(self):

        graph = Graph()
        expected = set()

        # (1) test empty graph
        actual = graph.get_all_vertices()
        self.assertEqual(expected, actual)

        # (2) test single vertex
        vertex = Vertex('$')
        graph.vertices['$'] = vertex
        expected.add(vertex)
        actual = graph.get_all_vertices()
        self.assertEqual(expected, actual)

        # (3) test multiple vertices
        graph = Graph()
        expected = set()
        for i, char in enumerate(string.ascii_lowercase):
            vertex = Vertex(char)
            graph.vertices[char] = vertex
            expected.add(vertex)
        actual = graph.get_all_vertices()
        self.assertEqual(expected, actual)

    def test_get_edge_by_ids(self):

        graph = Graph()

        # (1) neither end vertex exists
        actual = graph.get_edge_by_ids('a', 'b')
        self.assertIsNone(actual)

        # (2) one end vertex exists
        graph.vertices['a'] = Vertex('a')
        actual = graph.get_edge_by_ids('a', 'b')
        self.assertIsNone(actual)

        # (3) both end vertices exist, but no edge
        graph.vertices['a'] = Vertex('a')
        graph.vertices['b'] = Vertex('b')
        actual = graph.get_edge_by_ids('a', 'b')
        self.assertIsNone(actual)

        # (4) a -> b exists but b -> a does not
        graph.vertices.get('a').adj['b'] = 331
        actual = graph.get_edge_by_ids('a', 'b')
        self.assertEqual(('a', 'b', 331), actual)
        actual = graph.get_edge_by_ids('b', 'a')
        self.assertIsNone(actual)

        # (5) connect all vertices to center vertex and return all edges
        graph.vertices['$'] = Vertex('$')
        for i, char in enumerate(string.ascii_lowercase):
            graph.vertices[char] = Vertex(char)
            graph.vertices.get('$').adj[char] = i
        for i, char in enumerate(string.ascii_lowercase):
            actual = graph.get_edge_by_ids('$', char)
            self.assertEqual(('$', char, i), actual)

    def test_get_all_edges(self):

        graph = Graph()

        # (1) test empty graph
        actual = graph.get_all_edges()
        self.assertEqual(set(), actual)

        # (2) test graph with vertices but no edges
        graph.vertices['a'] = Vertex('a')
        graph.vertices['b'] = Vertex('b')
        actual = graph.get_all_edges()
        self.assertEqual(set(), actual)

        # (3) test graph with one edge
        graph.vertices.get('a').adj['b'] = 331
        actual = graph.get_all_edges()
        self.assertEqual({('a', 'b', 331)}, actual)

        # (4) test graph with two edges
        graph = Graph()
        graph.vertices['a'] = Vertex('a')
        graph.vertices['b'] = Vertex('b')
        graph.vertices.get('a').adj['b'] = 331
        graph.vertices.get('b').adj['a'] = 1855
        actual = graph.get_all_edges()
        expected = {('a', 'b', 331), ('b', 'a', 1855)}
        self.assertEqual(expected, actual)

        # (5) test entire alphabet graph
        graph = Graph()
        expected = set()
        for i, char in enumerate(string.ascii_lowercase):
            graph.vertices[char] = Vertex(char)
            for j, jar in enumerate(string.ascii_lowercase):
                if i != j:
                    graph.vertices.get(char).adj[jar] = 26 * i + j
                    expected.add((char, jar, 26 * i + j))

        actual = graph.get_all_edges()
        self.assertEqual(expected, actual)

    """
    End of Graphs Part 1 Tests
    """

    """
    Begin Graph Part 2 Tests
    """

    def test_dijkstra(self):
        """Basic Test cases"""
        graph = Graph()

        # (1) test on empty graph
        actual = graph.dijkstra('a', 'b')
        self.assertEqual(([], 0), actual)

        # (2) test on graph missing begin or dest
        graph.add_to_graph('a')
        actual = graph.dijkstra('a', 'b')
        self.assertEqual(([], 0), actual)
        actual = graph.dijkstra('b', 'a')
        self.assertEqual(([], 0), actual)

        # (3) test on single edge
        graph = Graph()
        graph.add_to_graph('a', 'b', 331)
        actual = graph.dijkstra('a', 'b')
        self.assertEqual((['a', 'b'], 331), actual)

        # (5) test on two edges
        graph = Graph()
        graph.add_to_graph('a', 'b', 331)
        graph.add_to_graph('b', 'c', 100)
        actual = graph.dijkstra('a', 'c')
        self.assertEqual((['a', 'b', 'c'], 431), actual)

        # (6) test where no path exists
        graph = Graph()
        graph.add_to_graph('a', 'b')
        actual = graph.dijkstra('b', 'a')
        self.assertEqual(([], 0), actual)

        # === (A) Grid graph tests ===#
        graph = Graph()

        # (5) test on nxn grid from corner to corner: should shoot diagonal
        grid_size = 5
        for x in range(grid_size):
            for y in range(grid_size):
                idx = f"{x},{y}"
                graph.vertices[idx] = Vertex(idx, x, y)
        for x in range(grid_size):
            for y in range(grid_size):
                if x < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x + 1},{y}", 1)
                    graph.add_to_graph(f"{x + 1},{y}", f"{x},{y}", 1)
                if y < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x},{y + 1}", 1)
                    graph.add_to_graph(f"{x},{y + 1}", f"{x},{y}", 1)
                if x < grid_size - 1 and y < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x + 1},{y + 1}", math.sqrt(2))
                    graph.add_to_graph(f"{x + 1},{y + 1}", f"{x},{y}", math.sqrt(2))

        actual = graph.dijkstra('0,0', '4,4')
        self.assertEqual(['0,0', '1,1', '2,2', '3,3', '4,4'], actual[0])
        self.assertAlmostEqual((grid_size - 1) * math.sqrt(2), actual[1])
        graph.reset_vertices()

        # (6) test on nxn grid with penalty for shooting diagonal
        for x in range(grid_size - 1):
            for y in range(grid_size - 1):
                graph.add_to_graph(f"{x},{y}", f"{x + 1},{y + 1}", 3)
                graph.add_to_graph(f"{x + 1},{y + 1}", f"{x},{y}", 3)

        actual = graph.dijkstra('0,0', '4,4')
        self.assertEqual((['0,0', '1,0', '2,0', '3,0', '4,0', '4,1', '4,2', '4,3', '4,4'], 8), actual)
        graph.reset_vertices()

    def test_dijkstra_large(self):
        # ===  Tollway graph tests ===#
        graph = Graph(csvf='test_csvs/astar/tollway_graph_csv.csv')
        # now must set of coordinates for each vertex:
        positions = [(0, 0), (2, 0), (4, 0), (7, 0), (10, 0), (12, 0), (2, 5), (6, 4), (12, 5), (5, 9), (8, 8), (12, 8),
                     (8, 10), (0, 2),
                     (4, 2), (9, 2), (9, -2), (7, 6), (8, 11), (14, 8)]

        for index, v_id in enumerate(list(graph.vertices)):
            graph.vertices[v_id].x, graph.vertices[v_id].y = positions[index]

        # (1) test Franklin Grove to Northbrook shortest path in both directions
        actual = graph.dijkstra('Franklin Grove', 'Northbrook')
        expected = (['Franklin Grove', 'A', 'B', 'G', 'J', 'M', 'Northbrook'], 22)
        self.assertEqual(expected, actual)
        graph.reset_vertices()

        actual = graph.dijkstra('Northbrook', 'Franklin Grove')
        expected = (['Northbrook', 'M', 'J', 'G', 'B', 'A', 'Franklin Grove'], 22)
        self.assertEqual(expected, actual)
        graph.reset_vertices()

        # (2) test Franklin Grove to Joliet shortest path - bypass slow path
        actual = graph.dijkstra('Franklin Grove', 'Joliet')
        expected = (['Franklin Grove', 'A', 'B', 'G', 'H', 'D', 'E', 'Joliet'], 35)
        self.assertEqual(expected, actual)
        graph.reset_vertices()

        actual = graph.dijkstra('Joliet', 'Franklin Grove')
        expected = (['Joliet', 'E', 'D', 'H', 'G', 'B', 'A', 'Franklin Grove'], 35)
        self.assertEqual(expected, actual)
        graph.reset_vertices()

        # (3) test Joliet to Chicago shortest path - bypass slow path
        actual = graph.dijkstra('Joliet', 'Chicago')
        expected = (['Joliet', 'E', 'D', 'H', 'G', 'J', 'K', 'L', 'Chicago'], 35)
        self.assertEqual(expected, actual)
        graph.reset_vertices()

        actual = graph.dijkstra('Chicago', 'Joliet')
        expected = (['Chicago', 'L', 'K', 'J', 'G', 'H', 'D', 'E', 'Joliet'], 35)
        self.assertEqual(expected, actual)
        graph.reset_vertices()

        # (4) test Northbrook to Belvidere - despite equal path lengths, A* heuristic will always prefer search to the left
        # (both heuristics will prefer the same path)
        actual = graph.dijkstra('Northbrook', 'Belvidere')
        expected = (['Northbrook', 'M', 'J', 'K', 'Belvidere'], 8)
        self.assertEqual(expected, actual)
        graph.reset_vertices()

        actual = graph.dijkstra('Belvidere', 'Northbrook')
        expected = (['Belvidere', 'K', 'J', 'M', 'Northbrook'], 8)
        self.assertEqual(expected, actual)
        graph.reset_vertices()

        # === (B) Big pre-generated graph tests ===#
        vertices = []
        e_graph = Graph(csvf="test_csvs/astar/test_astar_2.csv")
        t_graph = Graph(csvf="test_csvs/astar/test_astar_3.csv")
        position = [('a', 93, 41), ('b', 21, 31), ('c', 80, 13), ('d', 82, 60), ('e', 59, 79),
                    ('f', 84, 43), ('g', 74, 92), ('h', 95, 53), ('i', 85, 55), ('j', 98, 90),
                    ('k', 78, 53), ('l', 5, 55), ('m', 69, 36), ('n', 67, 92), ('o', 76, 98),
                    ('p', 42, 52), ('q', 69, 85), ('r', 29, 95), ('s', 18, 40), ('t', 97, 79),
                    ('u', 76, 21), ('v', 10, 88), ('w', 74, 80), ('x', 45, 93), ('y', 35, 68),
                    ('z', 65, 89)]
        for s, x, y in position:
            vertices.append(Vertex(s, x, y))
            e_graph.vertices[s].x = x
            t_graph.vertices[s].x = x
            e_graph.vertices[s].y = y
            t_graph.vertices[s].y = y
            e_graph.size += 1
            t_graph.size += 1

        def is_valid_path(graph, search_result):
            path, dist = search_result
            eps = 10 ** -8  # estimator of float
            length = 0
            for i in range(len(path) - 1):
                begin, end = path[i], path[i + 1]
                edge = graph.get_edge_by_ids(begin, end)
                if edge is None:
                    return False  # path contains some edge not in the graph
                length += edge[2]
            return abs(length - dist) < eps  # path consists of valid edges: return whether length matches

        # (5) test all 26 x 26 pairwise A* traversals across random matrix and ensure they return valid paths w/o error
        for begin in vertices:
            for end in vertices:
                if begin != end:
                    actual = e_graph.dijkstra(begin.id, end.id)
                    self.assertTrue(is_valid_path(e_graph, actual))
                    e_graph.reset_vertices()

    def test_a_star(self):

        # === Edge Cases === #

        # (1) test on empty graph
        graph = Graph()
        actual = graph.a_star('a', 'b', lambda v1, v2: 0)
        self.assertEqual(([], 0), actual)

        # (2) start/end vertex does not exist
        graph = Graph()
        graph.add_to_graph('a')
        # (2.1) start vertex
        actual = graph.a_star('b', 'a', lambda v1, v2: 0)
        self.assertEqual(([], 0), actual)
        # (2.2) end vertex
        actual = graph.a_star('a', 'b', lambda v1, v2: 0)
        self.assertEqual(([], 0), actual)

        # (3) test for path which does not exist
        graph = Graph()
        graph.add_to_graph('a', 'b')
        actual = graph.a_star('b', 'a', lambda v1, v2: 0)
        self.assertEqual(([], 0), actual)

        # === (A) Grid graph tests ===#
        graph = Graph()

        # (4) test on nxn grid from corner to corner: should shoot diagonal
        # (the shortest path is unique, so each heuristic will return the same path)
        grid_size = 5
        for x in range(grid_size):
            for y in range(grid_size):
                idx = f"{x},{y}"
                graph.vertices[idx] = Vertex(idx, x, y)
        for x in range(grid_size):
            for y in range(grid_size):
                if x < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x + 1},{y}", 1)
                    graph.add_to_graph(f"{x + 1},{y}", f"{x},{y}", 1)
                if y < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x},{y + 1}", 1)
                    graph.add_to_graph(f"{x},{y + 1}", f"{x},{y}", 1)
                if x < grid_size - 1 and y < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x + 1},{y + 1}", math.sqrt(2))
                    graph.add_to_graph(f"{x + 1},{y + 1}", f"{x},{y}", math.sqrt(2))

        for metric in [Vertex.euclidean_distance, Vertex.taxicab_distance]:
            actual = graph.a_star('0,0', '4,4', metric)
            self.assertEqual(['0,0', '1,1', '2,2', '3,3', '4,4'], actual[0])  # (4.1) actual path test
            self.assertAlmostEqual((grid_size - 1) * math.sqrt(2), actual[1])  # (4.2) distance test
            graph.reset_vertices()

        # (5) test on nxn grid with penalty for shooting diagonal
        # (the shortest path is not unique, so each heuristic will return a different path)
        for x in range(grid_size - 1):
            for y in range(grid_size - 1):
                graph.add_to_graph(f"{x},{y}", f"{x + 1},{y + 1}", 3)
                graph.add_to_graph(f"{x + 1},{y + 1}", f"{x},{y}", 3)

        actual = graph.a_star('0,0', '4,4', Vertex.euclidean_distance)
        self.assertEqual((['0,0', '1,0', '1,1', '2,1', '2,2', '3,2', '3,3', '4,3', '4,4'], 8),
                         actual)  # (5.1) euclidean
        graph.reset_vertices()
        actual = graph.a_star('0,0', '4,4', Vertex.taxicab_distance)
        self.assertEqual((['0,0', '1,0', '2,0', '3,0', '4,0', '4,1', '4,2', '4,3', '4,4'], 8), actual)  # (5.2) taxicab
        graph.reset_vertices()

    def test_a_star_large(self):

        # === (A) Tollway graph tests ===#
        graph = Graph(csvf='test_csvs/astar/tollway_graph_csv.csv')
        # now must set of coordinates for each vertex:
        positions = [(0, 0), (2, 0), (4, 0), (7, 0), (10, 0), (12, 0), (2, 5), (6, 4), (12, 5), (5, 9), (8, 8), (12, 8),
                     (8, 10), (0, 2),
                     (4, 2), (9, 2), (9, -2), (7, 6), (8, 11), (14, 8)]

        for index, v_id in enumerate(list(graph.vertices)):
            graph.vertices[v_id].x, graph.vertices[v_id].y = positions[index]

        # UMCOMMENT TO SEE PLOT
        # graph.plot_show = True
        # graph.plot()

        for metric in [Vertex.euclidean_distance, Vertex.taxicab_distance]:
            # (1) test Franklin Grove to Northbrook shortest path in both directions
            actual = graph.a_star('Franklin Grove', 'Northbrook', metric)
            expected = (['Franklin Grove', 'A', 'B', 'G', 'J', 'M', 'Northbrook'], 22)
            self.assertEqual(expected, actual)
            graph.reset_vertices()

            actual = graph.a_star('Northbrook', 'Franklin Grove', metric)
            expected = (['Northbrook', 'M', 'J', 'G', 'B', 'A', 'Franklin Grove'], 22)
            self.assertEqual(expected, actual)
            graph.reset_vertices()

            # (2) test Franklin Grove to Joliet shortest path - bypass expensive tollway path
            actual = graph.a_star('Franklin Grove', 'Joliet', metric)
            expected = (['Franklin Grove', 'A', 'B', 'G', 'H', 'D', 'E', 'Joliet'], 35)
            self.assertEqual(expected, actual)
            graph.reset_vertices()

            actual = graph.a_star('Joliet', 'Franklin Grove', metric)
            expected = (['Joliet', 'E', 'D', 'H', 'G', 'B', 'A', 'Franklin Grove'], 35)
            self.assertEqual(expected, actual)
            graph.reset_vertices()

            # (3) test Joliet to Chicago shortest path - bypass expensive tollway path
            actual = graph.a_star('Joliet', 'Chicago', metric)
            expected = (['Joliet', 'E', 'D', 'H', 'G', 'J', 'K', 'L', 'Chicago'], 35)
            self.assertEqual(expected, actual)
            graph.reset_vertices()

            actual = graph.a_star('Chicago', 'Joliet', metric)
            expected = (['Chicago', 'L', 'K', 'J', 'G', 'H', 'D', 'E', 'Joliet'], 35)
            self.assertEqual(expected, actual)
            graph.reset_vertices()

            # (4) test Northbrook to Belvidere - despite equal path lengths, A* heuristic will always prefer search to the left
            actual = graph.a_star('Northbrook', 'Belvidere', metric)
            expected = (['Northbrook', 'M', 'J', 'K', 'Belvidere'], 8)
            self.assertEqual(expected, actual)
            graph.reset_vertices()

            actual = graph.a_star('Belvidere', 'Northbrook', metric)
            expected = (['Belvidere', 'K', 'J', 'M', 'Northbrook'], 8)
            self.assertEqual(expected, actual)
            graph.reset_vertices()

        # === (B) Big pre-generated graph tests ===#
        vertices = []
        e_graph = Graph(csvf="test_csvs/astar/test_astar_2.csv")
        t_graph = Graph(csvf="test_csvs/astar/test_astar_3.csv")
        position = [('a', 93, 41), ('b', 21, 31), ('c', 80, 13), ('d', 82, 60), ('e', 59, 79),
                    ('f', 84, 43), ('g', 74, 92), ('h', 95, 53), ('i', 85, 55), ('j', 98, 90),
                    ('k', 78, 53), ('l', 5, 55), ('m', 69, 36), ('n', 67, 92), ('o', 76, 98),
                    ('p', 42, 52), ('q', 69, 85), ('r', 29, 95), ('s', 18, 40), ('t', 97, 79),
                    ('u', 76, 21), ('v', 10, 88), ('w', 74, 80), ('x', 45, 93), ('y', 35, 68),
                    ('z', 65, 89)]
        for s, x, y in position:
            vertices.append(Vertex(s, x, y))
            e_graph.vertices[s].x = x
            t_graph.vertices[s].x = x
            e_graph.vertices[s].y = y
            t_graph.vertices[s].y = y
            e_graph.size += 1
            t_graph.size += 1

        def is_valid_path(graph, search_result):
            path, dist = search_result
            eps = 10 ** -8  # estimator of float
            length = 0
            for i in range(len(path) - 1):
                begin, end = path[i], path[i + 1]
                edge = graph.get_edge_by_ids(begin, end)
                if edge is None:
                    return False  # path contains some edge not in the graph
                length += edge[2]
            return abs(length - dist) < eps  # path consists of valid edges: return whether length matches

        # (5) test all 26 x 26 pairwise A* traversals across random matrix and ensure they return valid paths w/o error
        for begin in vertices:
            for end in vertices:
                if begin != end:
                    actual = e_graph.a_star(begin.id, end.id, Vertex.euclidean_distance)
                    self.assertTrue(is_valid_path(e_graph, actual))
                    e_graph.reset_vertices()

                    actual = t_graph.a_star(begin.id, end.id, Vertex.taxicab_distance)
                    self.assertTrue(is_valid_path(t_graph, actual))
                    t_graph.reset_vertices()

    def test_application_problem(self):
        # 1 Test Empty
        graph = Graph()
        expected = ([], 0)
        coupon = (lambda x: x[0] == 'A', 0.5)
        self.assertEqual(expected, tollway_algorithm_again(graph, 'A', 'B', lambda v1, v2: 0, coupon))

        # 2 Test Missing Begin or End
        graph = Graph()
        graph.add_to_graph('A')
        expected = ([], 0)
        coupon = (lambda x: x[0] == "A", 0.5)
        actual = tollway_algorithm_again(graph, 'A', 'B', lambda v1, v2: 0, coupon)
        self.assertEqual(expected, actual)  # (2.1) Missing End
        actual = tollway_algorithm_again(graph, 'D', 'A', lambda v1, v2: 0, coupon)
        self.assertEqual(expected, actual)  # (2.2) Missing Start

        # 3 Testing Small Graph(Small Tollway at South Campus) with coupon that do nothing
        graph = Graph()
        # Updating location for metric
        graph.vertices['Wilson Hall'] = Vertex('Wilson Hall', 0, 0)
        graph.vertices['Wonder Hall'] = Vertex('Wonder Hall', 0, 1)
        graph.vertices['Case Hall'] = Vertex('Case Hall', 2, 2)
        graph.vertices['STEM'] = Vertex('STEM', 4, 4)
        graph.vertices['Engineer Building'] = Vertex('Engineer Building', 5, 5)

        graph.add_to_graph('Wilson Hall', 'Wonder Hall', 2)
        graph.add_to_graph('Wilson Hall', 'Case Hall', 4)
        graph.add_to_graph('Wonder Hall', 'STEM', 8)
        graph.add_to_graph('Wonder Hall', 'Engineer Building', 10)
        graph.add_to_graph('Case Hall', 'Engineer Building', 8)
        graph.add_to_graph('STEM', 'Engineer Building', 3)
        coupon = (lambda x: False, 1)
        expected = (['Wilson Hall', 'Wonder Hall', 'Engineer Building'], 12)
        actual = tollway_algorithm_again(graph, 'Wilson Hall', 'Engineer Building', lambda v1, v2: 0, coupon)
        self.assertEqual(expected, actual)  # (3.1) Only one path available

        expected = (['Wilson Hall', 'Case Hall', 'Engineer Building'], 12)
        actual = tollway_algorithm_again(graph, 'Wilson Hall', 'Engineer Building', Vertex.taxicab_distance, coupon)
        self.assertEqual(expected, actual)  # (3.2) Using taxicab, 'C' is closer to 'E'

        # 4 Testing Small Graph(Small Tollway at South Campus) with various coupon
        graph = Graph()
        # Updating location for metric
        graph.vertices['Wilson Hall'] = Vertex('Wilson Hall', 0, 0)
        graph.vertices['Wonder Hall'] = Vertex('Wonder Hall', 0, 1)
        graph.vertices['Case Hall'] = Vertex('Case Hall', 2, 2)
        graph.vertices['STEM'] = Vertex('STEM', 4, 4)
        graph.vertices['Engineer Building'] = Vertex('Engineer Building', 5, 5)

        graph.add_to_graph('Wilson Hall', 'Wonder Hall', 2)
        graph.add_to_graph('Wilson Hall', 'Case Hall', 4)
        graph.add_to_graph('Wonder Hall', 'STEM', 8)
        graph.add_to_graph('Wonder Hall', 'Engineer Building', 10)
        graph.add_to_graph('Case Hall', 'Engineer Building', 8)
        graph.add_to_graph('STEM', 'Engineer Building', 3)
        free_pass_stem = (lambda v_id: v_id == "STEM", 0)
        expected = (['Wilson Hall', 'Wonder Hall', 'STEM', 'Engineer Building'], 10)
        graph.plot_show = True
        graph.plot()
        actual = tollway_algorithm_again(graph, 'Wilson Hall', 'Engineer Building',
                                         Vertex.taxicab_distance, free_pass_stem)
        self.assertEqual(expected, actual)  # (4.1) Useful coupon that making lower cost

        STEM_pass = (lambda v_id: v_id == "STEM", 0.8)
        expected = (['Wilson Hall', 'Case Hall', 'Engineer Building'], 12)
        actual = tollway_algorithm_again(graph, 'Wilson Hall', 'Engineer Building',
                                         Vertex.taxicab_distance, STEM_pass)
        self.assertEqual(expected, actual)  # (4.2) Coupon isn't useful, so returning the same path

        free_coupon_every_where = (lambda v_id: True, 0.5)
        expected = (['Wilson Hall', 'Case Hall', 'Engineer Building'], 6)
        actual = tollway_algorithm_again(graph, 'Wilson Hall', 'Engineer Building',
                                         Vertex.taxicab_distance, free_coupon_every_where)
        self.assertEqual(expected, actual)  # (4.3) Every road reduce by half coupons

        double_cost_all = (lambda v_id: True, 2)
        expected = (['Wilson Hall', 'Case Hall', 'Engineer Building'], 12)
        actual = tollway_algorithm_again(graph, 'Wilson Hall', 'Engineer Building',
                                         Vertex.taxicab_distance, double_cost_all)
        self.assertEqual(expected, actual)  # (4.3) Terrible coupon, don't use it at all

        # 5. Tollway Graph test (The big one)
        graph = Graph(csvf="test_csvs/astar/tollway_graph_csv.csv")
        # now must set of coordinates for each vertex:
        positions = [(0, 0), (2, 0), (4, 0), (7, 0), (10, 0), (12, 0), (2, 5), (6, 4), (12, 5), (5, 9), (8, 8), (12, 8),
                     (8, 10), (0, 2),
                     (4, 2), (9, 2), (9, -2), (7, 6), (8, 11), (14, 8)]

        for index, v_id in enumerate(list(graph.vertices)):
            graph.vertices[v_id].x, graph.vertices[v_id].y = positions[index]

        for metric in [Vertex.euclidean_distance, Vertex.taxicab_distance]:
            # (5.1) test Franklin Grove to Northbrook shortest path in both directions
            # coupons will reduce the cost of path
            coupon_short_name = (lambda v_id: len(v_id) <= 5, 0.5)
            expected = (['Northbrook', 'M', 'J', 'G', 'B', 'A', 'Franklin Grove'], 11.0)
            actual = tollway_algorithm_again(graph, 'Northbrook', 'Franklin Grove',
                                             metric, coupon_short_name)
            self.assertEqual(expected, actual)  # (5.1.1)

            free_pass_short_name = (lambda v_id: len(v_id) <= 2, 0)
            expected = (['Franklin Grove', 'A', 'B', 'G', 'J', 'M', 'Northbrook'], 0)
            actual = tollway_algorithm_again(graph, 'Franklin Grove', 'Northbrook',
                                             metric, free_pass_short_name)
            self.assertEqual(expected, actual)  # (5.1.2)

            # (5.2) test Northbrook to Belvidere - despite equal path lengths,
            # A* heuristic will always prefer search to the left
            good_coupon = (lambda v_id: v_id in ['A', 'J', 'K'], 0.5)
            expected = (['Northbrook', 'M', 'J', 'K', 'Belvidere'], 6.0)
            actual = tollway_algorithm_again(graph, 'Northbrook', 'Belvidere',
                                             metric, good_coupon)
            self.assertEqual(expected, actual)  # (5.2.1)

            better_coupon = (lambda v_id: v_id in ['A', 'J', 'K'], 0.2)
            expected = (['Belvidere', 'K', 'J', 'M', 'Northbrook'], 1.6)
            actual = tollway_algorithm_again(graph, 'Belvidere', 'Northbrook',
                                             metric, better_coupon)
            self.assertEqual(expected, actual)  # (5.2.2)

    """
    End Graph Part 2 Tests
    """


if __name__ == '__main__':
    unittest.main()
