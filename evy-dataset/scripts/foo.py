import re

class SimpleTokenizer:
    def __init__(self, delimiters=(".", ",", " ")):
        self.delimiters = delimiters
        self.unk_token = "<unk>"
        self.vocab = {self.unk_token: 0}

    def tokenize(self, text):
      escaped_delimiters = [re.escape(delimiter) for delimiter in self.delimiters]
      # Create regex pattern to match any delimiter
      pattern = '|'.join(escaped_delimiters)
      # Split the text using regex pattern
      parts = re.split('(' + pattern + ')', text)
      # Remove empty strings from the result
      parts = [part for part in parts if part != '']
      self._build_vocab(parts)
      return parts

    def encode(self, text):
        tokens = self.tokenize(text)
        return [self.vocab.get(token, self.vocab[self.unk_token]) for token in tokens]

    def _build_vocab(self, tokens):
        for token in tokens:
            if token not in self.vocab:
                self.vocab[token] = len(self.vocab)

    def decode(self, encoded_text):
      reverse_vocab = {v: k for k, v in self.vocab.items()}

      decoded_text = ""
      for idx in encoded_text:
        token = reverse_vocab.get(idx, self.unk_token)
        if token in self.delimiters:  # If the token is a delimiter
          decoded_text += token  # Add directly without a space
        else:
          decoded_text += " " + token  # Add with a space before
      return decoded_text.strip()  # Remove any leading/trailing space


if __name__ == "__main__":
  tokenizer = SimpleTokenizer()
  text = "This is some text, with punctuation. Here are more words."
  strtokens = tokenizer.tokenize(text)
  tokens = tokenizer.encode(text)
  print(text)
  print(list(zip(tokens, strtokens)))
  decoded = tokenizer.decode(tokens)



