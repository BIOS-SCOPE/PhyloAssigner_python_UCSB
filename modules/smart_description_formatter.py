
# creates a class. Imported into pythonassigner_v0.9.py script, to format usage/help message description

import argparse

class SmartDescriptionFormatter(argparse.RawDescriptionHelpFormatter):
    def _fill_text(self, text, width,
                   indent):  # RawDescriptionHelpFormatter, although function name might change depending on Python
        if text.startswith('R|'):
            paragraphs = text[2:].splitlines()
            rebroken = [argparse._textwrap.wrap(tpar, width) for tpar in paragraphs]
            rebrokenstr = []
            for tlinearr in rebroken:
                if (len(tlinearr) == 0):
                    rebrokenstr.append("")
                else:
                    for tlinepiece in tlinearr:
                        rebrokenstr.append(tlinepiece)
            return '\n'.join(rebrokenstr)  # (argparse._textwrap.wrap(text[2:], width))
        return argparse.RawDescriptionHelpFormatter._fill_text(self, text, width, indent)
