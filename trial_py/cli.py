import os.path, sys, signal, re, os
from concurrent.futures import as_completed, ThreadPoolExecutor
from functools import partial
from threading import Event
import init, make_folder, input_manipulation, question_score, qs_mainpulation, crop_final, cleaning, crop_table, read_question_ms, crop_ms
from rich import print
from rich.console import Console
from rich import box
from rich.table import Table
import numpy as np

from rich.progress import (
    BarColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeElapsedColumn
)

progress = Progress(
    TextColumn("[bold blue]Past Paper(s)", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    TimeElapsedColumn(),
)

done_event = Event() #threading

def handle_sigint(signum, frame):
    done_event.set() #terminate thread

signal.signal(signal.SIGINT, handle_sigint)
console = Console()

def run_pdf(task_id: TaskID, qp_input_path: str, ms_input_path: str, output_format: str) -> None:

    if ms_input_path != None:
        progress.console.log(f"Processing {qp_input_path} and {ms_input_path}")
    else:
        progress.console.log(f"Processing {qp_input_path}")

    progress.update(task_id, total = 41)
    progress.start_task(task_id)

    (images, count) = make_folder.io_mac(qp_input_path)
    progress.update(task_id, advance=2)

    (crop_bottom, count) = input_manipulation.tessa(images, count)
    progress.update(task_id, advance=28)
    
    (cropped, left) = input_manipulation.cropping(images, count, crop_bottom)
    progress.update(task_id, advance=2)

    input_manipulation.merge(cropped, left)
    progress.update(task_id, advance=1)

    (question_result, score_result) = question_score.find_q_s()
    progress.update(task_id, advance=3)

    q_s_dict = qs_mainpulation.sort_qs(question_result, score_result)
    progress.update(task_id, advance=1)
    
    paper_code = crop_final.output_crop(q_s_dict, output_format)
    progress.update(task_id, advance=2)
    
    if ms_input_path == None:
        cleaning.clean_up("QP")
        progress.update(task_id, advance=2)

    elif ms_input_path != None:
        progress.update(task_id, total = 101)
        cleaning.clean_up("QP")
        progress.update(task_id, advance=1)

        (images, count) = make_folder.io_mac(ms_input_path)
        progress.update(task_id, advance=1)

        ms_question_dict = {}
        count_temp = 1
        ms_start = crop_table.check_GMP(images)
        progress.update(task_id, advance=5)

        for ms_count in range(ms_start, len(images)):
            boxes = crop_table.find_table(ms_count)
            (count_temp, box_dict) = crop_table.sort_table(count_temp, boxes)
            ms_question_dict.update(box_dict)
            images = [images[index] for index in range(count)]
            width = crop_table.cropping(ms_count, box_dict, np.array(images))

        progress.update(task_id, advance=50)

        (x, y, x2, y2) = crop_table.save_header(box_dict, images)
        question_dict = {}
        progress.update(task_id, advance=1)

        for ms_2_count in range(1,count_temp):
            question_result = read_question_ms.question_OCR(width, ms_2_count)
            question_dict = read_question_ms.sort_questions(question_dict, question_result)
        progress.update(task_id, advance=1)

        (question_dict, pages_depth) = crop_ms.sorting_ms_dict(question_dict)
        progress.update(task_id, advance=1)

        crop_ms.cropping_ms(paper_code, x, y, x2, y2, question_dict, pages_depth, output_format)
        progress.update(task_id, advance=1)

        cleaning.clean_up("MS")
        progress.update(task_id, advance=1)

    if done_event.is_set():
        return
    
    # if ms_input_path != None:
    #     progress.console.log(f"Processed {qp_input_path} and {ms_input_path}")
    # else:
    #     progress.console.log(f"Processed {qp_input_path}")


def start(input_file_structure: str, qp_input_path: str, ms_input_path: str, output_format: str):
    if output_format == "1":
        output_format = "jpg"
    elif output_format == "2":
        output_format = "png"

    with progress:
        with ThreadPoolExecutor(max_workers=1) as pool:
            if ms != None:
                task_id = progress.add_task("Parsing question paper ({qp_input_path}) and markscheme ({ms_input_path})", qp_input_path = qp, ms_input_path = ms, start = False)
                pool.submit(run_pdf, task_id, qp, ms, output_format)
            else:
                task_id = progress.add_task("Parsing question paper ({qp_input_path})", qp_input_path = qp, ms_input_path = ms, start = False)
                pool.submit(run_pdf, task_id, qp, ms, output_format)
               
if __name__ == "__main__":
    os_req = init.start()
    os.system("clear")
    if os_req == True:
        #input file structure
        console.rule("[bold blue]Input File Structure selection", style="bold white")
        console.print("Please choose [bold magenta]one[/] of the below Input File Structure formats for the program to run on:\n")

        table = Table(title="Input File Structure Choices", box=box.HEAVY_EDGE)
        table.add_column("Option", justify="center")
        table.add_column("Output format", justify="center")
        table.add_row("1", "Single Question Paper file")
        table.add_row("2", "Pair of Question Paper and Mark Scheme")
        console.print(table)

        input_file_structure = console.input("Enter [bold magenta]Option[/] here: ")
        while input_file_structure != "1" and input_file_structure != "2":
            input_file_structure = console.input("Usage:\n\tEnter [bold magenta]1 or 2[/] here: ")

        console.clear()

        #input selection
        console.rule("[bold blue]Input selection", style="bold white")
        if input_file_structure == "1":
            qp = console.input("Please type the [bold magenta]file name[/bold magenta], including [bold magenta]file extension (ie. .pdf)[/] of the past question paper file you would like to parse: ")
            while not os.path.isfile(qp):
                qp = console.input("Usage:\n\tPlease type a [bold magenta]valid file name[/bold magenta], including [bold magenta]file extension (ie. .pdf)[/] of the past question paper file you would like to parse: ")
            ms = None
        else:
            qp = console.input("Please type the [bold magenta]file name[/bold magenta], including [bold magenta]file extension (ie. .pdf)[/], of the [bold magenta]past question paper file[/] you would like to parse: ")
            while not os.path.isfile(qp):
                qp = console.input("Usage:\n\tPlease type a valid [bold magenta]file name[/bold magenta], including [bold magenta]file extension (ie. .pdf)[/], of the [bold magenta]past question paper file[/] you would like to parse: ")

            ms = console.input("Please type the [bold magenta]file name[/bold magenta], including [bold magenta]file extension (ie. .pdf)[/] of the [bold cyan]matching markscheme file[/] you would like to parse: ")
            while not os.path.isfile(ms):
                ms = console.input("Usage:\n\tPlease type a valid [bold magenta]file name[/bold magenta], including [bold magenta]file extension (ie. .pdf)[/] of the [bold cyan]matching markscheme file[/] you would like to parse: ")

        console.clear()

        #output format
        console.rule("[bold blue]Output Format selection", style="bold white")
        console.print("Please choose [bold magenta]one[/] of the below output formats:\n")

        table = Table(title="Output Format Choices", box=box.HEAVY_EDGE)
        table.add_column("Option", justify="center")
        table.add_column("Output format", justify="center")
        table.add_row("1", "jpg")
        table.add_row("2", "png")
        console.print(table)

        output_format = console.input("Enter [bold magenta]Option[/] here: ")
        while output_format != "1" and output_format != "2":
            output_format = console.input("Usage:\n\tEnter [bold magenta]1 or 2[/] here: ")

        console.clear()

        if input_file_structure == "1":
            console.rule("\n[bold blue]Great! Please wait while we work through [bold cyan]{}[/][/]".format(qp), style="bold white")

        else:
            console.rule("\n[bold blue]Great! Please wait while we work through [bold cyan]{} and {}[/][/]".format(qp, ms), style="bold white")

        start(input_file_structure, qp, ms, output_format)
        
        if ms != None:
            progress.console.log(f"Processed {qp} and {ms}")
        else:
            progress.console.log(f"Processed {qp}")

        console.print()
        console.rule("[bold blue]Done![/]", style="bold white")

        console.print("Please check your past paper file location again, there should be a new folder containing all the\ncropped and sorted individual images of questions/answers!\n\n")
        console.rule("[bold blue]Terminating", style = "bold red")

