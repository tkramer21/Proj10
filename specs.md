Project 10: Graphs Continue
=========================

**Due: Friday, Dec 9 @ 10:00 pm**

_This is not a team project, do not copy someone else’s work._

_This project is created by  Tanawan Premsri, Brooke Osterkamp, Andrew Haas, Andrew McDonald_

## Assignment Overview

### What is A* Search?

Instead of searching the "next closest" vertex as is done in Dijkstra's algorithm, [A\* Search](https://en.wikipedia.org/wiki/A*_search_algorithm) (A-Star Search) picks the vertex which is "next closest to the goal" by weighting vertices more cleverly.

Recall that in Dijkstra's algorithm, vertices are stored in a priority queue with a priority key equal to the current shortest path to that vertex. If we denote the current shortest path to a vertex *V* by **g(v)**, then on each iteration of Dijkstra's algorithm, we search on the vertex with **min(g(v)).**

A* search takes the same approach to selecting the next vertex, but instead of setting the priority key of a vertex equal to **g(v)** and selecting **min(g(v))**, it uses the value **f(v)** and selects the vertex with **min(f(v))** where

**f(v) = g(v) + h(v)**

**\= current\_shortest\_path\_to\_v + estimated\_distance\_between\_v\_and\_target**

### In English, Please...

A* Search prioritizes vertices *V* to search based on the value **f(v)**, which is the sum of

*   **g(v)**, or the current shortest known path to vertex *V*, and
*   **h(v)**, which is the estimated (Euclidean or Taxicab) distance between the vertex *V* and the target vertex you're searching for

The result is that A* prioritizes vertices to search that (1) are _close to the origin along a known path_ AND which (2) are _in the right direction towards the target._ Vertices with a small **g(v)** are _close to the origin along a known path_ and vertices with a small **h(v)** are _in the right direction towards the target**,**_ so we pick vertices with the smallest sum of these two values.

