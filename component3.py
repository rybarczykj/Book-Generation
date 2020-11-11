
import time
import random
from grammar.engine import GrammarEngine
from rule_system.engine import RuleEngine
from book.pdf_gen import PDF

def component3(random_seed=None):
    book = PDF(
        # filename=f"generated_books/murder_book_{int(time.time())}.pdf",
        filename=f"generated_books/murder_book_DRAFT.pdf",
        width=5.5,
        height=5.5,
        x_margin=1.0,
        y_margin=1.0,
        initial_base_style="BodyText",
        initial_font_name="Times-Roman",
        initial_font_size=12,
        initial_font_color="black"
    )
    book.style(leading=30, space_between_paragraphs=10, background_padding=20)


    rule_engine = RuleEngine(
        path_to_domain_file='rule_system/content/murder_domain.txt',
        path_to_rules_file='rule_system/content/murder_rules.txt',
        shuffle_randomly=True,
        random_seed=random_seed
    )

    rule_engine.execute(n=100)
    

    book.insert_title_page(title=f"A Mysterous Night of Murder", author="Piper Welch and Jack Rybarczyk", alignment="center")

    plot = rule_engine.actions
    # Prepare a grammar engine
    grammar_engine = GrammarEngine(
        file_path='grammar/grammars/murder_grammar.txt',
        initial_state=None,
        random_seed=random_seed
    )
    skip_actions = ["GoToRoom"]
  
    # For each action in the "plot", we'll generate text recounting that action by
    # rewriting a corresponding nonterminal symbol that I authored in the demo
    # grammar (see grammar/grammars/demo_grammar.txt).
    for i, action in enumerate(plot):
        if action.name not in skip_actions:
          # Before rewriting the corresponding nonterminal symbol, we need to update
          # the grammar-engine state. A quick glance at the grammar file will reveal
          # that each of these special action nonterminal symbols relies on the entities
          # associated with that action being included in the state, with variable names
          # matching up with the action's role names. The grammar also expects the entities'
          # attributes to be included in the state. Again, I'll use
          # Entity.add_to_grammar_engine_state().
          for role_name, entity in action.bindings.items():
              entity.add_to_grammar_engine_state(
                  grammar_engine=grammar_engine,
                  variable_name=role_name
              )
        
          # Now, rewrite the nonterminal symbol associated with this action. Of course,
          # there's only such a symbol because I authored symbols for all the actions I
          # knew I would want to potentially include in my stories. To make this process
          # easier, I named all of the nonterminal symbols such that they have the same
          # exact names as the actions they recount.
          text = grammar_engine.generate(start_symbol_name=action.name, debug=False)
          print(text)
          # Write the new text to the book! Let's change the style slightly for each action
          # in the plot, to show off how that works.
          book.style(
              font_color="black",
              alignment="left",
              background_color= "white"
          )
          book.insert_page_break()
          book.insert_space(height=1.0)
          book.write(text=text)

    book.insert_page_break()
    book.style(
        alignment="center",
        font_color="black",
        background_color="white",
        space_between_paragraphs=10,
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


        

component3()   


def grade():
    """The function James will be using to grade your component."""
    print("\n\n-- Component 3 -- ")
    component3()
