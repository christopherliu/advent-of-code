// TODO greedily pursue moving amphipods home
const util = require('util');

let debug = false;

type Occupant = "." | "A" | "B" | "C" | "D";

class Position {
    room: "hallway" | "rooms";
    x: number;
    y: number;

    static HALLWAY = "hallway";
    static ROOMS = "rooms";

    constructor(room: "hallway" | "rooms", x: number, y: number) {
        this.room = room;
        this.x = x;
        this.y = y;
    }

    getInMemoryX() {
        if (this.room === "hallway") {
            return [0, 1, 3, 5, 7, 9, 10].indexOf(this.x);
        }
        else if (this.room === "rooms") {
            return [2, 4, 6, 8].indexOf(this.x);
        }
        throw "That's all";
    }
    inspect() {
        return "HA";
    }
}

class Move {
    start: Position;
    destination: Position;
    constructor(start: Position, destination: Position) {
        this.start = start;
        this.destination = destination;
    }
    print(): string {
        return `${this.start.room}:(${this.start.x},${this.start.y}) - ${this.destination.room}:(${this.destination.x},${this.destination.y})`
    }
    [util.inspect.custom]() {
        return this.print();
    }
}

const HALLWAY_OPTIONS = [0, 1, 3, 5, 7, 9, 10].map((x) => new Position("hallway", x, -1));
const ROOM_OPTIONS = [2, 4, 6, 8].flatMap((x) => [0, 1, 2, 3].map((y) => new Position("rooms", x, y)));
const ALL_VALID_MOVES = HALLWAY_OPTIONS.flatMap((h) => ROOM_OPTIONS.flatMap((r) => [new Move(h, r), new Move(r, h)]));

class AmphipodBurrowState {
    hallway: Occupant[];
    rooms: Occupant[][];

    static cost = {
        ".": 100000,
        "A": 1,
        "B": 10,
        "C": 100,
        "D": 1000
    };

    constructor(
        hallway: Occupant[],
        rooms: Occupant[][]) {
        this.hallway = hallway;
        this.rooms = rooms;
    }

    public static fromString(map: string): AmphipodBurrowState {
        const mapLines = map.split("\n");
        const hallway = [...mapLines[1].slice(1, 11)].map((c) => <Occupant>c)
        const rooms = [3, 5, 7, 9].map((x) => [2, 3, 4, 5].map((y) => <Occupant>mapLines[y][x]));
        return new AmphipodBurrowState(hallway, rooms);
    }

    costOf(move: Move): number {
        const costPerSpace = AmphipodBurrowState.cost[this.getAtPosition(move.start)];
        return costPerSpace * (Math.abs(move.start.x - move.destination.x) + Math.abs(move.start.y - move.destination.y));
    }

    getAtPosition(position: Position): Occupant {
        if (position.room === Position.HALLWAY) {
            return this.hallway[position.getInMemoryX()];
        } else if (position.room === Position.ROOMS) {
            return this.rooms[position.getInMemoryX()][position.y];
        } else {
            throw "Invalid input";
        }
    }

