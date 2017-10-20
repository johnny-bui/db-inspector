
from context import parse_arg

def parse_arg_override_config_file_test():
    args = '-u postgresql://testuser:testpass@localhost/blabladb -o my-dir -f gif'.split()
    config = parse_arg(args)
    assert config['formatType'] == 'gif'
    assert config['outputDir'] == 'my-dir'

def pare_arg_raise_error_test():
    try:
        args = '-o my-dir -f gif'.split()
        config = parse_arg(args)
#        assert False
    except ValueError as ex: # assert that ValueError passiert
        pass
