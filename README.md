# anki-arrl

Convert ARRL exam review questions to Anki flashcards.

I made this to make studying for amateur radio exams a little more convenient.
I also included the generated Anki flashcards in this repo in case someone else 
wanted to use them without running the script themselves.

## Usage

`python anki-arrl.py <EXAM_LABEL> [OUT_PATH]`

## Question Pools

Exams are found in the format `https://arrlexamreview.appspot.com/_study/EXAM_LABEL.html`,
the corresponding question pool is found by replacing `.html` with `.json`.

So, the Technician 2022 question pool would be located at `https://arrlexamreview.appspot.com/_study/tech2022.json`
