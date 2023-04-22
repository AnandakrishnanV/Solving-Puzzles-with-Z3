# Solving-Puzzles-with-Z3
Project for CS5232
The project aims to explore the use of the Z3 SMT theorem prover in solving complex mathematical puzzles. The mathematical puzzle chosen by the team is the Twenty-Four Seven puzzle and its variations. The chosen puzzle ‘Twenty-Four Seven (Four-in-One)’ is a complex sudoku variant that involves finding the correct set of numbers that satisfies the 12-by-12 grid, keeping in line with the constraints provided

Place numbers in some of the empty cells so that in total each of the four 7-by-7 outlined grids is a legal “Twenty Four Seven” grid. Namely: each 7-by-7 grid’s interior should contain one 1, two 2’s, etc., up to seven 7’s. Furthermore, each row and column within the 7-by-7’s must contain exactly 4 numbers which sum to 20. Finally, the numbered cells must form a connected region, but every 2-by-2 subsquare in the completed grid must contain at least one empty cell.

Some numbers have been placed inside the grid. Additionally, some blue numbers have been placed outside the grid. A number outside the grid represents either the sum of the row or column it is facing, or the value of the first number it sees in that row or column.

Once completed, you can submit as your answer the product of the areas of the connected groups of orthogonally adjacent empty squares in the grid.

### Breakdown 
- [x] 12x12 grid in total
- [x] 7x7 grid division
- [x] In each 7x7 grid, 
  - [x] have to have 1x1, 2x2, 3x3, ....., 7x7
  - [x] must contain exactly 4 numbers that sum to 20
  - [x] Enforce the blue number, where it could be the sum or the first number
- [x] Each 2x2 subsquare must have at least one empty cell
- [x] Numbered cells must form a connected region
- [x] Identify empty connected regions, count number of cells in each region
- [x] Multiply the result

### Setup-Instructions
The 4 different question identified by team, of 3 different variations can be solved using their respective python impelmentation. All solvers should output their solutions within a few seconds. All are python files and can be run from the terminal.  The simple generator is currently configured to only generate a single 7x7 grid, owning to time constraints associated with the connected region constraint. You may have to run it a few times to receive a satisfiable output problem as the connected region condition can only be enfoced through multiple iterations, we have currently set the value to be either 1 or 2 connected regions for a faster output time, and can be changed in the generator file. Estimated average time is around 1-2 minutes.
