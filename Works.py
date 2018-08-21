class Tag:
    # separate tags
    # tag example "(活動名)【譯者(譯者協力)】[作者(作者別名)]名字(原作)(雜誌號)[備註]"
    def tag_separator(self, full_name):
        bracket_stack = []
        left_bracket = ["(", "[", "（", "【"]
        right_bracket = [")", "]", "）", "】"]
        bracket_pairs = {
            "(": ")", ")": "(",
            "[": "]", "]": "[",
            "（": "）", "）": "（",
            "【": "】", "】": "【"
        }

        tag_list = []
        temp = ""
        for c in full_name:
            if c in left_bracket:
                if len(bracket_stack) == 0 and len(temp) > 0:
                    tag_list.append(temp)
                    temp = ""
                temp += c
                bracket_stack.append(c)
            elif c in right_bracket:
                # got unpaired bracket
                if (not bracket_stack) or bracket_stack.pop() != bracket_pairs[c]:
                    return []
                # all brackets are paired
                elif not bracket_stack:
                    tag_list.append(temp + c)
                    temp = ""
                else:
                    temp += c
            else:
                temp += c
        return tag_list

