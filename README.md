# Binary & Sudoku Solver

A clean, dependency-free web interface for entering and solving binary and
standard 9×9 Sudoku puzzles.

## Run the website

Open `index.html` directly, or serve the folder locally:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

The Binary mode supports even square boards from 4×4 through 16×16 and validates
all three standard binary-puzzle rules. Sudoku mode validates rows, columns, and
3×3 boxes. Both modes accept keyboard input, include an example, preserve the
original clues after solving, and can keep a camera/photo upload beside the grid
as a reference. Image recognition is intentionally not claimed: photographed
clues remain user-reviewed instead of silently inserting incorrect OCR results.
