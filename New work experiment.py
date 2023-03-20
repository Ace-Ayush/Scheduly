import spacy

from spacy.matcher import Matcher

from flask import Flask, request, jsonify


nlp = spacy.load("en_core_web_sm")

matcher = Matcher(nlp.vocab)


pattern = [{"LOWER": "schedule"}, {"LOWER": "a"}, {"POS": "NOUN"}, {"LOWER": "on"}, {"LOWER": {"IN": ["at", "on"]}}, {"ENT_TYPE": "DATE", "OP": "?"}, {"ENT_TYPE": "TIME", "OP": "?"}, {"LOWER": {"IN": ["with", "between"]}}, {"ENT_TYPE": "PERSON", "OP": "+"}, {"LOWER": {"IN": ["for", "about", "regarding"]}, "OP": "?"}, {"LOWER": {"IN": ["a", "an"]}, "OP": "?"}, {"LOWER": {"IN": ["hour", "hours", "minute", "minutes"]}, "OP": "?"}]

matcher.add("Schedule", [pattern], on_match=None)


app = Flask(__name__)

def jls_extract_def(matcher, doc, i, matches):
    
    return matches


@app.route('/schedule', methods=['POST'])

def schedule():

    text = request.get_json()['text']

    doc = nlp(text)

    matches = matcher(doc)

    if len(matches) == 0:

        return jsonify({'error': 'No matches found.'})

    match_id, start, end = matches[0]

    task = doc[start+2:end].text

    date = None
    time = None

    for ent in doc.ents:

        if ent.label_ == 'DATE':

            date = ent.text
        elif ent.label_ == 'TIME':

            time = ent.text

    attendees = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']

    duration = None

    for i, token in enumerate(doc):

        if token.lower_ in ['hour', 'hours', 'minute', 'minutes']:

            duration = float(doc[i-1].text)

    return jsonify({

        'task': task,
        'date': date,
        'time': time,
        'attendees': attendees,
        'duration': duration

    })

if __name__ == '__main__':

    app.run()
