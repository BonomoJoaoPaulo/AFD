

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
        return self.__children
    
    @property
    def first_child(self) -> 'Self | None':
        return self.__get_child(0)

    @property
    def last_child(self) -> 'Self | None':
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
