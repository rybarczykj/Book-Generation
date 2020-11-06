from grammar.engine import GrammarEngine


def challenge1():
    # Here's some code to append the contents of one file
    # to another, which you can adapt to create a new
    # rules file with your original hand-authored rules along
    # with your procedurally generated ones.
    with open("rule_system/content/generated_monkey_rules.txt") as new_rules_file:
        # Read in the contents of your original rules file
        all_rules_str = open("rule_system/content/monkey_rules.txt").read()
        grammar_engine = GrammarEngine(
            file_path='grammar/grammars/monkey_rules_grammar.txt',
            initial_state=None,
            random_seed=None
        )
        for _ in range(3):
            new_rule_str = grammar_engine.generate(start_symbol_name="MonkeyRule")
            all_rules_str += new_rule_str
        new_rules_file.write(all_rules_str)


def grade():
    """The function James will be using to grade your component."""
    print("\n\n-- Supplementary Challenge 1 -- ")
    challenge1()
