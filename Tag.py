import re


class Tag:
    _left_bracket = '([{<（【「『〖〈《＜〔［｛'
    _right_bracket = ')]}>）】」』〗〉》＞〕］｝'
    _bracket_pairs_dictionary = dict()
    for i in range(len(_left_bracket)):
        _bracket_pairs_dictionary[_left_bracket[i]] = _right_bracket[i]
        _bracket_pairs_dictionary[_right_bracket[i]] = _left_bracket[i]

    # separate file names into tag list
    # tag example "(活動名)【譯者(譯者協力)+譯者協力】[作者(作者別名)]作品名(#集數)(原作)(雜誌號)[備註](備註)"
    @staticmethod
    def tag_separator(full_name):
        bracket_stack = []

        tag_list = []
        temp = ""
        for c in full_name:
            if c in Tag._left_bracket:
                if len(bracket_stack) == 0 and len(temp) > 0:
                    tag_list.append(temp)
                    temp = ""
                temp += c
                bracket_stack.append(c)
            elif c in Tag._right_bracket:
                # got unpaired right bracket
                if (not bracket_stack) or bracket_stack.pop() != Tag._bracket_pairs_dictionary[c]:
                    return []
                # all brackets are paired
                elif not bracket_stack:
                    tag_list.append(temp + c)
                    temp = ""
                else:
                    temp += c
            else:
                temp += c

        if len(bracket_stack) == 0:
            for tag in tag_list:
                if tag.isspace():
                    tag_list.remove(tag)
            return tag_list
        else:
            return []

    # guess what is the tag's type
    @staticmethod
    def tag_classifier(tag_list, database):
        table_list = []
        tag_classify_dictionary = dict()
        for tag in tag_list:
            for table in table_list:
                result = database.is_include(tag, table)
                if result == 'unknown':
                    tag_classify_dictionary[tag] = result
            if tag in tag_classify_dictionary:
                tag_classify_dictionary[tag] = 'unknown'

        # decision tree
        # build a 2D array
        #           surround by ()  |   surround by []  |   Found in table 1.....
        # (CXX)     1                   0                   0
        # [Tosh]    0                   1                   1
        # shogugeki 0                   0                   0
        #

        return tag_classify_dictionary

    @staticmethod
    def _is_surrounded_by_bracket(tag, left_bracket, right_bracket):
        return re.search(
            re.escape(left_bracket) + r'.*' + re.escape(right_bracket),
            tag
        ) is not None

    @staticmethod
    def _remove_surrounded_bracket(tag):
        while tag[0] in Tag._left_bracket and\
                Tag._bracket_pairs_dictionary[tag[0]] == tag[-1]:
            tag = tag[1:-1]
        return tag