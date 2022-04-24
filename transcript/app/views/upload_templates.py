from pyexcel_webio import make_response_from_array

from transcript.app.views import app


@app.route('/templates/courses')
def course_template():
    headers = [[
        'Title',
        'Abbr',
        'Code',
        'Course Type',
        'Credit Hours',
        'Programme',
        'Semester'
    ]]
    output = make_response_from_array(headers, 'csv', file_name='course-template')
    return output


@app.route('/templates/programme')
def programme_template():
    headers = [[
        'Title',
        'Abbr',
        'Code',
        'Course Type',
        'Credit Hours',
        'Programme',
        'Semester'
    ]]
    output = make_response_from_array(headers, 'csv', file_name='programme-template')
    return output
