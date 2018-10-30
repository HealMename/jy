class Four(object):
    regex = '^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$'

    def to_python(self, values):
        return int(values)

    def to_url(self, values):
        return '%s' % values