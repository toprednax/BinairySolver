const gridElement = document.querySelector('#puzzleGrid');
const puzzleTypeSelect = document.querySelector('#puzzleType');
const sizeSelect = document.querySelector('#sizeSelect');
const boardDescription = document.querySelector('#boardDescription');
const statusElement = document.querySelector('#status');
const solveButton = document.querySelector('#solveButton');
const clearButton = document.querySelector('#clearButton');
const exampleButton = document.querySelector('#exampleButton');
const undoButton = document.querySelector('#undoButton');
const photoInput = document.querySelector('#photoInput');
const photoPreview = document.querySelector('#photoPreview');
const photoImage = document.querySelector('#photoImage');
const inputTip = document.querySelector('#inputTip');

let puzzleType = puzzleTypeSelect.value;
let size = Number(sizeSelect.value);
let board = [];
let originalBoard = null;

function blankBoard(n) {
  return Array.from({ length: n }, () => Array(n).fill(null));
}

function setStatus(message, type = '') {
  statusElement.textContent = message;
  statusElement.className = `status ${type}`;
}

function configureMode() {
  puzzleType = puzzleTypeSelect.value;
  const sudoku = puzzleType === 'sudoku';
  sizeSelect.disabled = sudoku;
  if (sudoku) sizeSelect.value = '9';
  else if (sizeSelect.value === '9') sizeSelect.value = '6';
  [...sizeSelect.options].forEach(option => { option.hidden = option.value === '9' ? !sudoku : sudoku; });
  inputTip.innerHTML = sudoku
    ? '<span>Tip</span> Type a number from <b>1</b> to <b>9</b>. Use Delete or Backspace to clear a square.'
    : '<span>Tip</span> Tap a square to cycle through <b>0</b>, <b>1</b>, and blank. On a keyboard, type 0 or 1 directly.';
  document.querySelector('#helpEyebrow').textContent = sudoku ? 'Sudoku rules' : 'Binary puzzle rules';
  document.querySelector('#helpTitle').textContent = sudoku ? 'Fill the grid using three constraints.' : 'Every row and column follows three rules.';
  document.querySelector('#binaryRules').hidden = sudoku;
  document.querySelector('#sudokuRules').hidden = !sudoku;
  buildGrid();
}

function buildGrid() {
  size = puzzleType === 'sudoku' ? 9 : Number(sizeSelect.value);
  board = blankBoard(size);
  originalBoard = null;
  gridElement.innerHTML = '';
  gridElement.className = `puzzle-grid ${puzzleType}`;
  gridElement.style.gridTemplateColumns = `repeat(${size}, 1fr)`;
  gridElement.setAttribute('aria-label', `${puzzleType === 'sudoku' ? 'Sudoku' : 'Binary puzzle'} grid`);
  undoButton.disabled = true;

  for (let row = 0; row < size; row++) {
    for (let col = 0; col < size; col++) {
      const cell = document.createElement('button');
      cell.type = 'button';
      cell.className = 'cell';
      cell.dataset.row = row;
      cell.dataset.col = col;
      cell.setAttribute('role', 'gridcell');
      cell.addEventListener('click', () => cycleCell(row, col));
      cell.addEventListener('keydown', event => keyboardCell(event, row, col));
      gridElement.appendChild(cell);
    }
  }
  renderBoard();
  setStatus('Board ready — enter the printed clues.');
}

function updateBoardDescription() {
  const clueBoard = originalBoard || board;
  const clueCount = clueBoard.flat().filter(value => value !== null).length;
  const name = puzzleType === 'sudoku' ? 'Sudoku' : `${size} × ${size} binary puzzle`;
  boardDescription.textContent = `${name} · ${clueCount} clue${clueCount === 1 ? '' : 's'} entered`;
}

function cycleCell(row, col) {
  if (originalBoard) restoreClues();
  if (puzzleType === 'binary') {
    const current = board[row][col];
    board[row][col] = current === null ? 0 : current === 0 ? 1 : null;
  } else {
    const current = board[row][col];
    board[row][col] = current === null ? 1 : current === 9 ? null : current + 1;
  }
  renderBoard();
}

function keyboardCell(event, row, col) {
  const validDigit = puzzleType === 'binary' ? /^[01]$/ : /^[1-9]$/;
  if (validDigit.test(event.key) || event.key === 'Backspace' || event.key === 'Delete') {
    event.preventDefault();
    if (originalBoard) restoreClues();
    board[row][col] = validDigit.test(event.key) ? Number(event.key) : null;
    renderBoard();
    return;
  }
  const movement = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1] }[event.key];
  if (movement) {
    event.preventDefault();
    const nextRow = (row + movement[0] + size) % size;
    const nextCol = (col + movement[1] + size) % size;
    gridElement.querySelector(`[data-row="${nextRow}"][data-col="${nextCol}"]`).focus();
  }
}

