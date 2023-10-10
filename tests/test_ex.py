import nbmake

from nbwrite import ex


def test_when_index_then_build_index():
    assert ex.question == "Which NFL team won the Super Bowl in the 2010 season?"


def test_when_gen_nbrun_doc_then_nb_output():
    assert ex.question == "Which NFL team won the Super Bowl in the 2010 season?"
