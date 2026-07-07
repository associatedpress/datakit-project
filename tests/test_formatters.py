from datakit_project.formatters.templates import Templates


def test_list_marks_default_template():
    data = [
        {'Name': 'fake-repo', 'SHA': 'a11706f', 'Date': '2017-02-02', 'Subject': 'x'},
        {'Name': 'other', 'SHA': '55f62a0', 'Date': '2019-03-06', 'Subject': 'y'},
    ]
    tbl = Templates.list(data, default_cc_name='fake-repo')
    rendered = tbl.get_string()
    assert 'fake-repo*' in rendered
    assert 'other ' in rendered


def test_status_marks_default_template():
    data = [{
        'Name': 'fake-repo', 'SHA': 'a11706f', 'Date': '2017-02-02', 'Subject': 'x',
        'upstream_sha': 'c18705e', 'upstream_date': '2017-06-01', 'commits_behind': 3,
    }]
    tbl = Templates.status(data, default_cc_name='fake-repo')
    assert 'fake-repo*' in tbl.get_string()


def test_list_leaves_names_unmarked_when_no_default():
    data = [
        {'Name': 'fake-repo', 'SHA': 'a11706f', 'Date': '2017-02-02', 'Subject': 'x'},
    ]
    tbl = Templates.list(data, default_cc_name=None)
    assert 'fake-repo*' not in tbl.get_string()
