from src.functions import (handle_input, 
                           verify_transitions, 
                           determine_automato, 
                           remove_unreachable_states, mark_final_states, print_final_result)

def main():
    states_number, initial_state, final_states, alphabet, transitions = handle_input()    
    transitions_dict = verify_transitions(transitions)
    i = 0
    while i < 10:
        transitions = determine_automato(states_number, initial_state, final_states, alphabet, transitions_dict)
        i += 1
    
    final_states = mark_final_states(final_states, transitions)
    
    transitions = remove_unreachable_states(states_number, initial_state, final_states, alphabet, transitions)
    print(transitions)
    print(final_states)

    states_number = len(transitions)
    print(states_number)

    print_final_result(states_number, initial_state, final_states, alphabet, transitions)

if __name__ == '__main__':
    main()
