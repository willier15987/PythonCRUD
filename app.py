import sys
import CRUD


def InputAction():
    while True:

        sys.stdout.write('# ')
        sys.stdout.flush()

        user_input = input()
        args = InputSplit(user_input)
        if len(args) != 0:
            if args and args[0] == 'exit':
                break

            action = args[0]
            CRUD.action(action, args)


def InputSplit(inputString):
    args = inputString.split()

    mix = False
    sentence = ""
    commands = []
    for arg in args:
        if arg[0] == "‘":
            mix = True
            sentence = ""
        if mix:
            if sentence == "":
                start = 1
            else:
                start = 0

            if arg[len(arg)-1] == "’":
                sentence += arg[start:len(arg)-1]
                commands.append(sentence)
                mix = False
            else:
                sentence += arg[start:] + " "
        else:
            commands.append(arg)

    # print(commands)
    return commands


def fortest():
    while True:
        user_input = input()
        if user_input and user_input[0] == 'exit':
            break

        CRUD.action(user_input)


if __name__ == '__main__':
    CRUD.Init()
    InputAction()
