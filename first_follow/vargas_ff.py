def process_input(input: str):
    symbols_to_ignore = [' ', '=', ';', '&']
    non_terminals = []
    terminals = ['&']

    for char in input:
        if char.capitalize() == char and char not in symbols_to_ignore:
            non_terminals.append(char)
        elif char not in symbols_to_ignore:
            terminals.append(char)

    terminals = list(set(terminals))
    non_terminals = list(set(non_terminals))

    list_input = input[:-1].split('; ')
    productions_dict = {}

    for production in list_input:
        if production[0] not in productions_dict:
            productions_dict[production[0]] = [production[4:]]
        else:
            productions_dict[production[0]].append(production[4:])

    return productions_dict, non_terminals, terminals


def verify_left_recursion(productions: dict, non_terminals: list):
    for key, values in productions.items():
        for value in values:
            if value[0] in non_terminals:
                if key == value[0]:
                    return True
                else:
                    for i_prod in productions[value[0]]:
                        if key == i_prod[0]:
                            return True
    return False


def verify_non_determinism(productions: dict, non_terminals: list):
    for key, values in productions.items():
        key_alfas = []
        for value in values:
            if value[0] in key_alfas:
                return True
            else:
                key_alfas.append(value[0])

            if value[0] in non_terminals:
                for i_prod in productions[value[0]]:
                    if i_prod[0] in key_alfas:
                        return True
                    else:
                        key_alfas.append(i_prod[0])

    return False


def calculate_first_set(productions: dict, non_terminals: list, terminals: list) -> dict:
    first_set = {}
    for key, values in productions.items():
        first = calculate_first(key, productions, terminals, non_terminals)
        first_set[key] = list(set(first))

    auxiliar_dict = {}
    for key, values in first_set.items():
        new_values = list(set(values))
        if "&" in new_values:
            new_values.remove("&")
            new_values.sort()
            new_values.append("&")
        auxiliar_dict[key] = new_values
    first_set = auxiliar_dict

    return first_set


def calculate_first(x, productions, terminals, non_terminals):
    x_first = []
    for production in productions[x]:
        if production[0] in terminals:
            x_first.append(production[0])
        else:
            a = verify_case_a(production[0], productions, terminals, non_terminals)
            x_first.extend(a)
            for i in range(0, len(production)):
                c = verify_case_c(production[i], productions, terminals, non_terminals)
                if c[0]:
                    if i == len(production) - 1:
                        x_first.append('&')
                    else:
                        if c[1] != '':
                            x_first.extend(calculate_first(production[i], productions, terminals, non_terminals))
                            x_first.extend(calculate_first(c[1], productions, terminals, non_terminals))
                            break
                        else:
                            x_first.extend(calculate_first(production[i + 1], productions, terminals, non_terminals))
                            x_first.extend(calculate_first(production[i], productions, terminals, non_terminals))
                else:
                    break
    return x_first


def verify_case_a(x, productions, terminals, non_terminals):
    non_terminals_to_return = []
    for production in productions[x]:
        if production[0] in terminals:
            non_terminals_to_return.append(production[0])
    return non_terminals_to_return


def verify_case_c(x, productions, terminals, non_terminals):
    if '&' in productions[x]:
        return True, ''
    for production in productions[x]:
        production_void_count = 0
        for i in range(0, len(production)):
            if production[i] in non_terminals:
                if '&' in productions[production[i]]:
                    production_void_count += 1
        if production_void_count == len(production):
            return True, ''
        if production[0] in non_terminals:
            return True, production[0]
    return False, ''


def calculate_follow_set(inputed_grammar: str, productions: dict, first_set: list, non_terminals: list, terminals: list) -> list:
    follow_list = {non_terminal: [] for non_terminal in non_terminals}
    j = 0
    while j < len(productions):
        for key, values in productions.items():
            if key == inputed_grammar[0]:
                follow_list[key].append('$')

            for value in values:
                for i in range(0, len(value) - 1):
                    if value[i] in non_terminals:
                        if value[i + 1] in terminals and value[i + 1] != "&":
                            follow_list[value[i]].append(value[i + 1])
                        elif value[i + 1] in non_terminals:
                            follow_list[value[i]].extend(first_set[value[i + 1]])
                            if "&" in first_set[value[i + 1]] and i <= len(value) - 3:
                                if value[i + 2] in terminals:
                                    follow_list[value[i]].append(value[i + 2])
                                elif value[i + 2] in non_terminals:
                                    follow_list[value[i]].extend(first_set[value[i + 2]])
                        else:
                            pass

                for i in range(0, len(value)):
                    if value[i] in non_terminals:
                        if "&" in first_set[value[i]] and i == (len(value) - 1):
                            follow_list[value[i]].extend(follow_list[key])
                        if i < (len(value) - 1):
                            if value[i + 1] in terminals:
                                follow_list[value[i]].append(value[i + 1])
                            elif value[i + 1] in non_terminals and "&" in first_set[value[i + 1]]:
                                follow_list[value[i]].extend(follow_list[key])
        j += 1

    auxiliar_dict = {}
    for key, values in follow_list.items():
        new_values = list(set(values))
        if "&" in new_values:
            new_values.remove("&")
        if "$" in new_values:
            new_values.remove("$")
            new_values.sort()
            new_values.append("$")
        auxiliar_dict[key] = new_values
    follow_list = auxiliar_dict

    return follow_list


def adjust_output(first_set: dict, follow_list: dict, non_terminals: list, inputed_grammar: str) -> str:
    output = ""
    non_terminals_ordened = order_non_terminals(non_terminals, inputed_grammar)
    for non_terminal in non_terminals_ordened:
        output += f"First({non_terminal}) = " + "{" f"{get_list_formated(non_terminal, first_set)}" + "}; "
    for non_terminal in non_terminals_ordened:
        output += f"Follow({non_terminal}) = " + "{" f"{get_list_formated(non_terminal, follow_list)}" + "}; "

    return output


def order_non_terminals(non_terminals: list, grammar: str):
    grammar_splitted = grammar.split("; ")
    aux = []
    for a in grammar_splitted:
        if a[0] in non_terminals and a[0] not in aux:
            aux.append(a[0])
    non_terminals = aux

    return non_terminals


def get_list_formated(non_terminal, list):
    list_formated = ""
    for n in list[non_terminal]:
        list_formated += f"{n}, "
    return list_formated[:-2]


if __name__ == '__main__':
    inputed_grammar = input()
    if inputed_grammar[0] == " ":
        inputed_grammar = inputed_grammar[1:]

    productions_dict, non_terminals, terminals = process_input(inputed_grammar)

    left_recursion = verify_left_recursion(productions_dict, non_terminals)
    if left_recursion:
        print(f"ERRO: A gramática de entrada possui recursão à esquerda.")
        exit()

    non_determinism = verify_non_determinism(productions_dict, non_terminals)
    if non_determinism:
        print(f"ERRO: A gramática de entrada é não determinística.")
        exit()

    first_set = calculate_first_set(productions_dict, non_terminals, terminals)
    follow_list = calculate_follow_set(inputed_grammar, productions_dict, first_set, non_terminals, terminals)

    output = adjust_output(first_set, follow_list, non_terminals, inputed_grammar)
    print(output)
