import re
import sys
from collections import Counter

def colorize(lines):
    def bold(s):
        return '\x1b[1m{}\x1b[0m'.format(s)

    def red(s):
        return '\x1b[31m{}\x1b[0m'.format(s)

    def green(s):
        return '\x1b[32m{}\x1b[0m'.format(s)

    def yellow(s):
        return '\x1b[33m{}\x1b[0m'.format(s)

    def blue(s):
        return '\x1b[34m{}\x1b[0m'.format(s)

    def magenta(s):  # purple
        return '\x1b[35m{}\x1b[0m'.format(s)

    def cyan(s):
        return '\x1b[36m{}\x1b[0m'.format(s)

    def format_severity(txt, severity):
        """
        http://cppcheck.sourceforge.net/devinfo/doxyoutput/classSeverity.html
        enum:
            none, error, warning, style, performance,
            portability, information, debug
        """
        if severity == "none":
            return txt
        if severity == "error":
            return red(txt)
        if severity == "warning":
            return yellow(txt)
        if severity == 'style':
            return blue(txt)
        if severity == "performance":
            return cyan(txt)
        if severity == "portability":
            return magenta(txt)
        if severity == "information":
            return green(txt)
        if severity == "debug":
            return txt

        return txt

    re_message = re.compile(r'\[(?P<file>.*):(?P<line>.*?)\]:\((?P<severity>.*?)\),\[(?P<id>.*?)\],(?P<message>.*)')

    colored_lines = []
    matched_messages = []

    colored_lines = []
    matched_messages = []

    for line in lines:
        m = re_message.match(line)
        if m:
            d = m.groupdict()
            matched_messages.append(d)
        else:
            colored_lines.append(red(line))

    severity_order = ['error', 'warning', 'style', 'performance',
                      'portability', 'information', 'debug', 'none']

    counter = Counter(d['severity'] for d in matched_messages)
    summary_line = "\n\n==========================================\n"
    summary_line += "             {}:\n".format(bold(red("CPPCHECK Summary")))
    summary_line += "------------------------------------------"

    for severity in severity_order:
        n_severity = counter[severity]
        summary_line += "\n * "
        if n_severity:
            summary_line += format_severity(n_severity, severity)
        else:
            # summary_line += green("No {}(s)".format(severity))
            summary_line += green("No")
        summary_line += " {}(s)".format(format_severity(severity, severity))

    summary_line += "\n==========================================\n\n"

    # n_errors = counter['error']
    # if n_errors:
        # summary_line += red("{} Errors".format(n_errors))
    # else:
        # summary_line = green("No Errors")

    # n_warnings = counter['warning']
    # if n_errors:
        # summary_line += red("{} Errors".format(n_errors))
    # else:
        # summary_line = green("No Errors")

    # n_styles = counter['style']
    # n_performances = counter['performance']
    # n_portabilities = counter['portability']
    # n_informations = counter['information']


    # n_debugs = counter['debug']

    for d in sorted(matched_messages,
                    key=lambda d: severity_order.index(d['severity'])):

        f = d['file']
        line = d['line']
        severity = d['severity']
        iid = d['id']
        message = d['message']

        colored_lines.append(
            "[{f}:{line}]:({severity}),[{i}],{message}"
            .format(f=magenta(f),  # format_severity(f, severity),
                    line=green(line),
                    severity=format_severity(severity, severity),
                    i=bold(iid),
                    message=message))

    return colored_lines, summary_line


if __name__ == '__main__':
    with open('cppcheck.txt', 'r') as f:
        content = f.read()

    lines = content.splitlines()
    colored_lines, summary_line = colorize(lines)
    print(summary_line)
    # sys.stdout.writelines(colored_lines)
    print("\n".join(colored_lines))
