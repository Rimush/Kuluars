def get_filename(filename):
    return filename.upper()
    
def slugify(string):
    alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
                'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
                'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'i', 'ь': '',
                'э': 'e', 'ю': 'yu', 'я': 'ya', ' ': '-',}
    #return ''.join(alphabet.get(w, w) for w in filter(str.isalpha, string.lower()))
    return ''.join(alphabet.get(w.lower(), w.lower()) for w in string if (w.isalpha() or w.isspace()))
    
