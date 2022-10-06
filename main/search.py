def search(search_text, samples):
  search_text = search_text.lower()
  samples_unaltered = samples
  samples = list(map(lambda x:x.lower(), samples))
  def by_word():
    result = []
    tokens = map(lambda s:s.replace(' ',''), search_text.split(" "))
    for token in tokens:
        for sample in samples:
            if token in sample:
                result.append(sample)
    return result
  def by_char():
    result = []
    for sample in samples:
        c = all([char in sample for char in search_text])
        if c:
            result.append(sample)
    return result
  result = []
  w = by_word()
  c = by_char()
  #Append by word first. Results by word take higher priority
  if w:
    for res in w:
      res = samples_unaltered[samples.index(res)]
      if res not in result:
        result.append(res)
  #Then by character.
  if c:
    for res in c:
      res = samples_unaltered[samples.index(res)]
      if res not in result:
        result.append(res)

  return result
