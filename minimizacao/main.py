def handle_input(print_vars=False):
    """Funcao que lida com a entrada do usuario (no formato do VPL) e retorna os valores necessarios 
    para a criacao do automato."""
    input_list = input().split(";")
    states_number: int = int(input_list[0])
    initial_state: str = input_list[1]
    final_states: list = input_list[2][1:-1].split(",")
    alphabet: list = input_list[3][1:-1].split(",")
    transitions: list[str] = input_list[4:]
    transitions = create_transitions_dict(transitions)
   
    if print_vars:
        print("Inputed states_number:", states_number)
        print("Inputed initial_state:", initial_state)
        print("Inputed final_states:", final_states)
        print("Inputed alphabet:", alphabet)
        print("Inputed transitions:", transitions)

    return states_number, initial_state, final_states, alphabet, transitions


def create_transitions_dict(transitions):
    """Cria uma lista de tuplas, em que cada tupla representa uma transicao do automato."""
    transitions_tuples = []
    for transition in transitions:
        transitions_tuples.append(tuple(transition.split(',')))
    
    transitions_dict = {}
    for transition in transitions_tuples:
        if (transition[0] not in transitions_dict):
            transitions_dict[transition[0]] = {
                transition[1]: transition[2]
            }
        else:
            if transition[1] not in transitions_dict[transition[0]]:
                transitions_dict[transition[0]][transition[1]] = transition[2]
            else:
                if transition[2] not in transitions_dict[transition[0]][transition[1]]:
                    transitions_dict[transition[0]][transition[1]] += transition[2]
        if transition[2] not in transitions_dict:
            transitions_dict[transition[2]] = {}
    
    return transitions_dict

def remove_unreachable_states(initial_state, final_states, transitions):
    """Esta funcao eh responsavel por remover os estados inalcancaveis do automato."""
    
    visited_states = [] # Cria-se uma lista de estados visitados.
    visited_states = visit_reachable_states(initial_state, transitions, visited_states) # Visita-se os estados alcancaveis a partir do estado inicial.
    states_number = len(visited_states) # O numero de estados do automato passa a ser o numero de estados visitados.
    
    for state in transitions.copy():
        if state not in visited_states:
            transitions.pop(state) # Remove-se as transicoes que envolvam estados inalcancaveis.
            if state in final_states:
                final_states.remove(state) # Remove-se os estados finais inalcancaveis.
    
    return states_number, visited_states, transitions

def visit_reachable_states(origin_state, transitions, visited_states):
    """Esta eh uma funcao recursiva que visita os estados alcancaveis a partir de um estado inicial."""
    
    visited_states.append(origin_state)
    for state in transitions[origin_state].values():
        if state not in visited_states:
            visit_reachable_states(state, transitions, visited_states)
    
    return visited_states

def remove_dead_states(states, final_states, transitions):
    """Esta funcao eh responsavel por remover os estados mortos do automato."""
    not_dead_states = []

    for state in states:
        visited_states = visit_reachable_states(state, transitions, [])
        for final_state in final_states:
            if final_state in visited_states:
                not_dead_states.append(state)
                break
    
    if len(not_dead_states) != len(states):
        transitions_without_dead_states = {state: {} for state in not_dead_states}
        for state in states:
            if state not in not_dead_states:
                for s, trans in transitions.items():
                        for symbol in trans.keys():
                            if transitions[s][symbol] in not_dead_states:
                                transitions_without_dead_states[s][symbol] = transitions[s][symbol]
    else:
        transitions_without_dead_states = transitions
        
    states_number = len(not_dead_states)

    return states_number, not_dead_states, transitions_without_dead_states

