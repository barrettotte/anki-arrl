import json
import requests
import sys
import traceback

def get_question_pool(exam_label: str) -> list:
    """
    Fetches question pool from ARRL as JSON array
    """
    return requests.get(url=f'https://arrlexamreview.appspot.com/_study/{exam_label}.json').json()['questions']

def arrl_to_anki(arrl: dict) -> dict:
    """
    Converts ARRL question to Anki flashcard

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
    return {
        'id': arrl['id'],
        'number': arrl['qn'],
        'question': arrl['qt'],
        'choices': [arrl['at1'], arrl['at2'], arrl['at3'], arrl['at4']],
        'answer': arrl['ca']
    } # TODO: actual anki format

def main():
    if len(sys.argv) < 2:
        print('Missing exam label.\nUsage: python anki-arrl.py <EXAM_LABEL> [OUT_PATH]')
        exit(1)

    exam_label = sys.argv[1]
    out_path = '.' if len(sys.argv != 3) else sys.argv[2]

    try:
        questions = get_question_pool(exam_label)
        cards = []
        for q in questions:
            card = arrl_to_anki(q)
            print(card) # TODO: remove
            cards.append(card)
            break # TODO: remove
        # TODO: save cards to file
    except KeyboardInterrupt:
        print('Exited early.')
    except Exception as e:
        print('Unexpected exception occurred!')
        traceback.print_exc()
        exit(2)

if __name__ == '__main__':
    main()