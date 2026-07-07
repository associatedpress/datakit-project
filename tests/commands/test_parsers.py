from datakit_project import Create, Templates, TemplatesUpdate
from datakit_project.commands.help_text import CREATE_HELP_MSG


def test_create_parser_defaults():
    args = Create(None, None).get_parser('project create').parse_args([])
    assert args.template == ''
    assert args.make_default is False
    assert args.interactive is False
    assert args.no_input is False
    assert args.overwrite_if_exists is False
    assert args.checkout is None


def test_create_parser_all_flags():
    parser = Create(None, None).get_parser('project create')
    args = parser.parse_args(
        ['-t', 'gh:ap/tmpl', '-d', '-i', '-n', '-o', '-c', 'main']
    )
    assert args.template == 'gh:ap/tmpl'
    assert args.make_default is True
    assert args.interactive is True
    assert args.no_input is True
    assert args.overwrite_if_exists is True
    assert args.checkout == 'main'


def test_create_epilog_is_help_text():
    assert Create(None, None).get_epilog() == CREATE_HELP_MSG


def test_templates_parser_status_flag():
    parser = Templates(None, None).get_parser('project templates')
    assert parser.parse_args([]).status is False
    assert parser.parse_args(['-s']).status is True


def test_templates_update_parser_builds():
    # No custom arguments; exercising the parser guards against regressions.
    assert TemplatesUpdate(None, None).get_parser('project templates update') is not None