    _setAtPosition(position: Position, occupant: Occupant) {
        if (position.room === Position.HALLWAY) {
            this.hallway[position.getInMemoryX()] = occupant;
        } else if (position.room === Position.ROOMS) {
            this.rooms[position.getInMemoryX()][position.y] = occupant;
        }
    }
    _isValidMove(move: Move) {
        // Returns true if: there is a valid piece to move, and all intermediate spaces are unoccupied.
        if (this.getAtPosition(move.start) === ".")
            return false;

        for (let x = Math.min(move.start.x, move.destination.x); x <= Math.max(move.start.x, move.destination.x); x++) {
            if ([0, 1, 3, 5, 7, 9, 10].indexOf(x) !== -1)
                if (this.hallway[[0, 1, 3, 5, 7, 9, 10].indexOf(x)] !== "." && x !== move.start.x)
                    return false;
        }

        const startMemoryX = move.start.getInMemoryX();
        const endMemoryX = move.destination.getInMemoryX();

        const roomEndpoint = (move.start.room === "rooms" ? move.start : move.destination);
        const roomY = roomEndpoint.y;
        const roomIndex = roomEndpoint.getInMemoryX();
        for (let y = 0; y < roomY; y++)
            if (this.rooms[roomIndex][y] !== ".")
                return false;

        // Don't let em leave a valid room.
        if (move.start.room === "rooms") {
            const properAmphipod = ["A", "B", "C", "D"][startMemoryX];
            if (properAmphipod === this.getAtPosition(move.start)) {
                let atHome = true;
                const startRoom = this.rooms[startMemoryX];
                for (let y = roomY + 1; y < 4; y++)
                    if (startRoom[y] !== properAmphipod)
                        atHome = false;
                if (atHome)
                    return false;
            }
        }

        // Amphipods will never move from the hallway into a room unless
        // that room is their destination room and that room contains no
        // amphipods which do not also have that room as their own destination.
        if (move.destination.room === "rooms") {
            const properAmphipod = ["A", "B", "C", "D"][endMemoryX];
            if (properAmphipod !== this.getAtPosition(move.start))
                return false;
            const destinationRoom = this.rooms[endMemoryX];
            for (let y = 0; y <= roomY; y++) {
                if (destinationRoom[y] !== ".")
                    return false;
            }
            for (let y = roomY + 1; y < 4; y++) {
                if (destinationRoom[y] !== properAmphipod)
                    return false;
            }
        }

        return true;
    }
    getValidMoves(): Move[] {
        return (ALL_VALID_MOVES).filter((m) => this._isValidMove(m));
    }

    isSolved() {
        return this.hallway.every((occupant) => occupant === ".")
            && this.rooms[0].every((occupant) => occupant === "A")
            && this.rooms[1].every((occupant) => occupant === "B")
            && this.rooms[2].every((occupant) => occupant === "C")
            && this.rooms[3].every((occupant) => occupant === "D")
    }

    _move(move: Move) {
        this._setAtPosition(move.destination, this.getAtPosition(move.start));
        this._setAtPosition(move.start, ".");
    }

    withMove(move: Move): AmphipodBurrowState {
        const abs = new AmphipodBurrowState([...this.hallway], this.rooms.map((room) => [...room]));
        abs._move(move);
        return abs;
    }

    /**
     * DFS that looks for cheapest solution.
     * @returns {Move[]} List of moves that solves board most cheaply
     */
    findBestSolution(cost = 0): { moves: Move[], cost: number } | null {
        if (this.isSolved()) {
            return { moves: [], cost: 0 };
        }
        //if (cost > 100000) { return null; }

        debug && console.log(this.renderBoard());
        // console.log("Currently at cost", cost);
        const allMoves = this.getValidMoves().map((move) => {
            debug && console.log("Trying move", move.print());
            const currentCost = this.costOf(move);
            const solutionWithMove = this.withMove(move).findBestSolution(cost + currentCost);
            if (solutionWithMove !== null) {
                return {
                    moves: [move].concat(solutionWithMove.moves),
                    cost: currentCost + solutionWithMove.cost
                };
            }
            debug && console.log("Move failed, going back one step up");
            return null;
        });

        return allMoves.filter((x) => x !== null).reduce((previousValue, currentValue) => {
            return (!previousValue || (previousValue && currentValue && previousValue.cost > currentValue.cost)) ? currentValue : previousValue;
        }, null);
    }
    renderBoard(): any {
        const h = this.hallway;
        const r = this.rooms;
        return `#############
#${h[0]}${h[1]}.${h[2]}.${h[3]}.${h[4]}.${h[5]}${h[6]}#
###${r[0][0]}#${r[1][0]}#${r[2][0]}#${r[3][0]}###
  #${r[0][1]}#${r[1][1]}#${r[2][1]}#${r[3][1]}#
  #${r[0][2]}#${r[1][2]}#${r[2][2]}#${r[3][2]}#
  #${r[0][3]}#${r[1][3]}#${r[2][3]}#${r[3][3]}#`;
    }
}

const maps = {
    "trivialCase": `#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########`,
  "almostTrivialCase": `#############
#...........#
###A#D#C#B###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########`
};
const testMap =
    `#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########`;

const args = process.argv;
if (args.length > 2) debug = true;

const initialState = AmphipodBurrowState.fromString(maps.almostTrivialCase);
const solution = initialState.findBestSolution();
console.log(solution);