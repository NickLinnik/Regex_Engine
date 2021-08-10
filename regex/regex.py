import sys
sys.setrecursionlimit(10000)


def main(regex_string):
    regex, string = regex_string.split('|')
    return match(regex, string)


def match(regex: str, string: str, empty_string_case=False):
    if not regex:
        return True
    if empty_string_case:
        return False
    if regex[0] == '^':
        return fullmatch(regex[1:], string)

    return fullmatch(regex, string) or \
        match(regex, string[1:], False if string else True)


def fullmatch(regex: str, string: str):
    if not regex or regex[0] == '$' and not string:
        return True

    this_match = False
    char = regex[0]
    is_escape_sequence = regex[:1] == '\\'
    if is_escape_sequence:
        regex = regex[1:]
    elif regex[1:] and regex[1] in {'?', '*', '+'}:
        def metachar_match(metachar):
            repeats = len(string) if char == '.' else \
                len(string) - len(string.lstrip(char)) + 1

            repeats_dict = {
                '?':  1 if repeats == 0 else
                repeats if repeats < 3 else 2,
                '*': 1 if repeats == 0 else repeats,
                '+': repeats
            }

            for i in range(1 if metachar == '+' else 0, repeats_dict[metachar]):
                alternative_match = fullmatch(regex[2:], string[i:])
                if alternative_match:
                    return True
            return False

        if metachar_match(regex[1]):
            return True

    if char and string:
        this_match = regex[0] == string[0] or (regex[0] == '.' if not is_escape_sequence else False)

    return False if not this_match else fullmatch(regex[1:], string[1:])


if __name__ == '__main__':
    print(main(input()))
