from syntax_tree import SyntaxTreeBuilder

# regex = '(&|b)(ab)*(&|a)'
# regex = 'aa*(bb*aa*b)*'
# regex = 'a(a|b)*a'
regex = 'a(a*(bb*a)*)*|b(b*(aa*b)*)*'

tree = SyntaxTreeBuilder.build_tree(regex)
tree.print_tree()
tree.to_afd()
