# anki-arrl

Convert ARRL amateur radio exam question pools to Anki decks.

I made this to make studying for amateur radio exams a little more convenient.
I also included the generated Anki decks in [/decks](decks/) in case someone else 
wanted to use them without running the script themselves.

## Usage

`python anki-arrl.py <EXAM_LABEL> [OUT_PATH]`

## Question Pools

Exams are found in the format `https://arrlexamreview.appspot.com/_study/EXAM_LABEL.html`,
the corresponding question pool is found by replacing `.html` with `.json`.

So, the Technician 2022 question pool would be located at `https://arrlexamreview.appspot.com/_study/tech2022.json`

Exams:

- Technician
  - `tech2022` (July 1, 2022 to June 30, 2026)
- General
  - `gene2023` (July 1, 2023 to June 30, 2027)
- Extra
  - `extr2020` (July 1, 2020 to June 30, 2024)
