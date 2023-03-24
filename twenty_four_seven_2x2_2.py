# Jane Street: December 2020
# Twenty Four Seven 2-by-2 #2

# Each of the grids above is incomplete. Place numbers in some of the empty cells so that in total 
# each grid’s interior contains one 1, two 2’s, etc., up to seven 7’s. Furthermore, each row and column 
# within each grid must contain exactly 4 numbers which sum to 20. Finally, the numbered cells must form 
# a connected region, but every 2-by-2 subsquare in the completed grid must contain at least one empty cell.

# Some numbers have been placed inside each grid. Additionally, some blue numbers have been placed outside of 
# the grids. These blue numbers indicate the first value seen in the corresponding row or column when looking 
# into the grid from that location.

# Once each of the grids is complete, create a 7-by-7 grid by “adding” the four grids’ interiors together 
# (as if they were 7-by-7 matrices). The answer to this month’s puzzle is the sum of the squares of the values in this final grid.


tfs_array_one = (
    (0, 0, 4, 0, 0, 0, 0),
    (0, 0, 0, 6, 0, 0, 0),
    (5, 0, 0, 0, 0, 0, 0),
    (0, 3, 0, 0, 0, 6, 0),
    (0, 0, 0, 0, 0, 0, 2),
    (0, 0, 0, 1, 0, 0, 0),
    (0, 0, 0, 0, 4, 0, 0),
)

rc_left_one = [5, 7, 0, 0, 0, 5, 7]
rc_right_one = [7, 4, 0, 0, 0, 7, 6]

cc_top_one = [5, 4, 0, 0, 0, 7, 5]
cc_bottom_one = [5, 7, 0, 0, 0, 3, 6]

tfs_array_two = (
    (0, 2, 0, 0, 0, 0, 0),
    (2, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 3, 0),
    (0, 0, 0, 0, 3, 0, 0),
    (0, 0, 0, 3, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 1),
)

rc_left_two = [0, 0, 5, 6, 0, 7, 6]
rc_right_two = [6, 6, 4, 0, 0, 0, 0]

cc_top_two = [0, 0, 5, 6, 0, 6, 7]
cc_bottom_two = [6, 7, 5, 0, 0, 0, 0]

tfs_array_three = (
    (0, 0, 0, 0, 4, 0, 0),
    (0, 6, 0, 0, 0, 0, 0),
    (4, 0, 0, 0, 0, 0, 6),
    (0, 0, 0, 0, 0, 0, 0),
    (6, 0, 0, 0, 0, 0, 4),
    (0, 0, 0, 0, 0, 6, 0),
    (0, 0, 4, 0, 0, 0, 0),
)

rc_left_three = [0, 0, 0, 7, 0, 0, 0]
rc_right_three = [0, 0, 0, 5, 0, 0, 0]

cc_top_three = [7, 0, 0, 5, 0, 7, 0]
cc_bottom_three = [0, 7, 0, 3, 0, 0, 5]

tfs_array_four = (
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 3),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 4, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 3, 0, 0, 0, 0),
)

rc_left_four = [1, 2, 3, 4, 5, 6, 7]
rc_right_four = [0, 6, 0, 4, 0, 2, 0]

cc_top_four = [0, 0, 0, 0, 0, 0, 0]
cc_bottom_four = [0, 6, 0, 5, 0, 4, 0]