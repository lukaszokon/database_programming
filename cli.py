import os, earnings_calculation


def print_main_menu():
    while 1:
        os.system('cls')
        print("Witamy w super programie do obliczania listy płac")
        print("a - zarządzanie pracownikami")
        print("b - zarządzanie stanowiskami")
        print("c - zarzadzanie etatami")
        print("d - generowanie listy płac")
        print("q - wyjdź z programu")

        c = input("Wpisz literę wybranej funkcji: ")
        if c == 'q':
            return
        elif c == 'a':
            print_workers_menu()
        elif c == 'b':
            print_jobs_menu()
        elif c == 'c':
            print_etaty_menu()
        elif c == 'd':
            earnings_list_generate()


def earnings_list_generate():
    month = int(input("Wpisz numer miesiąca: "))
    year = int(input("Wpisz numer roku: "))
    earnings_calculation.print_earnings(month, year)


def print_workers_menu():
    os.system('cls')
    print("c - dodaj pracownika")
    print("d - usuń pracownika")
    print("u - edytuj pracownika")


def print_jobs_menu():
    os.system('cls')
    print("c - dodaj stanowisko")
    print("d - usuń stanowisko")
    print("u - edytuj stanowisko")


def print_etaty_menu():
    os.system('cls')
    print("c - dodaj etat")
    print("d - usuń etat")
    print("u - edytuj etat")
