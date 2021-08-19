class WHERE:
    def __init__(self, **statements: "in form: {col1: eq(5), col2: ge(77), ...}"):
        self.statements = statements

    def __bool__(self):
        return bool(self.statements)

    def handle_statements(self, tablesqla):
        output = []
        for col in self.statements:
            comp = self.statements[col]
            output.append(comp.get_statement(tablesqla.c[col]))
        return output

class comparison:
    def __init__(self, value):
        self.value = value

class eq(comparison):
    id = "eq"
    def get_statement(self, col):
        return col == self.value

class gt(comparison):
    id = "gt"
    def get_statement(self, col):
        return col > self.value

class ge(comparison):
    id = "ge"
    def get_statement(self, col):
        return col >= self.value

class lt(comparison):
    id = "lt"
    def get_statement(self, col):
        return col < self.value

class le(comparison):
    id = "le"
    def get_statement(self, col):
        return col <= self.value

class ne(comparison):
    id = "ne"
    def get_statement(self, col):
        return col != self.value
