
from datetime import datetime
import serial
from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from rich.prompt import Prompt
import threading
from time import sleep
from rich.live import Live
from prompt_toolkit import prompt
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout as PTLayout
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import clear

console = Console()

def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="Console", size=7),
    )
    layout["main"].split_row(
        Layout(name="side"),
        Layout(name="body", ratio=1, minimum_size=30),
    )
    layout["side"].split(Layout(name="Message"), Layout(name="box2"))
    layout["box2"].split_row(Layout(name="Activity"), Layout(name="Data",ratio = 6))
    return layout


class Header:
    """Display header with clock."""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "Diagnostics",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white on blue")

def make_console_panel() -> Panel:
    return

def make_activity_panel() -> Panel:
    activity_obj = Progress(
        TextColumn("{task.description}"),
        SpinnerColumn(),
        console=console,
        transient=True 
    )
    activity_obj.add_task("[green]Startup")
    activity_obj.add_task("[green]Enable Fans")

    

    activity_panel = Panel(
        Align.center(
            Group("\n", Align.center(activity_obj)),
            
            vertical="top",
        ),
        box=box.ROUNDED,
        # padding=(1, 1),
        title="[b green]Activity",
        border_style="bright_green",
    )
    

    return activity_panel

def make_message_panel() -> Panel:
    msg_grid = Table(padding=(0, 0), expand=True, show_edge=False, style="color(208)",pad_edge=True)
    msg_grid.add_column("Type", justify="center", style="white", no_wrap=True)
    msg_grid.add_column("Info(12e)(7w)(1n)", justify="left", style="white", no_wrap=True, ratio = 3)

    
    msg_grid.add_row("[bright_red]Error", "[red]DASH elouseaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    msg_grid.add_row("", "                                                                                                                                               ")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    msg_grid.add_row("", "")
    
    
    msg_panel = Panel(
       Align.left(msg_grid),
        box=box.ROUNDED,
        padding=(0, 0),
        expand= True,
        title="[b orange]Message",
        border_style="color(208)",
          
    )
    return msg_panel
def make_data_panel() -> Panel:
    # Create a table with headers
    data_grid = Table(padding=(0, 14), expand=True, show_edge=False, style="bright_green",pad_edge=True)
    data_grid.add_column("Name", justify="center", style="cyan", no_wrap=False)
    data_grid.add_column("Value", justify="center", style="magenta", no_wrap=False)
    data_grid.add_column("Unit", justify="center", style="green", no_wrap=False)
    
    # Add rows to the table
    
    data_grid.add_row("Velocity", "5", "m/s")
    data_grid.add_row("Acceleration", "9.8", "m/s²")
    data_grid.add_row("Velocity", "5", "m/s")
    data_grid.add_row("Acceleration", "9.8", "m/s²")
    data_grid.add_row("Velocity", "5", "m/s")
    data_grid.add_row("Acceleration", "9.8", "m/s²")
    data_grid.add_row("", "", "")
    data_grid.add_row("", "", "")
    data_grid.add_row("", "", "")
    data_grid.add_row("", "", "")
    data_grid.add_row("", "", "")
    data_grid.add_row("", "", "")
    data_grid.add_row("", "", "")
    data_grid.add_row("", "", "")
    data_grid.add_row("", "", "")
    data_grid.add_row("", "", "")
    data_grid.add_row("", "", "")
    data_grid.add_row("", "", "")
    data_grid.add_row("", "", "")
    data_grid.add_row("", "", "")
    
    # Create a panel containing the table, with centered alignment
    data_panel = Panel(
        Align.center(data_grid),
        box=box.ROUNDED,
        padding=(0, 0),
        expand= True,
        title="[b green]Data",
        border_style="bright_green",
    )

    return data_panel
def make_notification_message() -> Panel:
    """Some example content."""
    notification_message = Table.grid(padding=1)
    notification_message.add_column(style="green", justify="right")
    notification_message.add_column(no_wrap=True)
    notification_message.add_row(
        "Twitter",
        "[u blue link=https://twitter.com/textualize]https://twitter.com/textualize",
    )
    notification_message.add_row(
        "CEO",
        "[u blue link=https://twitter.com/willmcgugan]https://twitter.com/willmcgugan",
    )
    notification_message.add_row(
        "Textualize", "[u blue link=https://www.textualize.io]https://www.textualize.io"
    )

    message = Table.grid(padding=1)
    message.add_column()
    message.add_column(no_wrap=True)
    message.add_row(notification_message)

    message_panel = Panel(
        Align.center(
            Group("\n", Align.center(notification_message)),
            vertical="middle",
        ),
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red]Monitor",
        border_style="bright_red",
    )
    return message_panel




job_progress = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
)
job_progress.add_task("[green]Cooking")
job_progress.add_task("[magenta]Baking", total=200)
job_progress.add_task("[cyan]Mixing", total=400)

total = sum(task.total for task in job_progress.tasks)
overall_progress = Progress()
overall_task = overall_progress.add_task("All Jobs", total=int(total))

progress_table = Table.grid(expand=True)
progress_table.add_row(
    Panel(
        overall_progress,
        title="Overall Progress",
        border_style="green",
        padding=(2, 2),
    ),
    Panel(job_progress, title="[b]Jobs", border_style="red", padding=(1, 2)),
)


layout = make_layout()
layout["header"].update(Header())
layout["body"].update(make_notification_message())
layout["Activity"].update(make_activity_panel())
layout["Data"].update(make_data_panel())
layout["Message"].update(make_message_panel())
# layout["Console"].update(make_console_panel())

with Live(layout, refresh_per_second=10, screen=True) as live:
    while not overall_progress.finished:
        sleep(0.1)
        for job in job_progress.tasks:
            if not job.finished:
                job_progress.update(job.id, advance=1)
        live.update(layout)