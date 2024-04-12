def handle_input():
    """Handle input from the user."""
    while True:
        input_list = input().split(";")
        states_number: int = int(input_list[0])
        initial_state: str = input_list[1]
        final_states: list = input_list[2][1:-1].split(",")
        alphabet: list = input_list[3][1:-1].split(",")
        transitions: list[str] = input_list[4:]
        transitions: list[tuple[str, str, str]] = create_transitions_tuples(transitions)
        if type(states_number) == int:
            break

    print("Inputed states_number:", states_number)
    print("Inputed initial_state:", initial_state)
    print("Inputed final_states:", final_states)
    print("Inputed alphabet:", alphabet)
    print("Inputed transitions:", transitions)

    return states_number, initial_state, final_states, alphabet, transitions

def create_transitions_tuples(transitions: list[str]) -> list[tuple[str, str, str]]:
    """Create a list of tuples from the transitions list."""
    transitions_tuples = []
    for transition in transitions:
        transitions_tuples.append(tuple(transition.split(',')))
    return transitions_tuples

def verify_transitions(transitions):
    transitions_dict = {}
    for transition in transitions:
        if (transition[0] not in transitions_dict):
            transitions_dict[transition[0]] = {
                transition[1]: transition[2]
            }
            print(f"TRANSIÇÃO ADICIONADA: {transition[0]} -> {transition[1]} -> {transition[2]}")
        else:
            if transition[1] not in transitions_dict[transition[0]]:
                print(f"TRANSIÇÃO ADICIONADA em elseif: {transition[0]} -> {transition[1]} -> {transition[2]}")
                transitions_dict[transition[0]][transition[1]] = transition[2]
            else:
                if transition[2] not in transitions_dict[transition[0]][transition[1]]:
                    print(f"TRANSIÇÃO ADICIONADA em elseelseif: {transition[0]} -> {transition[1]} -> {transition[2]}")
                    transitions_dict[transition[0]][transition[1]] += transition[2]
        if transition[2] not in transitions_dict:
            transitions_dict[transition[2]] = {}
    print(transitions_dict)
    return transitions_dict

def determine_automato(states_number, initial_state, final_states, alphabet, transitions):
    new_transitions = {}
    for state, trans in transitions.items():
        for transition, destiny_states in trans.items():
            if len(destiny_states) > 1:
                #print(f"({state}, {transition}) -> {destiny_states}")
                new_transitions[destiny_states] = {}
                for destiny_state in destiny_states:
                    for tr in transitions[destiny_state]:
                        if tr not in new_transitions[destiny_states]:
                            new_transitions[destiny_states][tr] = transitions[destiny_state][tr]
                        else:
                            try:
                                if transitions[destiny_state][tr] not in new_transitions[destiny_states][tr]:
                                    new_transitions[destiny_states][tr] += transitions[destiny_state][tr]
                            except:
                                print(f"Transição de {destiny_state} por {tr} não existe")
                
    for keys, values in new_transitions.items():
        transitions[keys] = values
    
    return transitions

def mark_final_states(final_states, transitions):
    new_fs = final_states.copy()
    for transition in transitions.values():
        for destiny_state in transition.values():
            for fs in final_states:
                if fs in destiny_state:
                    if destiny_state not in new_fs:
                        new_fs.append(destiny_state)

    return new_fs

def remove_unreachable_states(states_number, initial_state, final_states, alphabet, transitions):
    visited_states = []
    visited_states = visit_reachable_states(initial_state, transitions, visited_states)
    
    for state in transitions.copy():
        if state not in visited_states:
            transitions.pop(state)
            if state in final_states:
                final_states.remove(state)
    
    return transitions

def visit_reachable_states(origin_state, transitions, visited_states):
    visited_states.append(origin_state)
    for state in transitions[origin_state].values():
        if state not in visited_states:
            visit_reachable_states(state, transitions, visited_states)
    return visited_states

def create_initial_state_string(initial_state):
    initial_state_strng = "{" + initial_state + "}"
    
    return initial_state_strng

def create_final_states_string(final_states):
    final_states_string = "{"
    for state in final_states:
        if state == final_states[-1]:
            final_states_string += ("{"  + state + "}}")
        else:
            final_states_string += ("{"  + state + "},")
    
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
    for state in transitions.keys():
        for key, value in transitions[state].items():
            transitions_string += "{" + f"{state}" + "}," + f"{key}," + "{" + f"{value}" + "};"
    transitions_string = transitions_string[:-1]
    
    return transitions_string

def print_final_result(states_number, initial_state, final_states, alphabet, transitions):
    states_number_string = str(states_number)
    initial_state_string = create_initial_state_string(initial_state)
    final_states_string = create_final_states_string(final_states)
    alphabet_string = create_alphabet_string(alphabet)
    transitions_string = create_transitions_string(transitions)
    
    return(states_number_string + ";" + initial_state_string + ";" + final_states_string + ";" + alphabet_string + ";" + transitions_string)
