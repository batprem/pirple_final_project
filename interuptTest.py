import signal


class Interupt(BaseException):
    """
    Help interuption
    """
    pass


def interrupted(signum, frame):
    """

    :param signum:
    :param frame:
    :return:
    """
    print("Timeout!")
    raise Interupt("test")

signal.signal(signal.SIGALRM, interrupted)
s = 1
while s != '0':
    signal.alarm(1)
    try:
        s = input("::>")
    except Interupt:
        print("You are interrupted.")
