import prettytable as pt


class Templates:

    @classmethod
    def list(cls, data, default_cc_name):
        fields = ('Name', 'SHA', 'Date', 'Subject')
        tbl = cls._ptable(fields)
        for row in data:
            if (row['Name'] == default_cc_name):
                row['Name'] += '*'
            vals = (
                row['Name'],
                row['SHA'],
                row['Date'],
                row['Subject']
            )
            tbl.add_row(vals)
        return tbl

    @classmethod
    def status(cls, data, default_cc_name):
        fields = (
            'Name',
            'SHA',
            'Date',
            'Upstream SHA',
            'Upstream Date',
            'Commits behind',
        )
        tbl = cls._ptable(fields)
        for row in data:
            if (row['Name'] == default_cc_name):
                row['Name'] += '*'
            vals = (
                row['Name'],
                row['SHA'],
                row['Date'],
                row['upstream_sha'],
                row['upstream_date'],
                row['commits_behind'],
            )
            tbl.add_row(vals)
        return tbl

    @classmethod
    def _ptable(cls, fields):
        tbl = pt.PrettyTable(
            field_names=fields,
            border=False,
            hrules=pt.NONE,
            vrules=pt.NONE,
            left_padding_width=2,
            sortby='Name'
        )
        alignments = dict(zip(fields, len(fields) * ['l']))
        tbl.align.update(alignments)
        return tbl
