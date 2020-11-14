from grammar.engine import GrammarEngine
from rule_system.engine import RuleEngine

# make domain file
grammar_engine = GrammarEngine(
    file_path='grammar/grammars/comp1.txt')
grammar_engine.generate( 
    start_symbol_name='ORIGIN',
    outfile_path='rule_system/content/newmonkey_domain.txt')   

# make copy of domain file text
with open('rule_system/content/newmonkey_domain.txt', 'r') as file:
    original = file.read().split('\n')

need_brackets = ['BEGIN ENTITIES', 'END ENTITIES', 'BEGIN FACTS', 'END FACTS']
# replace domain file text with brackets (generator doesn't allow this)
with open('rule_system/content/newmonkey_domain.txt', 'w') as file:
    for line in original:
        if line in need_brackets:
            line = "<" + line + ">"
        file.write(line + "\n")


engine = RuleEngine(
    path_to_domain_file='rule_system/content/newmonkey_domain.txt',
    path_to_rules_file='rule_system/content/monkey_rules.txt',
    shuffle_randomly=True,
)

engine.execute(n=30)
