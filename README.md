# IB Computer Science HL Internal Assessment

## Overview:
Planned and developed a PDF parsing program for teachers to use when organising questions from past exam papers. 
The program takes an individual/folder of PDF and outputs each individual main question as an image, with all its accompanying sub questions attached. 
The program also outputs corresponding mark schemes with intuitive file names.

## Original Issue:
My client, Mr. Greenwood, is an IGCSE ITGS teacher at my school, often having to provide past paper questions as class- or home-work. 
Currently, he has been manually going through each set of past papers and screenshotting questions, then manually sorting them based on year. 
This has been time consuming and repetitive and is a common chore that most teachers have to do.

## Goal: 
A program that you could just put all the past paper PDFs into a folder and run it on and get a bunch of sorted out questions. 
Individual images of separate questions will then be produced, indicated by an appended ‘_q(x)’ at the end of each file name, with ‘(x)’ being the question number. 
For example, an image of Q4 from Summer 2020, paper 1, time zone 1, will be ‘0417_s20_qp_11-q4.jpg’.

## Goal: 
1. Requires minimum user input
2. Parse through a PDF file and produce separate cropped images of questions and its
respective answer.
3. Must output files with correctly formatted file names which includes:
  a. Course code
  b. Year and session
  c. Paper
  d. Question number
4. Each image file must contain the full question with all of its accompanying subquestions.
5. Each image file should have an accompanying mark scheme image.
6. Must be able to run on Cambridge IGCSE ICT exam paper 1 post 2017 syllabus and format
change.
7. Final output must be two folders, one containing questions and the other containing mark
schemes. Each file must be named accordingly and each folder must contain the full paper.

## Results:
_See technical documentation in folder "Forms"_
