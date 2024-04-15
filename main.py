from src.functions import (handle_input, 
                           verify_transitions,
                           verify_transitions_with_epsilon,
                           create_state_by_visiting_states_by_epsilon,
                           determine_automato,
                           remove_unreachable_states, 
                           mark_final_states, 
                           print_final_result)

def main():
    states_number, initial_state, final_states, alphabet, transitions = handle_input() 
    transitions_dict = verify_transitions(transitions)
    
    if "&" in alphabet:
        initial_state = create_state_by_visiting_states_by_epsilon(transitions_dict, initial_state)
        transitions = verify_transitions_with_epsilon(transitions_dict, alphabet)
        final_states = mark_final_states(final_states, transitions)
        alphabet = [letter for letter in alphabet if letter != "&"]
    else:
        i = 0
        while i < 20:
            transitions = determine_automato(states_number, initial_state, final_states, alphabet, transitions_dict)
            i += 1
            
        final_states = mark_final_states(final_states, transitions)
        
        transitions = remove_unreachable_states(states_number, initial_state, final_states, alphabet, transitions)

    states_number = len(transitions)

    final_automato = print_final_result(states_number, initial_state, final_states, alphabet, transitions)

    print(final_automato)

if __name__ == '__main__':
    main()
