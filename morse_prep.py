import re
from contractions import fix

# Common Morse abbreviations
MORSE_ABBREVIATIONS = {
  "before": "B4",
  "message": "MSG",
  "thanks": "TU",
  "you are": "UR",
  "please": "PSE",
  "understand": "UNDST",
  "because": "BC",
  "between": "BTN",
  "question": "QSTN"
}


# Function to preprocess text for Morse code
def preprocess_text(text):
  # Convert to uppercase
  text = text.upper()

  # Expand contractions (e.g., "we're" → "we are")
  text = fix(text)

  # Handle footnotes in square brackets (e.g., "City,[2]" → "City")
  text = re.sub(r"\[\d+\]", "", text)

  # Handle date ranges like (1895-1981) → "1895 TO 1981"
  text = re.sub(r"\((\d{4})-(\d{4})\)", r"\1 TO \2", text)

  # Remove unwanted punctuation but keep periods, commas, and question marks
  text = re.sub(r"[^A-Z0-9.,? '-]", "", text)

  # Replace common Morse abbreviations
  words = text.split()
  processed_words = [MORSE_ABBREVIATIONS.get(word, word) for word in words]

  # Convert numbers to digit form (assumed already in digit form)

  # Join words back into a single string
  processed_text = " ".join(processed_words)

  return processed_text


# Example usage
sample_text = "Feynman was born on May 11, 1918, in New York City,[2] to Lucille (née Phillips; 1895–1981), a homemaker, and Melville Arthur Feynman (1890–1946), a sales manager.[3] Feynman's father was born into a Jewish family in Minsk, Russian Empire,[4] and immigrated with his parents to the United States at the age of five."
cleaned_text = preprocess_text(sample_text)
print(cleaned_text)
