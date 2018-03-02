"""单元测试."""
from colorama import colorama_text, Fore


def setUpModule():
    with colorama_text():
        print(Fore.GREEN + 'text is green')
        print(Fore.RESET + 'text is back to normal')
        print('back to normal now')
    print("setUp unit test")


def tearDownModule():
    print("tearUp unit test")
