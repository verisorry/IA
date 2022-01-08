from rich import print
from rich.console import Console
from rich import box
from rich.table import Table


console = Console()
#section 1
console.rule("[bold blue]Input File Structure selection", style="bold white")
console.print("Please choose [bold magenta]one[/] of the below Input File Structure formats for the program to run on:\n")

table = Table(title="Input File Structure Choices", box=box.HEAVY_EDGE)
table.add_column("Option", justify="center")
table.add_column("Output format", justify="center")
table.add_row("1", "Single Question Paper file")
table.add_row("2", "Single Mark Scheme file")
table.add_row("3", "Pair of Question Paper and Mark Scheme")
console.print(table)

input_file_structure = console.input("Enter [bold magenta]Option[/] here: ")
console.print("\n")
console.clear()

#section 2
console.rule("[bold blue]Input selection", style="bold white")
if input_file_structure == 1:
  console.print("Please type the [bold magenta]path[/bold magenta] of the past paper folder you would like to parse: ")
  input_selection = console.input()
else:
  console.print("Please type the [bold magenta]file name[/bold magenta], including [bold magenta]file extension[/] of the file you would like to parse: ")
  input_selection = console.input()
console.clear()

#section 3
console.rule("[bold blue]Output Format selection", style="bold white")
console.print("Please choose [bold magenta]one[/] of the below output formats:\n")

table = Table(title="Output Format Choices", box=box.HEAVY_EDGE)
table.add_column("Option", justify="center")
table.add_column("Output format", justify="center")
table.add_row("1", "jpg")
table.add_row("2", "png")
console.print(table)

output_format = console.input("Enter [bold magenta]Option[/] here: ")
console.clear()

#section 4
console.rule("\n[bold blue]Great! Please wait while we work through [bold cyan]{}[/][/]".format(input_selection), style="bold white")

#section 5
from rich.progress import Progress
from rich.progress import BarColumn, TimeElapsedColumn
import rich.progress
import time
progress = Progress(
  "[progress.description]{task.description}",
  BarColumn(),
  "[progress.percentage]{task.percentage:>3.0f}%",
  TimeElapsedColumn())
with progress as progress:
  task1 = progress.add_task("[cyan]Processing...", total = 20)
  while not progress.finished:
    progress.update(task1, advance=0.5)
    time.sleep(0.1)

if output_format == "1":
  a = "jpg"
elif output_format == "2":
  a = "png"

console.print()
console.rule("[bold blue]Done![/]", style="bold white")
console.print("Please check [bold cyan]{}[/bold cyan] again, there should be a new folder containing all the\ncropped and sorted individual [bold cyan]{}[/] images of questions!\n\n".format(input_selection, output_format))
console.print()
console.rule("[bold blue]Press any key to terminate", style="bold red")
console.input()