[We strongly recommend you watch this video to build your intuition behind A\* Search!](https://www.youtube.com/watch?v=ySN5Wnu88nE)

A* is extremely versatile. Here we use Euclidean and Taxicab distances to prioritize certain directions of search, but note that any [metric](https://en.wikipedia.org/wiki/Metric_(mathematics)#Definition) **h(v, target)** could be used should the need arise. See [here](http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html) for more information on situations where different metrics may be practical.\]

![AStarGif.gif](https://s3.amazonaws.com/mimirplatform.production/files/002f64b5-cafa-4531-8dc8-e56f0e0de6e6/AStarGif.gif)

Assignment Notes
----------------

*   A plotting function is provided to help you visualize the progression of various search algorithms
    *   Be sure to read the specs explaining **plot()**
    *   If you don't want to use it, just comment out the related import statements and **plot()** function
*   Python allows representation of the value infinity using **float('inf')**
*   No negative edge weights will ever be added to the graph
    *   All edge weights are numeric values greater than or equal to zero
*   Time complexities are specified in terms of *V* and *E*, where *V* represents the number of vertices in the graph and *E* represents the number of edges in a graph
    *   Recall that E is bounded above by *V*^2; a graph has *E* = *V*^2 edges if and only if every vertex is connected to every other vertex
*   Recall that **list.insert(0, element)** and **list.pop(0)** are both _O(N)_ calls on a Python list
    *   Recall that python's 'lists' are not lists in the more common sense of the word: linked lists. They are dynamically managed tuples, stored in memory as contiguous arrays of pointers to elements elsewhere in memory. This allows indexing into a 'list' in constant time. The downside of this, however, is that adding to a python 'list' at a specific index, _i,_ requires shifting the pointer to every element past _i_ by one in the underlying array: a linear operation.
    *   Be careful when implementing **dijkstra, astar,** and the Application Problem to ensure you do not break time complexity by popping or inserting from the front of a list when reconstructing a path
    *   Instead of inserting into / popping from the front of the list, simply append to or pop from the end, then reverse the list _once_ at the end
        *   If you have N calls to **list.insert(0, element)**, that is _O(N^2)_
        *   If you instead have N calls to **list.append(element)**, followed by a single call to **list.reverse()**, that is _O(N)_
        *   Both methods will result in the same list being constructed, but the second is far more efficient

## Assignment Specifications

### class Vertex

Represents a vertex object, the building block of a graph.

**_DO NOT MODIFY the following attributes/functions_**

*   **Attributes**
    *   **id:** A string used to uniquely identify a vertex
    *   **adj:** A dictionary of type **{other\_id : number}** which represents the connections of a vertex to other vertices; the existence of an entry with key **other\_i****d** indicates connection from this vertex to the vertex with id **other\_id** by an edge with weight **number**
        *   Note that as of Python 3.7, [insertion ordering](https://stackoverflow.com/a/57072435) in normal dictionaries is guaranteed and ensures traversals will select the next neighbor to visit deterministically
    *   **visited:** A boolean flag used in search algorithms to indicate that the vertex has been visited
    *   **x:** The x-position of a vertex (used in assignment) (defaults to zero)
    *   **y:** The y-position of a vertex (used in assignment) (defaults to zero)
*   **\_\_init\_\_(self, idx: str, x: float=0, y: float=0) -> None:**  
    *   Constructs a Vertex object
*   **\_\_eq\_\_(self, other: Vertex) -> bool:**
    *   Compares this vertex for equality with another vertex
*   **\_\_repr\_\_(self) -> str:**
    *   Represents the vertex as a string for debugging
*   **\_\_str\_\_(self) -> str:**
    *   Represents the vertex as a string for debugging
*   **\_\_hash\_\_(self) -> int:**
    *   Allows the vertex to be hashed into a set; used in unit tests

**_USE the following function however you'd like_**

*   **deg(self) -> int:**
    *   Returns the number of outgoing edges from this vertex; i.e., the outgoing degree of this vertex
    *   _Time Complexity: O(1)_
    *   _Space Complexity: O(1)_
*   **get\_outgoing\_edges(self) -> Set\[Tuple\[str, float\]\]:**
    *   Returns a **set** of tuples representing outgoing edges from this vertex
    *   Edges are represented as tuples **(other\_id, weight)** where
        *   **other\_id** is the unique string id of the destination vertex
        *   **weight** is the weight of the edge connecting this vertex to the other vertex
    *   Returns an empty set if this vertex has no outgoing edges
    *   _Time Complexity: O(degV)_
    *   _Space Complexity: O(degV)_
*   **euclidean\_distance(self, other: Vertex) -> float:**
    *   Returns the [euclidean distance](http://rosalind.info/glossary/euclidean-distance/) \[based on two-dimensional coordinates\] between this vertex and vertex **other**
    *   Used in AStar
    *   _Time Complexity: O(1)_
    *   _Space Complexity: O(1)_
*   **taxicab\_distance(self, other: Vertex) -> float:**
    *   Returns the [taxicab distance](https://en.wikipedia.org/wiki/Taxicab_geometry) \[based on two-dimensional coordinates\] between this vertex and vertex **other**
    *   Used in AStar
    *   _Time Complexity: O(1)_
    *   _Space Complexity: O(1)_

### class Graph

Represents a graph object

**_DO NOT MODIFY the following attributes/functions_**

* **Attributes**
    *   **size:** The number of vertices in the graph
    *   **vertices:** A dictionary of type **{id : Vertex}** storing the vertices of the graph, where **id** represents the unique string id of a **Vertex** object
        *   Note that as of Python 3.7, [insertion ordering](https://stackoverflow.com/a/57072435) in normal dictionaries is guaranteed and ensures **get\_edges(self)** and **get\_vertices(self)** will return deterministically ordered lists
    *   **plot\_show**: If true, calls to **plot()** display a rendering of the graph in matplotlib; if false, all calls to **plot()** are ignored (see **plot()** below)
    *   **plot\_delay**: Length of delay in **plot()** (see **plot()** below)
* **\_\_init\_\_(self, plt\_show: bool=False) -> None:**  
    *   Constructs a Graph object
    *   Sets **self.plot\_show** to False by default
* **\_\_eq\_\_(self, other: Graph) -> bool:**
    *   Compares this graph for equality with another graph
* **\_\_repr\_\_(self) -> str:**
    *   Represents the graph as a string for debugging
* **\_\_str\_\_(self) -> str:**
    *   Represents the graph as a string for debugging
* **add\_to\_graph(self, start\_id: str, dest\_id: str=None, weight: float=0) -> float:**
    *   Adds a vertex / vertices / edge to the graph
        *   Adds a vertex with id **start\_id** to the graph if no such vertex exists
        *   Adds a vertex with id **dest\_id** to the graph if no such vertex exists and **dest\_id** is not None
        *   Adds an edge with weight **weight** if **dest\_id** is not None
    *   If a vertex with id **start\_id** or **dest\_id** already exists in the graph, this function will not overwrite that vertex with a new one
    *   If an edge already exists from vertex with id **start\_id** to vertex with id **dest\_id**, this function will overwrite the weight of that edge
* **matrix2graph(self, matrix: Matrix) -> None:**
    *   Constructs a graph from a given adjacency matrix representation
    *   **matrix** is guaranteed to be a square 2D list (i.e. list of lists where # rows = # columns), of size **\[V+1\]** x **\[V+1\]**
        *   **matrix\[0\]\[0\]** is None
        *   The first row and first column of **matrix** hold string ids of vertices to be added to the graph and are symmetric, i.e. **matrix\[i\]\[0\] = matrix\[0\]\[i\]** for i = 1, ..., n
        *   **matrix\[i\]\[j\]** is None if no edge exists from the vertex **matrix\[i\]\[0\]** to the vertex **matrix\[0\]\[j\]**
        *   **matrix\[i\]\[j\]** is a **number** if an edge exists from the vertex **matrix\[i\]\[0\]** to the vertex **matrix\[0\]\[j\]** with weight **number**
* **graph2matrix(self) -> None:**
    *   Constructs and returns an adjacency matrix from a graph
    *   The output matches the format of matrices described in **matrix2graph**
    *   If the graph is empty, returns **None**
* **graph2csv(self, filepath: str) -> None:**
    *   Encodes the graph (if non-empty) in a csv file at the given location

* **reset\_vertices(self) -> None:**
    * Resets visited flags to False of all vertices within the graph
    * Used in unit tests to reset graphs between tests
    * Time Complexity: O(V)
    * Space Complexity: O(1)
* **get\_vertex\_by\_id(self, v\_id: str) -> Vertex:**
    * Returns the vertex object with id v_id if it exists in the graph
    * Returns None if no vertex with unique id v_id exists
    * Time Complexity: O(1)
    * Space Complexity: O(1)
* **get\_all\_vertices(self) -> Set\[Vertex\]:**
    * Returns a set of all Vertex objects held in the graph
    * Returns an empty set if no vertices are held in the graph
    * Time Complexity: O(V)
    * Space Complexity: O(V)
* **get\_edge\_by\_ids(self, begin\_id: str, end\_id: str) -> Tuple\[str, str, float\]:**
    * Returns the edge connecting the vertex with id begin_id to the vertex with id end_id in a tuple of the form (begin_id, end_id, weight)
    * If the edge or either of the associated vertices does not exist in the graph, returns None
    * Time Complexity: O(1)
    * Space Complexity: O(1)
* **get\_all\_edges(self) -> Set\[Tuple\[str, str, float\]\]:**
    * Returns a set of tuples representing all edges within the graph
    * Edges are represented as tuples (begin_id, end_id, weight) where
      * begin_id is the unique string id of the starting vertex
      * end_id is the unique string id of the starting vertex
      * weight is the weight of the edge connecting the starting vertex to the destination vertex
    * Returns an empty set if the graph is empty
    * Time Complexity: O(V+E)
    * Space Complexity: O(E)
* **build_path(self, back_edges: Dict\[str, str\], begin_id: str, end_id: str) -> Tuple[List[str], float]:**
    * Given a dictionary of back-edges (a mapping of vertex id to predecessor vertex id), reconstructs the path from start_id to end_id and computes the total distance
    * Returns tuple of the form (\[path\], distance) where
\[path\] is a list of vertex id strings beginning with begin_id, terminating with end_id, and including the ids of all intermediate vertices connecting the two
distance is the sum of the weights of the edges along the \[path\] traveled
    * Handle the cases where no path exists from vertex with id begin_id to vertex with end_id or if one of the vertices does not exist
    * Time Complexity: O(V)
    * Space Complexity: O(V)

**_USE the following function however you'd like_**

*   **plot(self) -> None:**
    *   Renders a visual representation of the graph using matplotlib and displays graphic in PyCharm
        *   [Follow this tutorial to install matplotlib and numpy if you do not have them](https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html), or follow the tooltip auto-suggested by PyCharm
    *   Provided for use in debugging
    *   If you call this in your searches and **self.****plot\_show** is true, the search process will be animated in successive plot renderings (with time between frames controlled by **self.plot\_delay**)
    *   Not tested in any testcases
        *   All testcase graphs are constructed with **self.plot\_show** set to False
    *   If vertices have (x,y) coordinates specified, they will be plotted at those locations
    *   If vertices do not have (x,y) coordinates specified, they will be plotted at a random point on the unit circle
    *   To install the necessary packages (matplotlib and numpy), follow the auto-suggestions provided by PyCharm
    *   **For any graph in test cases**, you can write following code to see the graph
        ```python
        graph.plot_show = True
        graph.plot()
        ```
    *   Vertices and edges are labeled; edges are color-coded by weight
        *   If a bi-directional edge exists between vertices, two color-coded weights will be displayed

![sample_plot.png](https://s3.amazonaws.com/mimirplatform.production/files/0aec2496-150a-4b85-b86f-142f235fe4ba/sample_plot.png)

*   **reset\_vertices(self) -> None:**
    *   Resets visited flags of all vertices within the graph
    *   Used in unit tests to reset graph between searches
    *   _Time Complexity: O(V)_
    *   _Space Complexity: O(V)_
*   **get\_vertex(self, vertex\_id: str) -> Vertex:**  
    *   Returns the Vertex object with id **vertex\_id** if it exists in the graph
    *   Returns None if no vertex with unique id **vertex\_id** exists
    *   _Time Complexity: O(1)_
    *   _Space Complexity: O(1)_
*   **get\_vertices(self) -> Set\[Vertex\]:**  
    *   Returns a **set** of all Vertex objects held in the graph
    *   Returns an empty set if no vertices are held in the graph
    *   _Time Complexity: O(V)_
    *   _Space Complexity: O(V)_
*   **get\_edge(self, start\_id: str, dest\_id: str) -> Tuple\[str, str, float\]:**  
    *   Returns the edge connecting the vertex with id **start\_id** to the vertex with id **dest\_id** in a tuple of the form **(start\_id, dest\_id, weight)**
    *   If the edge or either of the associated vertices does not exist in the graph, returns **None**
    *   _Time Complexity: O(1)_
    *   _Space Complexity: O(1)_
*   **get\_edges(self) -> Set\[Tuple\[str, str, float\]\]:**
    *   Returns a **set** of tuples representing all edges within the graph
    *   Edges are represented as tuples **(start\_id, other\_id, weight)** where
        *   **start\_id** is the unique string id of the starting vertex
        *   **other\_id** is the unique string id of the destination vertex
        *   **weight** is the weight of the edge connecting the starting vertex to the destination vertex
    *   Returns an empty set if the graph is empty
    *   _Time Complexity: O(V+E)_
    *   _Space Complexity: O(E)_

**_IMPLEMENT the following functions_**

*   **dijkstra(self, start\_id: str, target\_id: str) -> Tuple\[List\[str\], float\]:**
    *   Perform a dijkstra search beginning at vertex with id **start\_id** and terminating at vertex with id **end\_id**
    *   As you explore from each vertex, iterate over neighbors using **vertex.adj** (not vertex.get\_edges()) to ensure neighbors are visited in proper order
    *   Returns tuple of the form **(\[path\], distance)** where
        *   **\[path\]** is a list of vertex id strings beginning with **start\_id**, terminating with **end\_id**, and including the ids of all intermediate vertices connecting the two
        *   **distance** is the sum of the weights of the edges along the **\[path\]** traveled
    *   If no path exists from vertex with id **start\_id** to vertex with **end\_id** or if one of the vertices does not exist, returns tuple **(\[\],0)**
    *   Guaranteed that **start\_id != target\_id** (since that would be a trivial path)
    *   Because our adjacency maps use [insertion ordering](https://stackoverflow.com/a/57072435), neighbors will be visited in a deterministic order, and thus you do not need to worry about the order in which you visit neighbor vertices at the same depth
    *   Use the given AStarPriorityQueue class to simplify priority key updates in a search priority queue
    *   _Time Complexity: O((V + E) log V)_
    *   _Space Complexity: O(V)_
*   **a\_star(self, start\_id: str, target\_id: str, metric: Callable\[\[Vertex, Vertex\], float\]) -> Tuple\[List\[str\], float\]**
    * Perform an A\* search beginning at vertex with id **start\_id** and terminating at vertex with id **end\_id**
    * As you explore from each vertex, iterate over neighbors using **vertex.adj** (not vertex.get\_edges()) to ensure neighbors are visited in proper order
    * Use the **metric** parameter to estimate h(v), the remaining distance, at each vertex
        *   This is a callable parameter and will always be **Vertex.euclidean\_distance** or **Vertex.taxicab\_distance**
    * Returns tuple of the form **(\[path\], distance)** where
        *   **\[path\]** is a list of vertex id strings beginning with **start\_id**, terminating with **end\_id**, and including the ids of all intermediate vertices connecting the two
        *   **distance** is the sum of the weights of the edges along the **\[path\]** traveled
    * If no path exists from vertex with id **start\_id** to vertex with **end\_id** or if one of the vertices does not exist, returns tuple **(\[\],0)**
    * Guaranteed that **start\_id != target\_id** (since that would be a trivial path)
    * Recall that vertices are prioritized in increasing order of **f(v) = g(v) + h(v)**, where
        *   **g(v)** is the shortest known path to this vertex
        *   **h(v)** is the Euclidean distance from *V* to the target vertex
    * Use the given AStarPriorityQueue class to simplify priority key updates in a search priority queue
    * **Implementations of this function which do not utilize the heuristic metric will not receive any credit for automated and manual tests.**
        *   **Do not simply implement Dijkstra's Algorithm**
    * _Time Complexity: O((V + E)log(V))_
    * _Space Complexity: O(V)_

To simplify the operation of updating a priority key in your search priority queue, use the following given class.

### class PriorityQueue

_DO NOT MODIFY the following attributes/functions_

*   **Attributes**
    *   **data:** Underlying data list of priority queue
    *   **locator:** Dictionary to locate vertices within the priority queue
    *   **counter:** Used to break ties between vertices
*   **\_\_init\_\_(self)**  
    *   Constructs an AStarPriorityQueue object
*   **\_\_repr\_\_(self)**
    *   Represents the priority queue as a string for debugging
*   **\_\_str\_\_(self)**
    *   Represents the priority queue as a string for debugging
*   **empty(self)**
    *   Returns boolean indicating whether priority queue is empty
*   **push(self, priority, vertex)**  
    *   Push the **vertex** object onto the priority queue with a given **priority** key
    *   This priority queue has been specially designed to hold Vertex objects as values ranked by priority keys; be sure you push Vertex objects and NOT vertex id strings onto the queue
*   **pop(self)**  
    *   Visit, remove and return the Vertex object with the highest priority (i.e. lowest priority key) as a **(priority, vertex)** tuple
*   **update(self, new\_priority, vertex)**
    *   Update the priority of the **vertex** object in the queue to have a **new\_priority**

Application Problem
-------------------

After finishing your school year for the winter, you decide to take a vacation to the lovely 
toll-ridden city of Chicago-modeled by a road network with **v vertices and e edges.** After cleaning out your dorm room, you find you have **m EZ-pass coupons** to spend that cover the cost of **half of any toll segment**, i.e., you have m EZ-pass coupons which effectively set the toll of a road segment to HALF. After reading this, you realize that it's the same story as the last summer (Same story as Spring 22 project 10), and you don't want it to end up the same way. Since it's near Christmas, you make a wish to Santa Claus to have unlimited coupons.
Because of being wonderful programmer for entire year, Santa decides to give you mystery discount unlimited coupon. However, this coupon can be used in some specific cities that satisfy the particular condition.Your goal is to devise an algorithm to find a route from point **A** to point **B** on the toll roads of Chicago for the cheapest possible overall toll for your new winter vacation.

*   **tollways\_algorithm\_again(graph, start\_id: str, target\_id: str, coupon: Tuple(Callable\[\[str\], bool\], float), metric: metric: Callable\[\[Vertex, Vertex\], float\])**
    * Perform an toll algorithm beginning at vertex with id **start\_id** and terminating at vertex with id **target\_id**
    * This should still perform that A* algorithm to find the next path
    * Assume the distance between paths is the cost of going from one to another
    * As you explore from each vertex, iterate over neighbors using **vertex.adj** (not vertex.get\_edges()) to ensure neighbors are visited in proper order
    * The **coupon\[0\]** parameter to determine whatever to use coupon, **remember**, you can choose to not use coupon at all
    * The **coupon\[1\]** parameter to change cost to cost * coupon_discount
    * Returns tuple of the form **(\[path\], distance)** where
        *   **\[path\]** is a list of vertex id strings beginning with **start\_id**, terminating with **end\_id**, and including the ids of all intermediate vertices connecting the two
        *   **distance** is the sum of the weights of the edges along the **\[path\]** traveled
    * If no path exists from vertex with id **start\_id** to vertex with **end\_id** or if one of the vertices does not exist, returns tuple **(\[\],0)**
    * Guaranteed that **start\_id != target\_id** (since that would be a trivial path)
    * Use the given AStarPriorityQueue class to simplify priority key updates in a search priority queue
    * _Time Complexity: O((V + E) log(V))_
    * _Space Complexity: O(V)_
    

### Examples

Example 1:

![](img/APPEX1.png)

This corresponds to the test case:
```python
graph = Graph()
graph.add_to_graph('Wilson Hall', 'Wonder Hall', 2)
graph.add_to_graph('Wilson Hall', 'Case Hall', 4)
graph.add_to_graph('Wonder Hall', 'STEM', 8)
graph.add_to_graph('Wonder Hall', 'Engineer Building', 10)
graph.add_to_graph('Case Hall', 'Engineer Building', 8)
graph.add_to_graph('STEM', 'Engineer Building', 3)
coupon = (lambda x: False, 1)
expected = (['Wilson Hall', 'Wonder Hall', 'Engineer Building'], 12)
actual = tollway_algorithm_again(graph, 'Wilson Hall', 'Engineer Building', lambda v1, v2: 0, coupon)
self.assertEqual(expected, actual)  # (3.1) Only one shortest path available
```
Explanation: 

There is no vertices in the graph that satisfy coupon condition. Therefore, 
the shortest path from Wilson Hall to Engineer Building is Wilson Hall -> Wonder Hall -> Engineer Building with 12 costs

Example 2:

![](img/APPEX2.png)
This corresponds to the test case:
```python
graph = Graph()
graph.add_to_graph('Wilson Hall', 'Wonder Hall', 2)
graph.add_to_graph('Wilson Hall', 'Case Hall', 4)
graph.add_to_graph('Wonder Hall', 'STEM', 8)
graph.add_to_graph('Wonder Hall', 'Engineer Building', 10)
graph.add_to_graph('Case Hall', 'Engineer Building', 8)
graph.add_to_graph('STEM', 'Engineer Building', 3)
free_pass_stem = (lambda v_id: v_id == "STEM", 0)
expected = (['Wilson Hall', 'Wonder Hall', 'STEM', 'Engineer Building'], 10)
actual = tollway_algorithm_again(graph, 'Wilson Hall', 'Engineer Building',
                                 Vertex.taxicab_distance, free_pass_stem)
self.assertEqual(expected, actual)
```
Explanation: 

With using the free pass STEM coupon that reduced the cost of all road from STEM to 0, the new 
shortest path from Wilson Hall to Engineer Building is
Wilson Hall -> Wonder Hall -> STEM -> Engineer Building with cost of 10

Example 3:
![](img/APPEX3.png)


This corresponds to the test case:
```python
graph = Graph()
graph.add_to_graph('Wilson Hall', 'Wonder Hall', 2)
graph.add_to_graph('Wilson Hall', 'Case Hall', 4)
graph.add_to_graph('Wonder Hall', 'STEM', 8)
graph.add_to_graph('Wonder Hall', 'Engineer Building', 10)
graph.add_to_graph('Case Hall', 'Engineer Building', 8)
graph.add_to_graph('STEM', 'Engineer Building', 3)
double_cost_all = (lambda v_id: True, 2)
expected = (['Wilson Hall', 'Case Hall', 'Engineer Building'], 12)
actual = tollway_algorithm_again(graph, 'Wilson Hall', 'Engineer Building',
                                 Vertex.taxicab_distance, double_cost_all)
self.assertEqual(expected, actual)
```
Explanation: 

With given coupon that double the cost of all road, 
the shortest path from Wilson Hall to Engineer Building is the same as the first example since coupon is not being used.
The shortest path is Wilson Hall -> Case Hall -> Engineer Building with 12 costs.


### Here some music for you to help you with your coding.
* [Playlist: Splatoon](https://youtube.com/playlist?list=PLyyBMVVhBOc3VkRqPKdqx1eL4F2ymapDM)  

  
## **Submission**

#### **Deliverables**
In every project you will be given a file named as "**solution.py**". Your will work on this file to write your Python code.
We recommend that you **download your "solution.py" and "tests.py" to your local drive**, and work on your project using PyCharm so you can easily debug your code.

Below are the simple steps to work on any project locally in your personal computer in this class:

**APPROACH 1: USING D2L TO DOWNLOAD PROJECT'S STARTER PACKAGE:**
1. Make sure you installed PyCharm
2. You can download the starter package from D2L under Projects content. Watch the short tutorial video on how to download the starter package from D2L and open it up in PyCharm.
3. Work on your project as long as you want then upload your solution.py , (watch the short tutorial video on D2L for uploading your solution.py), and upload your solution.py to Codio.
4. Click Submit button on Guide when you are done!
![](img/Submit.png)

**APPROACH 2: USING CODIO TO DOWNLOAD solution.py and tests.py**
1. On your own computer make sure to create a local folder in your local drive, name it something like **ProjectXX**, replace xx with the actual project number, in this case your folder name would be **Project03**.
2. **Download** solution.py from Codio by simply right mouse clicking on the file tree, see image below
![](img/Codio_FileTree.png)
3. **Download** tests.py from Codio by simply right mouse clicking on the file tree as shown above.
4. Work locally using PyCharm as long as you need. 
5. When finished with your solution.py file, upload your file to Codio by right mouse clicking on the Project Directory on file tree.You should rename or remove the solution.py file that is currently existing in Codio before you upload your completed version. 
6. Go To Guide and click Submit button
![](img/Codio_Upload.png)


**It does not matter which approach you choose to work on your project, just be sure to upload your solution, “solution.py”, to Codio by and click on the Submit button by its deadline.**
Working locally is recommended so you can learn debugging. You can complete your entire solution.py using Codio editor, debugging may not as intuitive as PyCharm IDE. For this reason we recommend that you work locally as long as you need, then upload your code to Codio.


**Grading**
* **Auto Graded Tests (70 points)** see below for the point distribution for the auto graded tests:

      1.  dijkstra:               10 points
      2.  dijkstra_large:         10 points  
      3.  a_star:                 12 points
      4.  a_star_large:           13 points  
      5.  tollway_algorithm_again (application problem):       25 points  

* **Manual (30 points)**
- See the time complexity and auxiliary space requirement for each function listed below. 
- 
  * Loss of 1 point per missing docstring (max 5 point loss)
  * Loss of 2 points per changed function signature (max 20 point loss)
  
  Below is the list of manual points for the functions  

      1.  dijkstra:    \_\_/9 points
      2.  a_star:  \_\_/9 points
      3.  (application problem ):  \_\_/10 points (run time and space)
      4.  Feedback and citation. See text box below to complete.\_\_/2  points


* **Important reminder**
Note students can not use Chegg or similar sites, see syllabus for details, use of outside resources for the application problem is strictly forbidden, use of outside resources is limited to max of 2 functions in a project.


    * **DOCSTRING** is not provided for this project. Please use Project 1 as a template for your DOCSTRING . 
    To learn more on what is a DOCSTRING visit the following website: [What is Docstring?](https://peps.python.org/pep-0257/)
      * One point per function that misses DOCSTRING.
      * Up to 5 points of deductions

<input type="checkbox"> <b>STEP 1 :Rename the old solution file by clicking Rename button below. This button renames your file to **solution_old.py** </b>
{Rename}(mv solution.py solution_old.py)
<input type="checkbox"> <b>STEP 2 : Refresh your file tree by clicking on the refresh button under project name or refresh your browser. </b>

<input type="checkbox"> <b>STEP 3 : Upload your **solution.py** from your computer to Codio File Tree on the left. Refresh your file tree or browser to see if it actually updated the solution.py </b>


<input type="checkbox"> <b>STEP 4:Submit your code, by clicking the Submit button, you can submit as many times as you like, no limit on submission. 

Run button is removed. Run button was tied to tests.py in your file tree and in case of an update on tests.py , students who already started the work, would not see the update using the Run button.
Submit button is tied to tests.py in our secure folder, and it always gets the updated version of the tests.py. In case of any tests.py, students will always get the latest version to test their code through the submit button. In case of an update, the updated tests.py will be given through D2L or on Piazza so students can locally test it using their IDE. :</b>
{SUBMIT!|assessment}(test-3379255259)
Please note that there will be manual grading after you submit your work. Clicking Submit only runs the Auto-grader for the test cases. Manual Grading is 30 points in this project. (28 pts for Run Time and Space complexity, +2 points for filling out the feedback and the citation text box)


<input type="checkbox"> <b>STEP 5: Please make sure to **scroll all the way down on Guide Editor page**, Guide is the specs document, it is the document you are reading right now, scroll all the way down, and **click at the Mark as Completed button**, see below for the image of the button so you know what it looks like. Please scroll down and actually push the button. If you do not mark complete yourself, Codio will mark it at the end of the last penalty day, which will give 0 to your project. </b>
![](img/markcomplete.png)

{Check It!|assessment}(grade-book-3266829715)
{Submit Answer!|assessment}(free-text-3024451938)

















