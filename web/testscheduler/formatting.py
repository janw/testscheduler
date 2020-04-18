import pygments
import pygments.formatters
import pygments.lexers

lexer = pygments.lexers.get_lexer_by_name("ansi-color")
formatter = pygments.formatters.HtmlFormatter(linenos=True)


def format_logs(logs):
    return pygments.highlight(logs, lexer, formatter)