function renderBoard(invalidCells = new Set()) {
  [...gridElement.children].forEach(cell => {
    const row = Number(cell.dataset.row);
    const col = Number(cell.dataset.col);
    const value = board[row][col];
    cell.textContent = value ?? '';
    cell.className = 'cell';
    if (invalidCells.has(`${row},${col}`)) cell.classList.add('invalid');
    else if (originalBoard && originalBoard[row][col] === null && value !== null) cell.classList.add('solved');
    else if (value !== null) cell.classList.add('clue');
    cell.setAttribute('aria-label', `Row ${row + 1}, column ${col + 1}, ${value ?? 'blank'}`);
  });
  updateBoardDescription();
}

function getColumn(grid, col) { return grid.map(row => row[col]); }

function binaryLineValid(line) {
  const zeroes = line.filter(value => value === 0).length;
  const ones = line.filter(value => value === 1).length;
  const triple = line.some((value, index) => index > 1 && value !== null && value === line[index - 1] && value === line[index - 2]);
  return zeroes <= size / 2 && ones <= size / 2 && !triple;
}

function duplicateCompleteLine(lines, line) {
  if (line.includes(null)) return false;
  return lines.some(other => other !== line && !other.includes(null) && other.every((value, index) => value === line[index]));
}

function binaryBoardValid(grid) {
  const rows = grid;
  const cols = Array.from({ length: size }, (_, col) => getColumn(grid, col));
  if (![...rows, ...cols].every(binaryLineValid)) return false;
  return [rows, cols].every(lines => lines.every((line, index) => !duplicateCompleteLine(lines.filter((_, i) => i !== index), line)));
}

function sudokuUnits(grid) {
  const units = [...grid, ...Array.from({ length: 9 }, (_, col) => getColumn(grid, col))];
  for (let boxRow = 0; boxRow < 3; boxRow++) {
    for (let boxCol = 0; boxCol < 3; boxCol++) {
      const box = [];
      for (let row = boxRow * 3; row < boxRow * 3 + 3; row++)
        for (let col = boxCol * 3; col < boxCol * 3 + 3; col++) box.push(grid[row][col]);
      units.push(box);
    }
  }
  return units;
}

function sudokuBoardValid(grid) {
  return sudokuUnits(grid).every(unit => {
    const values = unit.filter(value => value !== null);
    return values.every(value => Number.isInteger(value) && value >= 1 && value <= 9) && new Set(values).size === values.length;
  });
}

function boardValid(grid) { return puzzleType === 'sudoku' ? sudokuBoardValid(grid) : binaryBoardValid(grid); }

function findConflicts(grid) {
  const conflicts = new Set();
  if (puzzleType === 'binary') {
    for (let row = 0; row < size; row++) if (!binaryLineValid(grid[row])) for (let col = 0; col < size; col++) conflicts.add(`${row},${col}`);
    for (let col = 0; col < size; col++) if (!binaryLineValid(getColumn(grid, col))) for (let row = 0; row < size; row++) conflicts.add(`${row},${col}`);
    for (const [lines, columns] of [[grid, false], [Array.from({ length: size }, (_, col) => getColumn(grid, col)), true]]) {
      for (let first = 0; first < size; first++) for (let second = first + 1; second < size; second++) {
        if (!lines[first].includes(null) && lines[first].every((value, index) => value === lines[second][index])) {
          for (let index = 0; index < size; index++) {
            conflicts.add(columns ? `${index},${first}` : `${first},${index}`);
            conflicts.add(columns ? `${index},${second}` : `${second},${index}`);
          }
        }
      }
    }
    return conflicts;
  }
  const markDuplicates = cells => {
    const byValue = new Map();
    for (const [row, col] of cells) {
      const value = grid[row][col];
      if (value === null) continue;
      if (!byValue.has(value)) byValue.set(value, []);
      byValue.get(value).push([row, col]);
    }
    for (const positions of byValue.values()) if (positions.length > 1) for (const [row, col] of positions) conflicts.add(`${row},${col}`);
  };
  for (let index = 0; index < 9; index++) {
    markDuplicates(Array.from({ length: 9 }, (_, col) => [index, col]));
    markDuplicates(Array.from({ length: 9 }, (_, row) => [row, index]));
  }
  for (let boxRow = 0; boxRow < 3; boxRow++) for (let boxCol = 0; boxCol < 3; boxCol++) {
    const cells = [];
    for (let row = boxRow * 3; row < boxRow * 3 + 3; row++) for (let col = boxCol * 3; col < boxCol * 3 + 3; col++) cells.push([row, col]);
    markDuplicates(cells);
  }
  return conflicts;
}

