from hazm.Normalizer import InformalNormalizer

inormalizer = InformalNormalizer()

with open("short_comments.txt") as cm:
  fnl, ifnl = inormalizer.normalize(cm.read())
  with open("formal_normalized_comments.txt", 'w') as ncm:
    ncm.write(fnl)
  with open("informal_normalized_comments.txt", 'w') as ncm:
    ncm.write(ifnl)

