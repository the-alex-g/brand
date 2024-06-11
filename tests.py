import brand

class Test:
    test = ""
    args = {}

    def __init__(self, test, args):
        self.args = args
        self.test = test
    

    def run(self):
        for test_case in self.args:
            if test_case != "":
                if brand.eval_string("[" + self.test + " " + test_case + "]", []) == self.args[test_case]:
                    continue
            else:
                if brand.eval_string("[" + self.test + "]", []) == self.args[test_case]:
                    continue
            return self.test + " failed"
        return self.test + " passed"


tests = [
    Test("roll", {"1 6 1":"4 (1d6 + 1)"}),
    Test("index_plural", {"1 name":"1 name", "2 name":"2 names", "2 hooch":"2 hooches"}),
    Test("sum", {"1 2 3":"6"}),
    Test("articulate", {"t fudge":"A fudge", "f ant":"an ant"}),
    Test("format_index", {"12":"12th", "5":"5th", "1":"1st", "22":"22nd"}),
    Test("percent", {"":"\\%"}),
]


for test in tests:
    print(test.run())