function candidates(grid, row, col) {
  const possible = [];
  const values = puzzleType === 'sudoku' ? [1, 2, 3, 4, 5, 6, 7, 8, 9] : [0, 1];
  for (const value of values) {
    grid[row][col] = value;
    if (boardValid(grid)) possible.push(value);
  }
  grid[row][col] = null;
  return possible;
}

function solve(grid) {
  let best = null;
  let bestOptions = null;
  for (let row = 0; row < size; row++) for (let col = 0; col < size; col++) {
    if (grid[row][col] !== null) continue;
    const options = candidates(grid, row, col);
    if (!options.length) return false;
    if (!bestOptions || options.length < bestOptions.length) {
      best = [row, col];
      bestOptions = options;
      if (options.length === 1) break;
    }
  }
  if (!best) return boardValid(grid);
  const [row, col] = best;
  for (const value of bestOptions) {
    grid[row][col] = value;
    if (solve(grid)) return true;
  }
  grid[row][col] = null;
  return false;
}

function solvePuzzle() {
  if (originalBoard) return;
  if (!board.flat().some(value => value !== null)) {
    setStatus('Enter at least one clue before solving.', 'error');
    return;
  }
  const conflicts = findConflicts(board);
  if (conflicts.size || !boardValid(board)) {
    renderBoard(conflicts);
    setStatus(`Some clues already break the ${puzzleType === 'sudoku' ? 'Sudoku' : 'binary puzzle'} rules.`, 'error');
    return;
  }
  originalBoard = board.map(row => [...row]);
  const working = board.map(row => [...row]);
  if (!solve(working)) {
    originalBoard = null;
    setStatus('This set of clues has no valid solution. Check the entered numbers.', 'error');
    return;
  }
  board = working;
  undoButton.disabled = false;
  renderBoard();
  setStatus('Solved. Your original clues remain in the lighter squares.', 'success');
}

function restoreClues() {
  if (!originalBoard) return;
  board = originalBoard.map(row => [...row]);
  originalBoard = null;
  undoButton.disabled = true;
  renderBoard();
  setStatus('Showing your original clues.');
}

puzzleTypeSelect.addEventListener('change', configureMode);
sizeSelect.addEventListener('change', buildGrid);
solveButton.addEventListener('click', solvePuzzle);
undoButton.addEventListener('click', restoreClues);
clearButton.addEventListener('click', () => {
  board = blankBoard(size);
  originalBoard = null;
  undoButton.disabled = true;
  renderBoard();
  setStatus('Board cleared.');
});

exampleButton.addEventListener('click', () => {
  if (puzzleType === 'sudoku') {
    board = [
      [5,3,null,null,7,null,null,null,null], [6,null,null,1,9,5,null,null,null], [null,9,8,null,null,null,null,6,null],
      [8,null,null,null,6,null,null,null,3], [4,null,null,8,null,3,null,null,1], [7,null,null,null,2,null,null,null,6],
      [null,6,null,null,null,null,2,8,null], [null,null,null,4,1,9,null,null,5], [null,null,null,null,8,null,null,7,9]
    ];
  } else {
    sizeSelect.value = '6';
    buildGrid();
    board = [
      [null,0,null,null,1,null], [1,null,null,0,null,null], [null,null,0,null,null,1],
      [null,1,null,null,0,null], [0,null,null,1,null,null], [null,null,1,null,null,0]
    ];
  }
  originalBoard = null;
  renderBoard();
  setStatus('Example loaded — solve it or edit any clue.');
});

document.querySelector('#photoButton').addEventListener('click', () => photoInput.click());
photoInput.addEventListener('change', () => {
  const file = photoInput.files?.[0];
  if (!file) return;
  photoImage.src = URL.createObjectURL(file);
  photoPreview.hidden = false;
  setStatus('Photo added as a reference — copy its clues into the grid.');
});
document.querySelector('#removePhoto').addEventListener('click', () => {
  if (photoImage.src.startsWith('blob:')) URL.revokeObjectURL(photoImage.src);
  photoImage.removeAttribute('src');
  photoInput.value = '';
  photoPreview.hidden = true;
});

const helpDialog = document.querySelector('#helpDialog');
document.querySelector('#helpButton').addEventListener('click', () => helpDialog.showModal());
document.querySelector('#closeHelp').addEventListener('click', () => helpDialog.close());
helpDialog.addEventListener('click', event => { if (event.target === helpDialog) helpDialog.close(); });

configureMode();
