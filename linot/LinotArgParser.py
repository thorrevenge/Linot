from __future__ import print_function
from argparse import SUPPRESS


class LinotArgParser:

    def __init__(self, subcmd, sub_cmd_parser, default_process):
        ap = sub_cmd_parser.add_parser(subcmd, add_help=False)
        self._arg_parser = ap.add_mutually_exclusive_group()
        self._subcmd = subcmd
        self._default_process = default_process
        self._arg_list = {}
        self._arg_parser.set_defaults(proc=self._processArgs)
        self.add_argument('-h', '--help',  action='store_true', func=self.print_help, help='show command list')

    def add_argument(self, *args, **kwargs):
        if 'dest' in kwargs:
            raise ValueError('"dest" is forbidden for plugin argument')
        if 'func' in kwargs:
            func = kwargs['func']
            kwargs.pop('func')
        else:
            func = None
        for arg_str in args:
            # we dont accept positional args
            if not arg_str.startswith(self._arg_parser.prefix_chars):
                raise ValueError('supports only optional args starts with ' +
                                 self._arg_parser.prefix_chars)
            option = arg_str.lstrip(self._arg_parser.prefix_chars)
            self._arg_list[option] = {}
            self._arg_list[option]['func'] = func
            self._arg_list[option]['arg'] = arg_str
            if 'help' in kwargs:
                self._arg_list[option]['help'] = kwargs['help']
            else:
                self._arg_list[option]['help'] = ''
        self._arg_parser.add_argument(*args, **kwargs)

    def _processArgs(self, input_args, sender):
        for args in self._arg_list:
            value = getattr(input_args, args, None)
            if value is not None and value is not False:
                func = self._arg_list[args]['func']
                if func is not None:
                    func(getattr(input_args, args), sender)
                else:
                    self._default_process(input_args, sender)

    def print_help(self, args, sender=None):
        print('[{} command list]'.format(self._subcmd))
        # TODO fix this ....
        print('{} {}'.format(self._subcmd, '-h/--help'))
        print('>> show this command list.')
        print('-----')
        for arg in self._arg_list:
            if self._arg_list[arg]['help'] is SUPPRESS:
                continue
            if arg == 'help' or arg == 'h':
                continue
            help_text = self._arg_list[arg]['help']
            print('{} {}'.format(self._subcmd, self._arg_list[arg]['arg']))
            if help_text != '':
                print('>> '+help_text)
            print('-----')
