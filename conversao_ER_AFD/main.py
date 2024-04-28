"""
1) Constrói-se a árvore de sintaxe estendida para a expressão regula em questão 
(usa-se o símbolo '#' ao término da expressão (r)#)
"""

def handle_input(er: str) -> str:
    """
    Esta função é responsável por tratar a entrada da expressão regular, ao adicionar o símbolo '.'
    onde há concatenação e o símbolo '#' ao final da expressão para facilitar a criação da árvore
    de sintaxe estendida.
    """
    new_er = ""
    concat_counter = 0

    for char_id in range(len(er)):
        if char_id == len(er) - 1:
            break
        if (er[char_id] == 'a' or 
            er[char_id] == 'b' or 
            er[char_id] == ')' or 
            er[char_id] == '*') and (er[char_id + 1] == 'a' or 
            er[char_id + 1] == 'b' or 
            er[char_id + 1] == '('
        ):
            concat_counter += 1
            if not new_er:
                new_er = er[:char_id+concat_counter] + '.' + er[char_id + concat_counter:]
            else:
                new_er = new_er[:char_id+concat_counter] + '.' + new_er[char_id + concat_counter:]
        else:
            if not new_er:
                new_er = er
    
    new_er = new_er + "#"

    return new_er

def create_syntax_tree(er: str) -> str:
    """
    Esta função é responsável por criar a árvore de sintaxe estendida para a expressão regular de entrada.
    """
    syntax_tree: list = []
    concat_symbols: list = []
    union_symbols: list = []
    star_symbols: list = []
    
    for id in range(len(er)):
        if er[id] == '.':
            concat_symbols.append(id)
        elif er[id] == '|':
            union_symbols.append(id)
        elif er[id] == '*':
            star_symbols.append(id)
            
    print(concat_symbols)
    
    for cid in concat_symbols:
        if concat_symbols.index(cid) == 0:
            syntax_tree = create_concat_node(syntax_tree, er, cid)
        else:
            if concat_symbols.index(cid) == len(concat_symbols) - 1:
                syntax_tree = create_concat_node(syntax_tree, er, cid, concat_symbols[concat_symbols.index(cid)-1], True)
            else:
                syntax_tree = create_concat_node(syntax_tree, er, cid, concat_symbols[concat_symbols.index(cid)-1])
    
    return syntax_tree
    

def create_concat_node(syntax_tree: list, er: str, cid: int, pcid: int = None, last_cid = False) -> str:
    """
    Esta função é responsável por criar um nó de concatenação na árvore de sintaxe estendida.
    """
    if not pcid:
        sub_er = er[:cid]
    else:
        if last_cid:
            sub_er = er[cid+1:]
        else:
            sub_er = er[pcid+1:cid]
    
    if '|' in sub_er:
        new_node = create_union_node(sub_er, sub_er.index('|'))
        syntax_tree.append(new_node)
    
    return syntax_tree

def create_union_node(er: str, uid: int) -> str:
    """
    Esta função é responsável por criar um nó de união na árvore de sintaxe estendida.
    """
    node_left = er[er.index('(')+1:uid]
    node_right = er[uid+1:er.index(')')]
    node = {
        'type': '|',
        'left': node_left,
        'right': node_right
    }

    return node



if __name__ == "__main__":
    er_inputed : str = input()
    er_processed = handle_input(er_inputed)
    print(er_processed)
    syntax_tree = create_syntax_tree(er_processed)
    print(syntax_tree)
