import time
from grammar.engine import GrammarEngine
from rule_system.engine import RuleEngine
from book.pdf_gen import PDF


def cleanup_domain(filename):
    """
    rewrites file in cleaner way
    splits on newlines
    adds brackets to bracket phrases
    """
    with open(filename, 'r') as file:
        original = file.read().split('\n')

    need_brackets = ['BEGIN ENTITIES', 'END ENTITIES', 'BEGIN FACTS', 'END FACTS']
    # replace domain file text with brackets
    with open(filename, 'w') as file:
        in_facts = False
        for line in original:
            if line:
                if line in need_brackets:
                    if line == 'BEGIN FACTS':
                        in_facts = True
                    line = "<" + line + ">"
                if in_facts and line[0].istitle():
                    split = line.split(None, 1)
                    line = "<" + split[0] + "> " + ' '.join([i for i in split[1:]])
            file.write(line + "\n")

def component4():
    # make domain file
    domain_engine = GrammarEngine(
        file_path='grammar/grammars/it_domain.txt')
    domain_engine.generate( 
        start_symbol_name='ORIGIN',
        outfile_path='rule_system/content/new_it_domain.txt')   
    cleanup_domain('rule_system/content/new_it_domain.txt')

    # fire rules
    rule_engine = RuleEngine(
        path_to_domain_file='rule_system/content/new_it_domain.txt',
        path_to_rules_file='rule_system/content/it_rules.txt',
        shuffle_randomly=True,
    )
    rule_engine.execute(n=100)

    book = PDF(
        # filename=f"generated_books/IT_book_{int(time.time())}.pdf",
        filename="generated_books/IT_DRAFT.pdf",
        width=8.5,
        height=11,
        x_margin=1.0,
        y_margin=1.0,
        initial_base_style="BodyText",
        initial_font_name="Times-Roman",
        initial_font_size=12,
        initial_font_color="black"
    )
    book.style(leading=30, space_between_paragraphs=10, background_padding=20)

    # make engine to do the writing
    grammar_engine = GrammarEngine(
        file_path='grammar/grammars/it_grammar.txt',
        initial_state=None)

    book.insert_title_page(title=f"IT", author="Jack Rybarczyk", alignment="center", image_filename="book/images/it.png", image_width =5)
    plot = rule_engine.actions
    print(plot)

    skip_actions = ["GoToRoom", "Free", "UnFree"]

    for i, action in enumerate(plot):
        for role_name, entity in action.bindings.items():
            entity.add_to_grammar_engine_state(
                grammar_engine=grammar_engine,
                variable_name=role_name
            )
        
        text = grammar_engine.generate(start_symbol_name=action.name, debug=False)
        print(text)
        # Write the new text to the book! Let's change the style slightly for each action
        # in the plot, to show off how that works.
        
        book.style(
            font_color="black",
            alignment="left",
            background_color= "white"
        )
        book.write(text=text)
        if action.name not in skip_actions:
            book.insert_space(height=1)
            # book.insert_page_break()

    book.insert_page_break()
    book.style(
        alignment="center",
        font_color="black",
        background_color="white",
        space_between_paragraphs=5,
        leading=5
    )
    book.write("Appendix: Facts")
    book.insert_space(height=1.0)
    book.style(font_name="Times-Roman", font_size=10, alignment="left")
    for fact in sorted(rule_engine.working_memory.facts):
        book.write(f"  {fact}")
    # I'm going to throw in an image at the end, just to show you how
    book.insert_page_break()
    book.build(page_numbers=True)

component4()

def grade(): 
    """The function James will be using to grade your component."""
    print("\n\n-- Component 4 -- ")
    component4()


