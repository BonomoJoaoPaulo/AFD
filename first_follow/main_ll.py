"""
Trabalho desenvolvido em grupo por:
- João Paulo Araujo Bonomo   (21100133)
- João Victor Volpato        (21105481)
- Rodrigo Santos de Carvalho (21100139)

Nos disponibilizamos para explicar o código e o raciocínio utilizado para a resolução do problema.
"""

def process_input(input: str):
    """
    Função que processa a entrada e retorna um dicionário com as produções,
    uma lista com os não terminais e uma lista com os terminais
    """
    symbols_to_ignore = [' ', '=', ';', '&']
    non_terminals = []
    terminals = ['&']

    for char in input:
        if char.capitalize() == char and char not in symbols_to_ignore:
            non_terminals.append(char)
        elif char not in symbols_to_ignore:
            terminals.append(char)
            
     # Criamos uma lista para não terminais e terminais
    terminals = list(set(terminals))
    non_terminals = list(set(non_terminals))

    list_input = input[:-1].split('; ') # Pegamos apenas as produções da gramática de entrada
    productions_dict = {}

    for production in list_input:
        if production[0] not in productions_dict:
            productions_dict[production[0]] = [production[4:]]
        else:
            productions_dict[production[0]].append(production[4:])
            
    #print(non_terminals)
    #print(terminals)
    #print(productions_dict)

    return productions_dict, non_terminals, terminals


def verify_left_recursion(productions: dict, non_terminals: list) -> tuple[bool, str]:
    """
    Função que verifica se a gramática possui recursão à esquerda direta e indireta
    """
    for key, values in productions.items():
        for value in values:
            if value[0] in non_terminals:
                if key == value[0]: # Recursão à esquerda direta
                    return True, 'direta'
                else:
                    for i_prod in productions[value[0]]:
                        if key == i_prod[0]: # Recursão à esquerda indireta
                            return True, 'indireta'

    return False, ''


def verify_non_determinism(productions: dict, non_terminals: list) -> tuple[bool, str]:
    """
    Função que verifica se a gramática é não determinística
    """
    for key, values in productions.items():
        key_alfas = []
        for value in values:
            if value[0] in key_alfas:
                return True, 'diretamente'
            else:
                key_alfas.append(value[0])

            if value[0] in non_terminals:
                for i_prod in productions[value[0]]:
                        if i_prod[0] in key_alfas:
                            return True, 'indiretamente'
                        else:
                            key_alfas.append(i_prod[0])

    return False, ''

def calculate_first_set(productions: dict, non_terminals: list, terminals: list) -> dict:
    """
    Para todo X ∈ (T U N ), o FIRST(X) é obtido pela aplicação das
    seguintes regras: (até não haver mais terminais ou ε que possam ser
    acrescentados a algum dos conjuntos FIRST)

    1. Se X ∈ terminais então FIRST(X) ={X}
    
    2. Se X ∈ não terminais então
        (a): Se X ::= aY ∈ P, então a ∈ FIRST(X)
        (b): Se X ::= ε ∈ P, então ε ∈ FIRST(X)
        (c) Se X ::= Y1 Y2 ...Yk ∈ P , então FIRST(Y1 ) ∈ FIRST(X)
            i. Se ε ∈ FIRST(Y1), então FIRST(Y2 ) ∈ FIRST(X)
            ii. Se ε ∈ FIRST(Y2), ...
            iii. Se ε ∈ FIRST(Yk) e ... e ε ∈ FIRST(Y1) , então ε ∈ FIRST(X)
    """
    first_set = {}
    for key, values in productions.items():
        first = calculate_first(key, productions, terminals, non_terminals)  
        #print(key, "->", first)      
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
    #print("Calculating FIRST for", x)
    for production in productions[x]:
            if production[0] in terminals: # 1 - Se X ∈ terminais
                x_first.append(production[0])
            else: # 2 - Se X ∈ não terminais
                a = verify_case_a(production[0], productions, terminals, non_terminals)
                x_first.extend(a)
                # Não é preciso verificar o caso B, pois estamos considerando que ε é um terminal,
                # então ele já foi adicionado no FIRST No if anterior.
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
                                x_first.extend(calculate_first(production[i+1], productions, terminals, non_terminals))
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


