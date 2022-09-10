import numpy as np
import pandas as pd
from prettytable import PrettyTable, ALL
from termcolor import colored
import nltk


class Compiler:
    def __init__(self, input_string):
        self.sentence = input_string
        self.input_string = input_string + "$"
        self.parse_table = self.make_table()
        self.stack = ["$"]
        self.grammar = "S -> 'a' S S 'b' | 'c'"
        self.input_state = []
        self.stack_state = []
        self.table_state = []
        self.action_state = []

    def make_table(self):

        values = np.array(
            [
                ["=.", "<.", "=.", "<.", "-"],
                ["=.", "<.", "-", "<.", "-"],
                ["-", ".>", ".>", ".>", ".>"],
                ["-", ".>", ".>", ".>", ".>"],
                ["-", "<.", "-", "<.", "-"],
            ]
        )
        names = ["s", "a", "b", "c", "$"]
        table = pd.DataFrame(data=values, index=names, columns=names)
        return table

    def detect_handle(self):

        temp = [i for i in reversed(self.stack)]
        try:
            target_index = temp.index("<.") + 1
        except ValueError:
            target_index = None

        temp = temp[:target_index]
        temp = [i for i in reversed(temp)]
        handle = "".join(temp)
        if handle == "<.assb" or handle == "<.c":
            return True
        else:
            return False

    def reduce(self):

        temp = [i for i in reversed(self.stack)]
        try:
            target_index = temp.index("<.") + 1
        except ValueError:
            target_index = None

        temp = temp[target_index:]
        self.stack = [i for i in reversed(temp)]
        self.stack.append("s")

    def shift(self, symbol):

        if symbol == "<.":
            self.stack.append("<.")
            self.stack.append(self.input_string[0])
            self.input_string = self.input_string[1:]
        if symbol == "=.":
            self.stack.append(self.input_string[0])
            self.input_string = self.input_string[1:]

    def parser(self):

        result = True
        while True:

            if (
                self.input_string[0] != "a"
                and self.input_string[0] != "b"
                and self.input_string[0] != "c"
                and self.input_string[0] != "$"
            ):
                result = False
                break

            elif self.parse_table.at[self.stack[-1], self.input_string[0]] == "<.":
                self.stack_state.append([item for item in self.stack])
                self.input_state.append(self.input_string)
                self.table_state.append(self.stack[-1] + "<." + self.input_string[0])
                self.action_state.append("Shift")
                self.shift("<.")

            elif self.parse_table.at[self.stack[-1], self.input_string[0]] == "=.":
                self.stack_state.append([item for item in self.stack])
                self.input_state.append(self.input_string)
                self.table_state.append(self.stack[-1] + "=." + self.input_string[0])
                self.action_state.append("Shift")
                self.shift("=.")

            elif self.parse_table.at[self.stack[-1], self.input_string[0]] == ".>":
                if self.detect_handle():
                    self.stack_state.append([item for item in self.stack])
                    self.input_state.append(self.input_string)
                    self.table_state.append(
                        self.stack[-1] + ".>" + self.input_string[0]
                    )
                    self.action_state.append("Reduce")
                    self.reduce()
                else:
                    result = False
                    break

            elif len(self.stack) == 2 and self.stack[1] == "s":
                self.stack_state.append([item for item in self.stack])
                self.input_state.append(self.input_string)
                self.action_state.append(colored("ACCEPT", "green", attrs=["bold"]))
                self.table_state.append(colored("ACCEPT", "green", attrs=["bold"]))
                break

            else:
                result = False
                break

        self.result_table(result)

    def make_tree(self):
        grammer2 = nltk.CFG.fromstring(
            """
        S -> S0 S1 | 'c'
        S0 -> 'a' S S 
        S1 -> 'b'
        """
        )
        tokenized_sentence = " ".join(self.sentence).split()
        parser1 = nltk.ChartParser(nltk.CFG.fromstring(self.grammar))
        parser2 = nltk.ChartParser(grammer2)
        tree1 = list(parser1.parse(tokenized_sentence))
        tree2 = list(parser2.parse(tokenized_sentence))
        tree2[0].pretty_print()
        tree1[0].draw()

    def result_table(self, result):

        if result:
            pretty_table = PrettyTable()
            pretty_table.add_column("STACK", [item for item in self.stack_state])
            pretty_table.add_column("INPUT", [item for item in self.input_state])
            pretty_table.add_column(
                "CONSIDERATION", [item for item in self.table_state]
            )
            pretty_table.add_column("ACTION", [item for item in self.action_state])
            pretty_table.hrules = ALL
            print(pretty_table.get_string(title="Analysis Steps"))
            self.make_tree()
        if not result:
            print(colored("REJECT", "red", attrs=["bold"]))

    def UI(self):
        pretty_table = PrettyTable()
        pretty_table.add_column("GRAMMER", [self.grammar])
        pretty_table.add_column("PARSE TABLE", [self.parse_table])
        pretty_table.add_column("INPUT", [input_string])
        print(pretty_table)


if __name__ == "__main__":
    input_string = input("Enter A String : ")
    c = Compiler(input_string)
    c.UI()
    c.parser()

# acaccbb
# aaccbaccbb
# aacaccbbcb
# aaaccbaaccbcbbaaccbcbb
