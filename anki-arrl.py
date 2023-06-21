# Convert ARRL exam review questions to Anki flashcards.

import genanki
import os
import requests
import sys
import traceback

# arbitrary random ids for Anki
MODEL_ID = 4445681636
DECK_ID_BASE = MODEL_ID + 1

ARRL_BASE = 'https://arrlexamreview.appspot.com/_study'

# model for each Anki card
anki_model = genanki.Model(
    model_id=MODEL_ID,
    name='ARRL Exam Question',
    fields=[
        {'name': 'Number'},
        {'name': 'Id'},
        {'name': 'Question'},
        {'name': 'ChoiceA'},
        {'name': 'ChoiceB'},
        {'name': 'ChoiceC'},
        {'name': 'ChoiceD'},
        {'name': 'AnswerLetter'},
        {'name': 'AnswerFull'},
    ],
    templates=[
        {
            'name': 'ARRL Exam Question Card',
            'qfmt': '{{Number}}). [{{Id}}]<br><br>{{Question}}<br>' +
                '<br>a). {{ChoiceA}}' +
                '<br>b). {{ChoiceB}}' +
                '<br>c). {{ChoiceC}}' +
                '<br>d). {{ChoiceD}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{AnswerLetter}}). {{AnswerFull}}',
        },
    ],
)

def get_question_pool(exam_label: str) -> list:
    """
    Fetches question pool from ARRL as JSON array
    """
    url = f'{ARRL_BASE}/{exam_label}.json'
    resp = requests.get(url=url)

    if resp.status_code != 200:
        print(f'Error: GET {url} returned status code of {resp.status_code}')
        exit(3)
    return resp.json()['questions']

def arrl_to_anki(arrl: dict, model: genanki.Model) -> genanki.Note:
    """
    Convert each ARRL question to an Anki note
    Example question:
    {
        "id": 325,
        "qn": "T8B11",
        "qg": "T8B",
        "qt": "Who may receive telemetry from a space station",
        "at1": "Anyone",
        "at2": "A licensed radio amateur with a transmitter equipped for interrogating the satellite",
        "at3": "A licensed radio amateur who has been certified by the protocol developer",
        "at4": "A licensed radio amateur who has registered for an access code from AMSAT",
        "ca": "1",
        "cn": "6",
        "sn": "6",
        "pn": "6-24"
    }
    """
    answer_idx = int(arrl['ca']) - 1
    choices = [arrl['at1'].strip(), arrl['at2'].strip(), arrl['at3'].strip(), arrl['at4'].strip()]
    
    fields = [
        str(arrl['id']), # question number
        arrl['qn'].strip(),  # question id
        arrl['qt'].strip(),  # question
        choices[0], # A
        choices[1], # B
        choices[2], # C
        choices[3], # D
        ['a','b','c','d'][answer_idx], # answer letter
        choices[answer_idx], # answer full
    ]
    return genanki.Note(model=model, fields=fields)

def main():
    if len(sys.argv) < 2:
        print('Missing exam label.\nUsage: python anki-arrl.py <EXAM_LABEL> [OUT_PATH]')
        exit(1)

    try:
        exam_label = sys.argv[1]
        out_path = '.' if len(sys.argv) != 3 else sys.argv[2]

        if not os.path.exists(out_path):
            os.makedirs(out_path)

        # pull questions from ARRL site
        questions = get_question_pool(exam_label)

        # calculate unique deck id for particular exam
        deck_id = DECK_ID_BASE + sum([ord(c) for c in exam_label])
        deck = genanki.Deck(deck_id, f'ARRL Exam - {exam_label}')

        # create anki note for each question
        for q in questions:
            note = arrl_to_anki(q, anki_model)
            deck.add_note(note)
        
        # save deck to anki package
        package_path = os.path.join(out_path, f'arrl-{exam_label}.apkg')
        genanki.Package(deck).write_to_file(package_path)
        print(f'Created Anki deck of {len(questions)} card(s) at {package_path}')

    except KeyboardInterrupt:
        print('Exited early.')
    except Exception:
        print('Unexpected exception occurred!')
        traceback.print_exc()
        exit(2)

if __name__ == '__main__':
    main()