def remove_equivalent_states(states, final_states, alphabet, transitions):
    ec1 = final_states 
    ec2 = list(filter(lambda x : x in states and x not in final_states, states)) 
    equivalence_classes = [ec1, ec2]
    auxiliar_trans_dict = {state: {} for state in states}

    new_equivalence_classes_created = True
    while new_equivalence_classes_created:
        for class_ in equivalence_classes:
            equivalence_transitions = []
            new_equivalence_classes = []
            for state in class_:
                for symbol in alphabet:
                    try:
                        auxiliar_trans_dict[state][symbol] = verify_ec_of_state(transitions[state][symbol], 
                                                                                equivalence_classes)
                    except:
                        #print(f"Não há transições por {symbol} em {state}")
                        pass

                if auxiliar_trans_dict[state] not in equivalence_transitions:
                    equivalence_transitions.append(auxiliar_trans_dict[state])
                    new_equivalence_classes.append([state])
                else:
                    id = equivalence_transitions.index(auxiliar_trans_dict[state])
                    new_equivalence_classes[id].append(state)

            for ec in new_equivalence_classes:
                ec.sort()
                if ec not in equivalence_classes:
                    equivalence_classes = [oec for oec in equivalence_classes if ec[0] not in oec]
                    equivalence_classes.append(ec)
                    new_equivalence_classes_created = True
                else:
                    new_equivalence_classes_created = False
    
    for c in equivalence_classes:
        if len(c) > 1:
            for state in c[1:]:
                transitions.pop(state)
                for s, trans in transitions.items():
                    for symbol in trans.keys():
                        if transitions[s][symbol] == state:
                            transitions[s][symbol] = c[0]
                if state in final_states:
                    final_states.remove(state)

    states_number = len(equivalence_classes)

    return  states_number, equivalence_classes, final_states, transitions

def verify_ec_of_state(state, equivalence_classes):
    for i in range(len(equivalence_classes)):
        if state in equivalence_classes[i]:
            return i
    return -1

def create_initial_state_string(initial_state):
    initial_state_strng = initial_state
    
    return initial_state_strng

def create_final_states_string(final_states):
    final_states_string = "{"
    for state in final_states:
        if state == final_states[-1]:
            final_states_string += (state + "}")
        else:
            final_states_string += (state + ",")
    
    return final_states_string

def create_alphabet_string(alphabet):
    alphabet_string = "{"
    for symbol in alphabet:
        if symbol == alphabet[-1]:
            alphabet_string += symbol + "}"
        else:
            alphabet_string += symbol + ","
            
    return alphabet_string

def create_transitions_string(transitions):
    transitions_string = ""
    list_ordered = []
    for state in transitions.keys():
        list_ordered.append(state)
    list_ordered.sort()
    
    for state in list_ordered:
        for key, value in transitions[state].items():
            transitions_string +=  f"{state},{key},{value};"
    transitions_string = transitions_string[:-1]
    
    return transitions_string

def print_final_result(states_number, initial_state, final_states, alphabet, transitions, print_formated=False):
    if print_formated:
        print("Outputed states number:", states_number)
        print("Outputed final initial state:", initial_state)
        print("Outputed final states:", final_states)
        print("Outputed Alphabet:", alphabet)
        print("Outputed Transitions:", transitions)

    states_number_string = str(states_number)
    initial_state_string = create_initial_state_string(initial_state)
    final_states_string = create_final_states_string(final_states)
    alphabet_string = create_alphabet_string(alphabet)
    transitions_string = create_transitions_string(transitions)
    
    return(states_number_string + ";" + initial_state_string + ";" + final_states_string + ";" + alphabet_string + ";" + transitions_string)
    
if __name__ == "__main__":
    states_number, initial_state, final_states, alphabet, transitions = handle_input(print_vars=False)
    states_number, states, transitions = remove_unreachable_states(initial_state, final_states, transitions)
    states_number, states, transitions = remove_dead_states(states, final_states, transitions)
    states_number, states, final_states, transitions = remove_equivalent_states(states, final_states, alphabet, transitions)
    print(print_final_result(states_number, initial_state, final_states, alphabet, transitions, False))
