from typing import List, Tuple, Dict
from src.sentence_analyzer.word import Word
from src.sentence_analyzer.argument import Argument
from src.sentence_analyzer.query import Query
from src.query_handling.tag_condition import PatternMatcher, AndMultiTagCondition, OrMultiTagCondition, AndTagCondition, OrTagCondition

ALL = -1


class QueryPattern:
    def __init__(
            self,
            conditions: List[AndTagCondition | OrTagCondition | AndMultiTagCondition | OrMultiTagCondition],
            required_argument_type: str = None,
            required_arguments: Dict[str, int] = None,
    ):
        self.pattern_matcher = PatternMatcher(conditions)
        self.conditions = conditions
        self.required_argument_type = required_argument_type
        self.required_arguments = required_arguments
        assert not (required_argument_type and required_arguments)

    def match(self, query: Query) -> Tuple[bool, List[Word], List[Argument]]:
        query_tag_structure = query.query_tag_structure
        res = None
        all_used_words = []
        used_args = []

        if self.required_argument_type:
            if self.required_argument_type in query.arguments:
                res = True
                used_args = query.arguments[self.required_argument_type][:1]
            else:
                res = False

        if self.required_arguments:
            for arg_type, num in self.required_arguments.items():
                if arg_type in query.arguments:
                    required_arguments_num = len(query.arguments[arg_type])
                    if num == ALL and required_arguments_num > 0:
                        res = True
                        used_args = query.arguments[arg_type]
                    elif required_arguments_num >= num:
                        res = True
                        used_args = query.arguments[arg_type][:num]
                    else:
                        res = False
                else:
                    res = False

        match_res, used_words = self.pattern_matcher.match_pattern(query_tag_structure)
        if match_res:
            all_used_words += used_words
        if res is None:
            res = match_res
        else:
            res *= match_res
        return res, all_used_words, used_args

    def __str__(self):
        conditions = ' '.join([str(cond) for cond in self.conditions])
        conditions_without_first_word = conditions.split()[1:]
        conditions = ' '.join(conditions_without_first_word)
        if self.required_argument_type:
            arguments = f'{self.required_argument_type}: 1'
        elif self.required_arguments:
            arguments = ' '.join([f'{argument}: {num if num != ALL else "ALL"}'
                                  for argument, num in self.required_arguments.items()])
        else:
            arguments = ''

        return f'Аргументы: {arguments.ljust(20)} | Условие: {conditions}'