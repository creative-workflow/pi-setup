import os, re

def collect_files(path):
  if os.path.isfile(path):
    return [path]

  files = []
  for dirname, dirnames, filenames in os.walk(path):
    for filename in filenames:
      files.append(os.path.join(dirname, filename))

  return files

def filter_files(files, exclude_pattern):
  result = []
  for check_file in files:
    append = True
    for ex in exclude_pattern:
      if re.search(ex, check_file):
        append = False
        break

    if append: result.append(check_file)

  return result
