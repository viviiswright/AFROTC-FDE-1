from dataclasses import dataclass, field
from drafter import (
    route,
    start_server,
    set_website_title,
    set_site_information,
    hide_debug_information,
    set_website_framed,
    Page,
    TextBox,
    CheckBox,
    Button,
    Row,
    Header,
    Text,
    LineBreak,
)

set_website_title("AFROTC Flight Drill Evaluation (FDE) Game")
set_site_information(
    author="Viviana Wright",
    description="AFROTC FDE game to train cadets.",
    sources="DAFPAM 34-1203.",
    planning=["Message_to_the_TA.pdf", "Final_Project_1_Design.pdf", "Final_Project_0_Pick_a_Problem.pdf"],
    links=["https://github.com/your-username/your-repository"],
)
set_website_framed(False)


@dataclass
class DrillMovement:
    """Represents a single required FDE drill movement."""
    name: str
    completed: bool
    requires_marching: bool
    required_formation: str
    point_value: int

def create_initial_movements() -> list[DrillMovement]:
    """Creates the initial list of 20 drill movements."""
    return [
        DrillMovement("Left Face", False, False, "ANY", 5),
        DrillMovement("Right Face", False, False, "ANY", 5),
        DrillMovement("About Face", False, False, "ANY", 5),
        DrillMovement("Parade Rest", False, False, "ANY", 5),
        DrillMovement("Attention", False, False, "ANY", 5),
        DrillMovement("Present Arms", False, False, "ANY", 5),
        DrillMovement("Order Arms", False, False, "ANY", 5),
        DrillMovement("Left Step", False, False, "ANY", 5),
        DrillMovement("Right Step", False, False, "ANY", 5),
        DrillMovement("Forward March", False, False, "ANY", 5),
        DrillMovement("Half Step", False, True, "ANY", 5),
        DrillMovement("Column Left", False, True, "Column Formation", 5),
        DrillMovement("Column Right", False, True, "Column Formation", 5),
        DrillMovement("Left Flank", False, True, "ANY", 5),
        DrillMovement("Right Flank", False, True, "ANY", 5),
        DrillMovement("To the Rear", False, True, "ANY", 5),
        DrillMovement("Change Step", False, True, "ANY", 5),
        DrillMovement("Mark Time", False, True, "ANY", 5),
        DrillMovement("Flight Halt", False, True, "ANY", 5),
        DrillMovement("Cover", False, False, "Column Formation", 5),
    ]

@dataclass
class State:
    """Tracks game info across all the pages"""
    flight_name: str = "Alpha"
    score: int = 100
    stance: str = "Halted (At Attention)"
    facing: str = "NORTH"
    formation: str = "Line Formation"
    must_march_next: bool = False
    status_feedback: str = "Feedback pending..."
    show_checklist: bool = True
    movements: list[DrillMovement] = field(default=create_initial_movements)
    evaluation_complete: bool = False

@route
def index(state: State) -> Page:
    """Page One: Startup screen with basic info and facts for players to understand the mission/goal."""
    return Page(state, [
        Header("AFROTC Flight Drill Evaluation (FDE) Game"),
        Text("Welcome cadet! Practice calling your 20 FDE movements."),
        Button("Start Flight Drill Evaluation", instructions),
    ])

@route
def instructions(state: State) -> Page:
    """Page Two: Instructions and  Rules of Engagement for players to understand HOW to issue commands and what they mean."""
    return Page(state, [
        Header("Instructions and Rules of Engagement"),
        Text("[Mission: Learn and practice all 20 FDE mvovements in accordance with DAFPAM 34-1203]"),
        Row(
            Button("Back", index),
            Button("Setup Flight", setup_flight),
        ),
    ])

@route
def setup_flight(state: State) -> Page:
    """Page Three: Pre-evaluation setup and starting orientation, so that players understand how the flight looks to begin with."""
    return Page(state, [
        Header("Flight Setup and Starting Orientation"),
        Text("Flight Name:"),
        TextBox("flight_name", state.flight_name),
        Row(
            CheckBox("show_checklist", state.show_checklist),
            Text("Show 20-Command Checklist"),
        ),
        Text("Starting Orientation: Halted (At Attention) / Facing: NORTH / Line Formation"),
        Row(
            Button("Back", instructions),
            Button("Begin FDE", current_score),
        ),
    ])

@route
def current_score(state: State) -> Page:
    """Page Four: Main evaluation screen and skeleton of the game."""
    elements = [
        Header(f"{state.flight_name} Flight — FDE Evaluation"),
        Text(f"Score: {state.score} / 100"),
        Text(f"Stance: {state.stance} | Facing: {state.facing} | Formation: {state.formation}"),
        Text(f"Feedback: {state.status_feedback}"),
        LineBreak(),
        Text("Enter Command Number (1-20):"),
        TextBox("command_input", ""),
        Row(
            Button("Submit Command", enter_command),
            Button("Finish Evaluation", final_results),
        ),
    ]

    if state.show_checklist:
        elements.append(LineBreak())
        elements.append(Header("20-Command Reference Checklist"))
        for idx, move in enumerate(state.movements, start=1):
            mark = "✅" if move.completed else "⬜"
            elements.append(Text(f"{mark} {idx}. {move.name}"))

    return Page(state, elements)

@route
def enter_command(state: State, command_input: str) -> Page:
    """This is going to be how the feedback box provdes feedback to players. It is a WIP."""
    # is the input a integer from (1-20)?
    # must_march_next, stance, formation
    # Update stance, facing, formation, score, and move.completed
    # Auto-route to final_results when all 20 movements = complete
    state.status_feedback = f"Received input '{command_input}' (Game rules not yet implemented)."
    return current_score(state)

@route
def final_results(state: State) -> Page:
    """Page Five: This is the final evaluation score screen, where the player sees pass or fail."""
    return Page(state, [
        Header(f"Evaluation Complete for {state.flight_name} Flight"),
        Text(f"Final Score: {state.score} / 100"),
        Text("[You Passed! (>= 75) or You Failed! (< 75).]"),
        Button("Try Again", reset_game),
    ])

@route
def reset_game(state: State) -> Page:
    """Resets State and routes back to the startup screen."""
    return index(State())

start_server(State(), port=8080)
