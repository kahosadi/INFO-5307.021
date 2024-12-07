import re
import spacy

class enapatitlecasechecker:
    def __init__(self):
        # Load English language model for part-of-speech tagging
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("SpaCy English model not found. Please install using: python -m spacy download en_core_web_sm")
            raise

    def _is_minor_word(self, word):
        """
        Determine if a word should be capitalized based on POS or length

        Args:
        word (str): The word to check
        pos (str): Part of speech of the word

        Returns:
        bool: True if the word should be capitalized
        """
        # Major word part of speech categories
        # major_pos = {'NOUN', 'VERB', 'ADJ', 'ADV', 'PRON'}

        # Minor words to always lowercase (except first word)
        minor_words = {
            'a', 'an', 'the',  # Articles
            'and', 'but', 'or', 'nor', 'for', 'so', 'yet',  # Conjunctions
            'at', 'by', 'for', 'in', 'of', 'on', 'to', 'up', 'via'  # Prepositions
        }

        # Capitalize if:
        # 1. Word is in major POS categories
        # 2. Word is 4 letters or longer
        # 3. Word is not in minor words list

        return (
            #pos in major_pos or
            word.lower() not in minor_words
            #len(word) >= 4 and word.lower() not in minor_words
        )

    def detect_extra_spaces(self, title):
      """
      Detect and report extra spaces in a title.

      Args:
          title (str): The input title to check for extra spaces

      Returns:
          dict: A dictionary with detailed space information
      """
      # Check for leading/trailing spaces
      has_leading_space = title.startswith(' ')
      has_trailing_space = title.endswith(' ')

      # Check for multiple consecutive spaces
      multiple_spaces = '  ' in title

      # Detailed space analysis
      space_details = {
          'original_title': title,
          'has_leading_space': has_leading_space,
          'has_trailing_space': has_trailing_space,
          'has_multiple_consecutive_spaces': multiple_spaces,
          'space_count': title.count(' '),
          'extra_space_locations': []
      }

      # Find locations of extra spaces
      words = title.split()
      original_words = title.split(' ')

      if len(words) != len(original_words):
          # Identify where extra spaces occur
          for i in range(len(original_words)):
              if original_words[i] == '':
                  space_details['extra_space_locations'].append(i)

      return space_details

    def check_apa_title_case(self, title):
        """
        Check if a title follows APA 7th edition capitalization rules

        Args:
        title (str): The title to check

        Returns:
        dict: Validation results with detailed feedback
        """

        # Validation results
        validation = {
            'is_valid': True,
            'errors': [],
            'corrections': []
        }

        # Check if the title is in upper case
        if title.isupper():
            validation['is_valid'] = False
            validation['errors'].append("Title should not be in uppercase")

        # Check for extra spacing and spaces in the middle of the title
        space_check = self.detect_extra_spaces(title)

        if space_check['has_leading_space'] or space_check['has_trailing_space'] or space_check['has_multiple_consecutive_spaces']:
            validation['is_valid'] = False
            validation['errors'].append("Extra space in leading, trailing, or in the middle")

        # Check for extra spacing and spaces before punctuation
        if re.search(r'\s+[,:;—!?]', title):
            validation['is_valid'] = False
            validation['errors'].append("Extra space before punctuation")

        # Check for missing space after punctuation (except em dash or comma)
        if re.search(r'[:;!?](\S)', title):
            validation['is_valid'] = False
            validation['errors'].append("Missing space after punctuation")

        #Remove the extra spacing
        title = ' '.join(title.split());

        # Tokenize and analyze the title
        doc = self.nlp(title)

        # Track whether we're checking a new section after specific punctuation
        new_section = True

        for i, token in enumerate(doc):
            # Skip punctuation
            if token.pos_ == 'PUNCT':
                # Reset new section flag after specific punctuation
                if token.text in [':', ';', '—', '!', '?']:
                    new_section = True
                continue

            # Check capitalization
            word = token.text
            pos = token.pos_

            # First word or start of new section after punctuation should always be capitalized
            should_be_capitalized = (
                i == 0 or
                new_section or
                self._is_minor_word(word)
            )

            # Check for hyphenated words
            if '-' in word:
                parts = word.split('-')
                # Capitalize each part of hyphenated words
                if not all(part[0].isupper() for part in parts):
                    validation['is_valid'] = False
                    validation['errors'].append(f"Hyphenated word '{word}' not properly capitalized")

            # Validate capitalization
            if should_be_capitalized and not word[0].isupper() and word[0] not in ['\'','’'] and word[0].isdigit()==False:
                validation['is_valid'] = False
                validation['errors'].append(f"Word '{word}' should be capitalized")

            # Validate no capitalization for minor words (except first/new section)
            if not should_be_capitalized and word[0].isupper():
                validation['is_valid'] = False
                validation['errors'].append(f"Word '{word}' should not be capitalized")

            # Reset new section flag
            new_section = False

        return validation
'''
# Example usage and testing
def test_apa_title_case():
    # Create an instance of the checker
    checker = EnAPATitleCaseChecker()

    # Test cases
    test_titles = [
        " The Effects of Social Media on Mental Health",  # Correct
        "Self-Report Questionnaire: A Comprehensive Analysis ",  # Correct with subtitle
        "A Study of Urban Development: Challenges and Solutions",  # Correct with subtitle
        "Breaking Down Barriers — A New Approach",  # Correct with em dash
        "the Wrong Capitalization",  # Incorrect
        "Incorrect Capitalization of short Words",  # Incorrect
        "A study  Without Proper Rules",  # Incorrect,
        "A STUDY WITHOUT PROPER  RULES",  # Incorrect
        "Students' Anxiety: in Speaking English In An Indonesian High School"
    ]

    for title in test_titles:
        print(f"\nTitle: '{title}'")
        result = checker.check_apa_title_case(title)
        print("Is Valid:", result['is_valid'])
        if not result['is_valid']:
            print("Errors:")
            for error in result['errors']:
                print(f"- {error}")

# Run the tests
if __name__ == "__main__":
    test_apa_title_case()
'''