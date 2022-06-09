# one = input("\nPlease type the name of the past paper folder you would like to parse: ")
# output = int(input("Please choose one of the below output formats:\n\t1) jpg\n\t2) png\n\t3) pdf\nEnter number here: "))
# if output == 1:
# 	output = 'jpg'
# elif output == 2:
# 	output = 'png'
# elif output == 3:
# 	output = 'pdf'

# print("\nGreat! Please wait while we work through", one)
# import itertools
# import threading
# import time
# import sys

# done = False
# #here is the animation
# def animate():
#     for c in itertools.cycle(['|', '/', '-', '\\']):
#         if done:
#             break
#         sys.stdout.write('\rworking ' + c)
#         sys.stdout.flush()
#         time.sleep(0.2)
#     sys.stdout.write('\rDone! Please check {} again, there should be a new folder containing all the\ncropped and sorted individual {} images of questions!\n\n					'.format(one, output))

# t = threading.Thread(target=animate)
# t.start()

# #long process here
# time.sleep(30)
# done = True

# import sys
# print()

# from progress.bar import IncrementalBar 
# import time
# bar = IncrementalBar('Processing', max=20, suffix = '%(percent)d%%\t[%(elapsed_td)s/%(eta_td)s]')
# for i in range(20):
#     time.sleep(0.1)
#     bar.next()
# bar.finish()

from rich import print
from rich.console import Console
console = Console()
console.rule("[bold blue]Input selection", style="bold white")
console.print("Please type the [bold magenta]path[/bold magenta] of the past paper folder you would like to parse: ")
one = console.input()
from rich import box
from rich.table import Table
console.rule("[bold blue]Output format selection", style="bold white")
console.print("Please choose [bold magenta]one[/] of the below output formats:\n")
my_list = ["1) jpg", "2) png", "3) pdf"]
table = Table(title="output choices", box=box.HEAVY_EDGE)
table.add_column("Number", justify="center")
table.add_column("Output format", justify="center")
table.add_row("1", "jpg")
table.add_row("2", "png")
table.add_row("3", "pdf")
console.print(table)
output = console.input("Enter [bold magenta]Number[/] here: ")

console.rule("\n[bold blue]Great! Please wait while we work through [bold cyan]{}[/][/]".format(one), style="bold white")

# from rich.progress import track
# import time
# for i in track(range(20)):
#   time.sleep(0.1)
#   do_step(step)

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
# from progress.bar import IncrementalBar 
# import time
# bar = IncrementalBar('Processing', max=20, suffix = '%(percent)d%%\t[%(elapsed_td)s/%(eta_td)s]')
# for i in range(20):
#     time.sleep(0.1)
#     bar.next()
# bar.finish()

if output == "1":
  a = "jpg"
elif output == "2":
  a = "png"
elif output == "3":
  a = "pdf"
console.print()
console.rule("[bold blue]Done![/]", style="bold white")
console.print("Please check [bold cyan]{}[/bold cyan] again, there should be a new folder containing all the\ncropped and sorted individual [bold cyan]{}[/] images of questions!\n\n".format(one, a))
console.print()
console.rule("[bold blue]Press any key to terminate", style="bold red")
console.input()

# one = input("\nPlease type the name of the past paper folder you would like to parse: ")

