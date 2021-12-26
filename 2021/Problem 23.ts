class Room {
    occupant: string;
    constructor(occupant: string){
        this.occupant = occupant;
    }
}

class Move {
    start: string;
    destination: string;
}

class AmphipodBurrowState {
    hallway: Room[];
    rooms: Room[][];

    constructor(map: string) {
        const mapLines = map.split("\n");
        this.hallway = mapLines[1].slice(1,11).map((c) => new Room(c))
        this.rooms = [3,5,7,9].map((x) => [2,3,4,5].map((y) => new Room(mapLines[y][x])));
    }

    costOf(move: Move): int {

    }

    getValidMoves(): Move[] {
        function isValidMove(move: Move) {
            // Returns true if: there is a valid piece to move, and all intermediate spaces are unoccupied.
        }

        return (product(ROOM_OPTIONS, HALLWAY_OPTIONS) + product(HALLWAY_OPTIONS, ROOM_OPTIONS)).filter(isValidMove);
    }

    withMove(move: Move): AmphipodBurrowState {

    }

    /**
     * DFS that looks for cheapest solution.
     * 
     * @param {int} costCeiling Ignore solutions that cost more than this.
     * @returns {Move[]} List of moves that solves board most cheaply
     */
    findBestSolutions(let costCeiling: int|false = false): Move[] {
        let bestSolution = null;
        for (let move: this.getValidMoves()) {
            const bestSolutionFromHere = this.withMove(move).findBestSolutions(), costCeiling);
            if (costCeiling !== false || this.costOf(bestSolutionFromHere) < costCeiling) {
                bestSolution = [move] + bestSolutionFromHere;
                costCeiling = this.costOf(bestSolutionFromHere);
            }
        }
        return bestSolution;
    }
}

const testMap =
`#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########`;
const initialState = new AmphipodBurrowState(testMap);
console.log(initialState.findBestSolutions());