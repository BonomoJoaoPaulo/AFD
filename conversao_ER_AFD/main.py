"""
Grupo: João Paulo Araujo Bonomo   (21100133)
       João Victor Volpato        (21105481)
       Rodrigo Santos de Carvalho (21100139)
       
Descrição: O programa recebe uma expressão regular e retorna o AFD equivalente à ER de entrada,
a partir da árvore de sintaxe gerada.

O projeto está estruturado em 3 arquivo: main.py, syntax_tree.py e automata.py.

- main.py:
    Arquivo principal executado pelo usuário/VPL. Recebe a ER como input e chama a função
    do construtor da árvore de sintaxe e a função de conversão da árvore para AFD.
- syntax_tree.py:
    Maior arquivo do projeto, contém as seguintes classes:
        - Node: classe que representa os nós da árvore de sintaxe;
        - SyntaxTreeBuilder: responsável por construir a árvore de sintaxe a partir
    da ER de entrada;
        - SyntaxTree: classe que representa a árvore de sintaxe.
- automata.py:
    Arquivo que contém as classes abaixo:
        - State: classe para representar os estados do AFD;
        - Transition: classe para representar as transições do AFD;
    
Todos os métodos e atributos das classes estão devidamente documentados e comentados em português
para melhor entendimento das funcionalidades, apesar do código estar em inglês por praticidade e 
costume dos alunos.

Algumas tipagens precisaram ser removidas do código para que o VPL aceitasse a submissão, por isso
alguns métodos e atributos não estão tipados e isso pode ser um problema para a legibilidade do código.   
Portanto nos disponilibizamos para quaisquer dúvidas ou esclarecimentos.
"""


if __name__ == '__main__':
    from syntax_tree import SyntaxTreeBuilder

    # regex = '(&|b)(ab)*(&|a)'             # Exemplo de Teste 1 do VPL.
    # regex = 'aa*(bb*aa*b)*'               # Exemplo de Teste 2 do VPL.
    # regex = 'a(a|b)*a'                    # Exemplo de Teste 3 do VPL.
    # regex = 'a(a*(bb*a)*)*|b(b*(aa*b)*)*' # Exemplo de Teste 4 do VPL.

    # Recebe a expressão regular como input e remove os espaços em branco (que existe no input do VPL).
    # OBS: alguns bons minutos foram gastos para descobrir que o input do VPL possui espaços em branco rsrsrs.
    regex = input().replace(" ", "")

    tree = SyntaxTreeBuilder.build_tree(regex) # Cria a árvore de sintaxe a partir da expressão regular.
    tree.to_afd() # Retorna o AFD equivalente à ER de entrada a partir da árvore de sintaxe gerada.
