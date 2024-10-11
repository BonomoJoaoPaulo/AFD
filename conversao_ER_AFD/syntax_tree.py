from collections import deque # Biblioteca para usar a estrutura de dados deque.
from typing import List

from automata import State
from automata import Transition


class Node:
    """
    Classe para representar um nó da Árvore de Sintaxe Estendida.
    """
    def __init__(self, symbol: str):
        """
        Método construtor da classe.
        Os atributos da classe são:
            - symbol: símbolo do nó;
            - nullable: é verdadeira para um nó 'n' da árvore sintática sse a subexpressão representada por 'n'
        tiver ε em sua linguagem (pode-se tornar a subexpressão nula);
            - first_pos: é o conjunto de posições na subárvore com raiz em 'n' que corresponde ao primeiro
        símbolo de pelo menos uma cadeia na linguagem da subexpressão cuja raiz é 'n'.
            - last_pos: é o conjunto de posições na subárvore com raiz em 'n' que corresponde ao último símbolo
        de pelo menos uma cadeia na linguagem da subexpressão cuja raiz é 'n'.
            - id: identificador do nó.
            - children: lista de filhos do nó, neste caso o atributo precisa ser privado.
        """
        self.symbol = symbol
        self.nullable = symbol in ('*', '&')
        self.first_pos = None
        self.last_pos = None
        self.id = None
        self.__children = []

    @property
    def children(self) -> 'list[Self]':
        """
        Retona a lista de filhos do nó.
        """
        return self.__children
    
    @property
    def first_child(self) -> 'Self | None':
        """
        Retorna o primeiro filho do nó (c1).
        """
        return self.__get_child(0)

    @property
    def last_child(self) -> 'Self | None':
        """
        Retorna o segundo filho do nó (c2).
        """
        return self.__get_child(1)

    def __get_child(self, index: int) -> 'Self | None':
        """
        Método reutilizável para obter um filho da lista especificado pelo seu index.
        """
        try:
            return self.__children[index]
        except:
            return None

    def append_child(self, child: 'Self') -> None:
        """
        Método para adicionar um filho ao nó.
        """
        self.__children.append(child)


class SyntaxTreeBuilder():
    """
    Classe responsável por construir a Árvore de Sintaxe Estendida.
    
    A classe possui um método estático que recebe uma expressão regular e retorna
    a Árvore de Sintaxe Estendida correspondente. Há também uma variável de classe,
    que é um dicionário que mapeia os operadores da expressão regular para os símbolos
    correspondentes na Árvore de Sintaxe Estendida.
    """

    operators = {
        'concat': '.',
        'or': '|',
        'star': '*',
        'open_par': '(',
        'close_par': ')'
    }

    @classmethod
    def build_tree(cls, regex: str) -> 'SyntaxTree':
        """
        Método estático que constrói a Árvore de Sintaxe Estendida a partir de uma expressão regular.
        """
        return SyntaxTree(regex, cls.operators)


