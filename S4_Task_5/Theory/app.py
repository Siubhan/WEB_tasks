from flask import Flask, request, render_template
import constants

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    render = bool(request.values)
    name = request.values.get('username', '')
    gender = request.values.get('gender', '')
    program_id = request.values.get('program', 0, int)
    subject_id = request.values.getlist('subject', int)
    subjects_select = [constants.subjects[i] for i in subject_id]

    html = render_template(
        'index.html',
        program_list=enumerate(constants.programs),
        subject_list=enumerate(constants.subjects),
        name=name,
        gender=gender,
        program_id=program_id,
        program=constants.programs[program_id],
        subject_id=subject_id,
        subjects_select=subjects_select,
        render=render
    )
    return html


@app.route('/subject/<sub>')
def subject(sub):
    html = render_template(
        'subject.html',
        sub=sub,
        description=constants.subject_dict[sub]
    )
    return html