def calculate_follow_set(inputed_grammar: str, productions: dict, first_set: list,
                         non_terminals: list, terminals: list) -> list:
    """
    Para calcular o FOLLOW(A) para todos os não-terminais A, aplique as seguintes regras,
    até que nada mais possa ser acrescentado a nenhum dos conjuntos FOLLOW

    1. Se S é o símbolo inicial da gramática, então $ ∈ FOLLOW(S)

    2. Se A ::= αBβ ∈ P e β != ε, então adicione FIRST(β) em FOLLOW(B)

    3. Se A ::= αB (ou A ::= αBβ, onde ε ∈ FIRST(β)) ∈ P , então adicione FOLLOW(A) em FOLLOW(B)
        - FIRST(β) → FIRST(da sequência β)
    """
    follow_list = {non_terminal : [] for non_terminal in non_terminals}
    j = 0
    while j < len(productions):
        for key, values in productions.items():
            if key == inputed_grammar[0]:
                follow_list[key].append('$')

            for value in values:
                #print(key, "->", value)
                for i in range(0, len(value) - 1):
                    if value[i] in non_terminals:
                        if value[i+1] in terminals and value[i+1] != "&":
                            #print("2 - Adding", value[i+1], f"to FOLLOW({value[i]}) because of terminal after {value[i]}")
                            follow_list[value[i]].append(value[i+1])
                        elif value[i+1] in non_terminals:
                            follow_list[value[i]].extend(first_set[value[i+1]])
                            #print("2 - Adding", first_set[value[i+1]], 
                            #      f"to FOLLOW({value[i]}) because of non-terminal {value[i+1]} after {value[i]}")
                            if "&" in first_set[value[i+1]] and i <= len(value) - 3:
                                if value[i+2] in terminals:
                                    follow_list[value[i]].append(value[i+2])
                                    #print("2.1.1 - Adding", value[i+2], f"to FOLLOW({value[i]}) because of terminal after {value[i+1]}")
                                elif value[i+2] in non_terminals:
                                    follow_list[value[i]].extend(first_set[value[i+2]])
                                    #print("2.1.2 - Adding", first_set[value[i+2]], f"to FOLLOW({value[i]}) because of & in FIRST({value[i+1]})")
                        else:
                            pass

                for i in range(0, len(value)):
                    if value[i] in non_terminals:
                        #print(key, "->", value, "value[i]: ", value[i])
                        if "&" in first_set[value[i]] and i == (len(value) - 1):
                            follow_list[value[i]].extend(follow_list[key])
                            #print("3.1 - Adding", follow_list[key], f"to FOLLOW({value[i]}) because of & in FIRST({value[i]})")
                        if i < (len(value) - 1):
                            if value[i+1] in terminals:
                                follow_list[value[i]].append(value[i+1])
                                #print("3.2 - Adding", value[i+1], f"to FOLLOW({value[i]}) because of terminal after {value[i]}")
                            elif value[i+1] in non_terminals and "&" in first_set[value[i+1]]:
                                follow_list[value[i]].extend(follow_list[key])
                                #print("3.3 - Adding", follow_list[key], f"to FOLLOW({value[i]}) because of & in FIRST({value[i+1]})")
        j += 1


    # APENAS PARA REMOVER ELEMENTOS REPETIDOS E DEIXAR EM ORDEM
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
    

