from dataclasses import dataclass
from typing import List


@dataclass
class State:
    """
    Classe para representar um estado do autômato finito.
    
    A razão para usarmos a dataclass é que ela fornece funcionalidades úteis automaticamente,
    como __init__(), __repr__() e __eq__(), que são comuns em classes que são basicamente containers de dados.
    Além disso, com a anotação de tipo, a dataclass pode ser mais clara e legível, 
    tornando o código mais fácil de entender.
    """

    source: List[int]

    def __eq__(self, other):
        """
        O método é utilizado para comparar dois objetos do tipo State.
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
        return hash(self.source)


@dataclass
class Transition:
    """
    Clase para representar uma transição do autômato finito.
    
    A razão para usarmos a dataclass é que ela fornece funcionalidades úteis automaticamente,
    como __init__(), __repr__() e __eq__(), que são comuns em classes que são basicamente containers de dados.
    Além disso, com a anotação de tipo, a dataclass pode ser mais clara e legível, 
    tornando o código mais fácil de entender.
    """
    source: List[str]
    symbol: str
    target: List[str]

    def __eq__(self, other):
        """
        O método é utilizado para comparar dois objetos do tipo Transition.
        O método recebe 'other', verifica se é um objeto do tipo Transition e, caso seja, compara as duas transições.
        O método retorna verdadeiro sse as transições partirem da mesma origem e chegarem ao mesmo destino pelo mesmo
        símbolo.
        """
        if isinstance(other, Transition):
            return (
                self.source == other.source and
                self.symbol == other.symbol and
                self.target == other.target
            )
        return False
    
    def __hash__(self):
        """
        O método retorna o valor de hash para a transição.
        O valor de hash é calculado com base no estado de origem, no símbolo e no estado destino.
        """
        return hash((self.source, self.symbol, *self.target))
