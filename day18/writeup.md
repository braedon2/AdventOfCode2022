# Part 2

The idea is to represent the air as a graph.
Computing breadth-first-search on the graph starting at an air-node that is
on the outside of the lava object will show which air-nodes can be reached.
Any air-node that is not reached by this search is part of an air pocket.

Consider the maximum and minumum x, y, z values of the input points.
Call these min_x, min_y, min_z, max_x, max_y, max_z.
Now consider all the points within the inclusive bounds `\[min_x - 1, max_x + 1\]`,
`\[min_y - 1, max_y + 1\]`, and `\[min_z - 1, max_z + 1\]`.
The set-difference between these points and the puzle input represents all the air around 
the lava. Representing these points as a graph and starting breadth-first-search starting
at `(min_x - 1, min_y - 1, min_z - 1)` will reveal what air is reachable from the outside
and what is part of an air-pocket.

