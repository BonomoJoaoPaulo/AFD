from dataclasses import dataclass

@dataclass
class State:
    """
    Classe para representar um estado do autômato finito.
    
        A razão para usarmos a dataclass é que ela fornece funcionalidades úteis automaticamente,
    como __init__(), __repr__() e __eq__(), que são comuns em classes que são basicamente containers de dados.
        Além disso, com a anotação de tipo, a dataclass pode ser mais clara e legível, 
    tornando o código mais fácil de entender.
    """

    source: list[int]

    def __eq__(self, other):
        """
        O método é utilizado para comparar dois estados (objetos do tipo State).
        O método recebe 'other', verifica se é um objeto do tipo State e, caso seja, compara os estados.
        O método retorna verdadeiro sse os estados possuírem o mesmo conjunto de estados de origem.
        """
        if isinstance(other, State):
            return (
                set(self.source) == set(other.source)
            )
        return False
    
    def __hash__(self):
        """
        O método retorna o valor de hash para o objeto State.
        O valor de hash é calculado com base nos estados de origem.
        """
        return hash((self.source, self.symbol, *self.target))
