from src.parser.brochure_parser import parse_brochure


def test_parser():

    sample_text = "Entry Fee 1000 Organiser K Srunjay 8106909008"

    result = parse_brochure(sample_text)

    print(result)