def calculate_parsing_table(productions_dict: dict, first_set: dict, 
                            follow_list: dict, non_terminals: list, terminals: list) -> dict:
    """
    Função que calcula a tabela de parsing de acordo com o passo a passo do algoritmo:
        Step 1:
            For each production A → α , of the given grammar perform Step 2 and Step 3.  
        Step 2:
            For each terminal symbol 'a' in FIRST(α),
            ADD A → α in table T[A,a], where 'A' determines row & 'a' determines column.
        Step 3: 
            If ε is present in FIRST(α) then find FOLLOW(A),
            ADD A → ε, at all columns 'b', where 'b' is FOLLOW(A).  (T[A,b])
        Step 4:
            If ε is in FIRST(α) and $ is the FOLLOW(A), ADD A → α to T[A,$].
    """
    parsing_table = {}
    for non_terminal, productions in productions_dict.items():
        for production in productions:
                if production[0] in non_terminals:
                    for a in first_set[production[0]]:
                        if a != '&':
                            parsing_table[(non_terminal, a)] = (non_terminal, production)

                    if '&' in first_set[production[0]]:
                        for i in range(0, len(production)):
                            for b in first_set[production[i]]:
                                if b != '&':
                                    parsing_table[(non_terminal, b)] = (non_terminal, production)
                            if '&' not in first_set[production[i]]:
                                break
                            elif i == len(production) - 1:
                                for c in follow_list[non_terminal]:
                                    parsing_table[(non_terminal, c)] = (non_terminal, production)

                elif production[0] == '&':
                    for d in follow_list[non_terminal]:
                        parsing_table[(non_terminal, d)] = (non_terminal, production)

                else:
                    parsing_table[(non_terminal, production[0])] = (non_terminal, production)

    return parsing_table

 
def adjust_output(first_set: dict, follow_list: dict, non_terminals: list,
                  terminals, parsing_table, inputed_grammar: str) -> str:
    """
    Função que ajusta a saída para o formato do VPL
    """
    output = "{"
    
    aux_nt = []
    for non_terminal in non_terminals:
        aux_nt.append(non_terminal.lower())
    aux_nt.sort()   
    non_terminals = [x.upper() for x in aux_nt]
    
    for non_terminal in non_terminals:
        output += f'{non_terminal},'
    output = output[:-1]
    output += "},"
    
    non_terminals_ordened = order_non_terminals(non_terminals, inputed_grammar)
    output += non_terminals_ordened[0] + ','
    
    output += "{"
    if '&' in terminals:
        terminals.remove('&')
    terminals.sort()
    terminals.append('$')

    for terminal in terminals:
        output += f"{terminal},"
    output = output[:-1]
    output += "};"
    
    ordered_transitions = order_transitions(parsing_table)
    for non_terminal in non_terminals:
        for terminal in terminals:
            for key, value in parsing_table.items():
                if key[0] == non_terminal and key[1] == terminal:
                    output += f"[{key[0]},{key[1]},{ordered_transitions.index(value) + 1}]"

    return output


def order_non_terminals(non_terminals: list, grammar: str):
    grammar_splitted = grammar.split("; ")
    #print(grammar_splitted)
    aux = []
    for a in grammar_splitted:
        if a[0] in non_terminals and a[0] not in aux:
            aux.append(a[0])
    non_terminals = aux

    return non_terminals

def order_transitions(parsing_table: dict):
    ordered_transitions = []
    for transition in parsing_table.values():
        if transition not in ordered_transitions:
            ordered_transitions.append(transition)
    
    return ordered_transitions

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

    left_recursion_bool, left_recursion_type = verify_left_recursion(productions_dict, non_terminals)
    if left_recursion_bool:
        print(f"ERRO: A gramática de entrada possui recursão à esquerda {left_recursion_type}.")
        exit()

    verify_non_determinism_bool, non_determinism_type = verify_non_determinism(productions_dict, non_terminals)
    if verify_non_determinism_bool:
        print(f"ERRO: A gramática de entrada é não determinística {non_determinism_type}.")
        exit()

    first_set = calculate_first_set(productions_dict, non_terminals, terminals)
    follow_list = calculate_follow_set(inputed_grammar, productions_dict, first_set, non_terminals, terminals)

    parsing_table = calculate_parsing_table(productions_dict, first_set, follow_list, non_terminals, terminals)

    output = adjust_output(first_set, follow_list, non_terminals, terminals, parsing_table, inputed_grammar)
    print(output)
