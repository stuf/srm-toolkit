import logging


def setup_logger(logger: logging.Logger):
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(fmt='{name:.<12} {levelname:>5} | {message}',
                                  style='{')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)


def set_loglevel(logger: logging.Logger, verbose: bool):
    print(f'set loglevel {verbose=}')
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)


def pluralize(n: int, noun: str):
    return f'{n} {noun}{"s"[:n^1]}'