class SyntaxTree:
    """
    Classe para representar a Árvore de Sintaxe Estendida.
    """
    def __init__(self, regex: str, operators):
        """
        Método construtor da classe.
        Os atributos da classe são:
            - alphabet: conjunto de símbolos da expressão regular;
            - root: raiz da Árvore de Sintaxe Estendida;
            - aux_stack: pilha auxiliar;
            - completed_regex: expressão regular completada com os símbolos '#' e '.';
            - __id_counter: contador de identificadores dos nós da árvore;
            - __leaf_nodes: dicionário que mapeia os identificadores dos nós folha para os nós folha;
            - __followpos: dicionário que mapeia os followpos para os conjuntos de posições.
        """
        self.__define_alphabet(regex, operators)
        self.__complete_regex(regex)
        self.root = Node(None)
        self.aux_stack = deque()
        self.__create_tree(self.completed_regex, self.root)

        self.__id_counter: int = 1
        self.__leaf_nodes = {}
        self.__followpos = {}

        self.__process_in_post_order(self.root)
        self.__create_followpos(self.root)
    
    def __define_alphabet(self, regex: str, operators) -> None:
        """
        Define o alfabeto (os símbolos) da expressão regular.
        """
        alphabet = {i for i in f'({regex})#' if i not in operators.values()}
        self.alphabet = alphabet
    
    def __complete_regex(self, regex: str) -> None:
        """
        Adiciona o terminal '#' ao final da ER e 
        o símbolo de concatenação ('.') nos devidos locais da ER.
        """
        masked_regex = f'({regex})#'
        new_regex = ''
        
        for index, item in enumerate(masked_regex[:-1]):
            next_item = masked_regex[index + 1]
            if item in self.alphabet:
                new_regex += item if next_item in [')', '*', '|'] else f'{item}.'
            elif item == ')':
                new_regex += item if next_item in ['*', ')'] else f'{item}.'
            elif item == '*':
                new_regex += item if next_item in ['.', '|', ')'] else f'{item}.'
            else:
                new_regex += item

        self.completed_regex = f'{new_regex}#'

    def __create_tree(self, regex: str, root: Node) -> None:
        """
        Cria os nós da Árvore de Sintaxe Estendida a partir da expressão regular e do nó raiz.
        
        No caso base, a expressão regular é um símbolo.
        Caso contrário, a função é chamada recursivamente da seguinte forma:
            1 - Encontramos a posição do operador que pode dividir a expressão regular;
            2 - Esse operador será a raiz da nova subárvore;
            3 - Dividimos a expressão regular em duas partes;
            4 - Criamos novos nós e chamamos recursivamente para cada um.
        """
        if len(regex) == 1:
            root.symbol = regex
        else:
            operator, position = self.__search_operator_position(regex)
            root.symbol = operator
            left, right = self.__divide_regex(regex, position)
            root.append_child(Node(None))
            self.__create_tree(left, root.first_child)
            if right:
                root.append_child(Node(None))
                self.__create_tree(right, root.last_child)

    def __search_operator_position(self, regex):
        """
        Considerando a expressão regular, encontra a posição da última
        ocorrência de um dos operadores, em ordem inversa de precedência.
        
        Neste método, nós buscamos na ordem inversa da precedência natural.
        """
        for oper in ['|', '.', '*']:
            self.aux_stack.clear()
            for index, item in enumerate(regex[::-1]):
                if item == ')':
                    self.aux_stack.append(item)

                elif item == '(':
                    self.aux_stack.pop()

                elif not bool(self.aux_stack):
                    if item == oper:
                        return oper, len(regex) - index - 1

    def __divide_regex(self, regex: str, position: int): #-> tuple[str, str]:
        """
        Divide a expressão regular em duas partes com base na posição
        do operador com menor precedência.
        
        Se a posição for zero, estamos em um caso de operação de concatenação.
        """
        left = regex[:position]
        right = regex[position + 1 :] if position > 0 else None

        new_list = []
        for i in [left, right]:
            if i:
                has_extra, carac = self.__has_extra_parenthesis(i)
                if not has_extra:
                    if i[0] == '(' and i[-1] != '*': i = i[1:]
                    if i[-1] == ')': i = i[:-1]
                else:
                    if carac == '(':
                        i.replace(carac, '', 1)
                    elif carac == ')':
                        rev_s = i[::-1]
                        i = len(i) - rev_s.index(carac) - 1
                        i = i[:i] + i[i+1:]
            new_list.append(i)

        return new_list

    def __has_extra_parenthesis(self, regex: str): #-> tuple[bool, str]:
        """
        Analisa se a expressão regular contém parênteses extras.
        """        
        stack = deque()
        for item in regex:
            if item == '(': stack.append(item)
            elif item == ')':
                if not bool(stack):
                    return True, ')'
                else:
                    stack.pop()

        is_empty = not bool(stack)

        return not is_empty, '(' if not is_empty else None
    

    def __process_in_post_order(self, node: Node) -> None:
        """
        Método recursivo para processar firstpos e lastpos dos nós da árvore:
            - Percorre a árvore em pós-ordem.
        """
        if node.first_child is not None:
            self.__process_in_post_order(node.first_child)

        if node.last_child is not None:
            self.__process_in_post_order(node.last_child)

        self.__set_firstpos_and_lastpos(node)

    def __set_firstpos_and_lastpos(self, node: Node) -> None:
        """
        'Seta' os valores de firstpos, lastpos e nullable dos nós da árvore.
        """
        if node.symbol == '&':
            node.nullable = True

        elif node.symbol == '|':

            node.first_pos = [
                pos
                for child in [node.first_child, node.last_child]
                for pos in (child.first_pos or [])
                if pos != []
            ]
            node.last_pos = [
                pos
                for child in [node.first_child, node.last_child]
                for pos in (child.last_pos or [])
                if pos != []
            ]

            if node.first_child.nullable or node.last_child.nullable:
                node.nullable = True

        elif node.symbol == '*':
            node.first_pos = [pos for pos in node.first_child.first_pos if pos != []]
            node.last_pos = [pos for pos in node.first_child.last_pos if pos != []]
            node.nullable = True

        elif node.symbol == '.':
            if node.first_child.nullable and node.last_child.nullable:
                node.nullable = True

            if node.first_child.nullable:
                node.first_pos = [
                    pos
                    for child in [node.first_child, node.last_child]
                    for pos in child.first_pos
                ]
            else:
                node.first_pos = [pos for pos in node.first_child.first_pos]

            if node.last_child.nullable:
                node.last_pos = [
                    pos
                    for child in [node.first_child, node.last_child]
                    for pos in child.last_pos
                ]
            else:
                node.last_pos = [pos for pos in node.last_child.last_pos]
        
        else:
            node.id = self.__id_counter
            self.__leaf_nodes[self.__id_counter] = node
            self.__followpos[self.__id_counter] = set()

            self.__id_counter += 1

            node.first_pos = [node.id]
            node.last_pos = [node.id]

    def __create_followpos(self, node: Node) -> None:
        """
        Cria o followpos para cada nó com um símbolo do alfabeto da expressão na árvore:
            - Também 'seta' o followpos para os nós que representam a operação de concatenação e estrela;
            - Pós-ordem.
        """
        # traverse in post-order
        if node.first_child is not None:
            self.__create_followpos(node.first_child)

        if node.last_child is not None:
            self.__create_followpos(node.last_child)

        if node.symbol in ['.', '*']: self.__set_followpos(node)

    def __set_followpos(self, node: Node) -> None:
        """
        'Seta' o followpos para os nós que representam a operação de concatenação e estrela.
        """
        if node.symbol == '*':
            for n in node.last_pos:
                for id in node.first_pos:
                    self.__followpos[n].add(id)
        if node.symbol == '.':
            for n in node.first_child.last_pos:
                for id in node.last_child.first_pos:
                    self.__followpos[n].add(id)

    def to_afd(self):
        """
        Método que converte a Árvore de Sintaxe Estendida em um Autômato Finito Determinístico.
            - states: lista de estados do AFD;
            - visited_sates: lista de estados visitados;
            - final_states: lista de estados finais;
            - transitions: lista de transições do AFD;
            - initial_state: estado inicial do AFD.
        """
        states = [self.__get_initial_state()]
        visited_states = []
        final_states = []
        transitions = []
        initial_state = self.root.first_pos
        
        final_id = list(self.__leaf_nodes.keys())[-1]

        # Percorre a lista de estados até que todos os estados sejam visitados.
        while states:
            state = states.pop(0)
            visited_states.append(state)

            # Verifica se o estado é um estado final.
            if final_id in state.source:
                final_states.append(state)
            
            # Cria as transições do estado.
            new_transitions = self.__create_transitions(state)
            transitions.extend(new_transitions)

            # Adiciona os estados alvos das transições à lista de estados.
            for transition in new_transitions:
                if transition.target != []:
                    new_state = transition.target
                    state = State(new_state)
                    if not state in visited_states and not state in states:
                        states.append(state)

        # Retorna a representação do AFD.
        return self.__format_str(initial_state, visited_states, final_states, transitions)
    
    def __get_initial_state(self) -> State:
        """
        Retorna o estado inicial do autômato finito.
        """
        return State(self.root.first_pos)
    
    def __create_transitions(self, state: List[int]):
        """
        Método privado que cria as transições de um estado.
        
        O método recebe um estado,
        """
        transitions = {}
        for id in state.source:
            symbol = self.__leaf_nodes[id].symbol
            followpos = self.__followpos[id]
            if symbol in transitions:
                for i in followpos:
                    transitions[symbol].add(i)
            else:
                transitions[symbol] = set(followpos)
        
        transitions_list = []
        for symbol, target in transitions.items():
            t = Transition(state, symbol, sorted(list(target)))
            transitions_list.append(t)

        ordered_transitions = sorted(transitions_list, key=lambda x: (x.symbol))
        
        return ordered_transitions

    def __format_str(self,
                     intitial: List[int],
                     all: List[State],
                     finals: List[State],
                     transitions: List[Transition]) -> str:
        """
        Gera o autômato finito determinístico em formato de string para printar no formato
        especificado pelo VPL.
        """
        af_str = ''

        # QUANTIDADE DE ESTADOS
        af_str += f'{len(all)};'
        
        # ESTADO INICIAL
        initial_str = ",".join([str(i) for i in intitial])
        
        af_str += f'{{{initial_str}}};'

        # ESTADOS FINAIS        
        curr_str = []
        for final in finals:
            curr_str.append(f'{{{",".join([str(i) for i in final.source])}}}')
        af_str += f'{{{",".join(curr_str)}}};'
        
        # ALFABETO
        self.alphabet.remove('#')
        if '&' in self.alphabet:
            self.alphabet.remove('&')
        af_str += f'{{{",".join(sorted([letter for letter in self.alphabet]))}}};'
        
        # TRANSIÇÕES
        for transition in transitions:
            if transition.symbol != '#':
                source = f'{{{",".join([str(i) for i in transition.source.source])}}}'
                symbol = f'{transition.symbol}'
                target = f'{{{",".join([str(i) for i in transition.target])}}}'
                af_str += f'{source},{symbol},{target};'

        # PRINTA O AUTÔMATO FINITO DETERMINÍSTICO GERADO
        print(af_str[:-1])
