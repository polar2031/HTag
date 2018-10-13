import re
# from sklearn import tree


class Tag:
    _left_bracket = '([{<（【「『〖〈《＜〔［｛'
    _right_bracket = ')]}>）】」』〗〉》＞〕］｝'
    _bracket_pairs_dictionary = dict()
    for i in range(len(_left_bracket)):
        _bracket_pairs_dictionary[_left_bracket[i]] = _right_bracket[i]
        _bracket_pairs_dictionary[_right_bracket[i]] = _left_bracket[i]

    def __init__(self, tag_name):
        self.name = Tag._remove_surrounded_bracket(tag_name)
        self.bracket = Tag._get_surrounded_bracket(tag_name)
        self.children = []
        Tag._tag_separator(self)

    def __str__(self):
        s = self.bracket + self.name
        if self.children:
            for ch in self.children:
                s = s + '\n' + str(ch)
        return s

    # separate file names into tag list
    # tag example "(活動名)【譯者(譯者協力)+譯者協力】[作者,作者(社團)]作品名(#集數)(原作)(雜誌號)[備註](備註)"
    @staticmethod
    def _tag_separator(tag):
        bracket_stack = []
        separated_tag_list = []
        temp = ""
        for c in Tag._remove_surrounded_bracket(tag.name):
            if c in Tag._left_bracket:
                if not bracket_stack and len(temp) > 0:
                    separated_tag_list.append(temp)
                    temp = ""
                temp += c
                bracket_stack.append(c)
            elif c in Tag._right_bracket:
                # got unpaired right bracket
                if (not bracket_stack) or bracket_stack.pop() != Tag._bracket_pairs_dictionary[c]:
                    return
                # all brackets are paired
                elif not bracket_stack:
                    separated_tag_list.append(temp + c)
                    temp = ""
                else:
                    temp += c
            elif not c.isalpha() and not bracket_stack:
                if len(temp) > 0:
                    separated_tag_list.append(temp)
                    temp = ""
                separated_tag_list.append(c)
            else:
                temp += c
        if len(temp) > 0:
            separated_tag_list.append(temp)
        if len(bracket_stack) == 0 and len(separated_tag_list) > 1:
            for s in separated_tag_list:
                if not s.isspace():
                    tag.children.append(Tag(s))

    # guess what is the tag's type
    def tag_classifier(self, database):

        # load pretraining data

        # decision tree
        # build a 2D array
        #           surround by ()  |   surround by []  |   Found in table 1.....
        # (CXX)     1                   0                   0
        # [Tosh]    0                   1                   1
        # shogugeki 0                   0                   0
        #

        return

    @staticmethod
    def _get_surrounded_bracket(tag):
        if len(tag) > 1 and \
                tag[0] in Tag._left_bracket and \
                tag[-1] in Tag._right_bracket and \
                Tag._bracket_pairs_dictionary[tag[0]] == tag[-1]:
            return tag[0] + tag[-1]
        else:
            return ""

    @staticmethod
    def _remove_surrounded_bracket(tag):
        if len(tag) > 1 and \
                tag[0] in Tag._left_bracket and \
                tag[-1] in Tag._right_bracket and \
                Tag._bracket_pairs_dictionary[tag[0]] == tag[-1]:
            return tag[1:-1]
        else:
            return tag


if __name__ == '__main__':
    t = Tag('(活動名)【譯者(譯者協力)+譯者協力】[作者,作者(社團)]作品名')
    print(t)