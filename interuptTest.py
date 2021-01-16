import signal


class Interrupt(BaseException):
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
    raise Interrupt("test")

signal.signal(signal.SIGALRM, interrupted)
s = 1
def test():
    while s != '0':
        signal.alarm(1)
        try:
            s = input("::>")
        except Interrupt:
            return False
            break


print("end")