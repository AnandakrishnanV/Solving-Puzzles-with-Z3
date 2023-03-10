# Solving-Puzzles-with-Z3
Project for CS5232

Place numbers in some of the empty cells so that in total each of the four 7-by-7 outlined grids is a legal “Twenty Four Seven” grid. Namely: each 7-by-7 grid’s interior should contain one 1, two 2’s, etc., up to seven 7’s. Furthermore, each row and column within the 7-by-7’s must contain exactly 4 numbers which sum to 20. Finally, the numbered cells must form a connected region, but every 2-by-2 subsquare in the completed grid must contain at least one empty cell.

Some numbers have been placed inside the grid. Additionally, some blue numbers have been placed outside the grid. A number outside the grid represents either the sum of the row or column it is facing, or the value of the first number it sees in that row or column.

Once completed, you can submit as your answer the product of the areas of the connected groups of orthogonally adjacent empty squares in the grid.



### TODO 
- [ ] 12x12 grid in total
- [ ] 7x7 grid division 
- [ ] In each 7x7 grid, 
  - [ ] have to have 1x1, 2x2, 3x3, ....., 7x7
  - [ ] must contain exactly 4 numbers that sum to 20
  - [ ] Enforce the blue number, where it could be the sum or the first number
- [ ] Each 2x2 subsquare must have at least one empty cell
- [ ] Numbered cells must form a connected region
- [ ] Multiply the result