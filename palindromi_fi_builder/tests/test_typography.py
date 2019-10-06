import pytest

from palindromi_fi_builder import typography


@pytest.mark.parametrize(
    'text, expect',
    [('', ''),
     ('"', '"'),
     ("'", "'"),
     ('""', '&ldquo;&rdquo;'),
     ("''", '&lsquo;&rsquo;'),
     ("Antti's palindrome", "Antti's palindrome"),
     ("It's Antti's palindrome", "It's Antti's palindrome"),
     ('It "is" a "good" palindrome',
      'It &ldquo;is&rdquo; a &ldquo;good&rdquo; palindrome'),
     ('"Foo!", bar.', '&ldquo;Foo!&rdquo;, bar.')])
def test_typographic_quotes(text, expect):
    result = typography.typographic_quotes(text)

    assert result == expect


@pytest.mark.parametrize(
    'text, expect',
    [('', ''),
     ('"', '"'),
     ("'", "'"),
     ("Antti's palindrome", "Antti&rsquo;s palindrome"),
     ("It's Antti's palindrome", "It&rsquo;s Antti&rsquo;s palindrome"),
     ('It "is" a "good" palindrome',
      'It "is" a "good" palindrome'),
     ('"Foo!", bar.', '"Foo!", bar.')])
def test_inword_apostrophe(text, expect):
    result = typography.inword_apostrophe(text)

    assert result == expect


@pytest.mark.parametrize(
    'text, expect',
    [('', ''),
     ('"', '"'),
     ("'", "'"),
     ('""', '&ldquo;&rdquo;'),
     ("''", '&lsquo;&rsquo;'),
     ("Antti's palindrome", "Antti&rsquo;s palindrome"),
     ("It's Antti's palindrome", "It&rsquo;s Antti&rsquo;s palindrome"),
     ('It "is" a "good" palindrome',
      'It &ldquo;is&rdquo; a &ldquo;good&rdquo; palindrome'),
     ('"Foo!", bar.', '&ldquo;Foo!&rdquo;, bar.'),
     ('&ldquo;Isiä!&rdquo;, kääritty Tytti rääkäisi.',
      '&ldquo;Isiä!&rdquo;, kääritty Tytti rääkäisi.')])
def test_add_typography(text, expect):
    result = typography.add_typography(text)

    assert result == expect


