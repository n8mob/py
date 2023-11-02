class SystemDictionary:
    base_path = '/usr/share/dict/'
    by_length = {}
    by_first_letter = {}
    proper_names = set()

    with open(base_path + 'propernames') as proper_names_file:
        for name in proper_names_file.read().split('\n'):
            if name:
                proper_names.add(name)


    with open(base_path + 'words') as word_list:
        for word in word_list.read().split('\n'):
            if not word or word in proper_names:
                continue
            assert not word[-1] == '\n'

            word = word.lower()

            l = len(word)
            if l not in by_length:
                by_length[l] = set(word)
            else:
                by_length[l].add(word)

            if word[0] not in by_first_letter:
                by_first_letter[word[0]] = [word]
            else:
                by_first_letter[word[0]].append(word)
              
