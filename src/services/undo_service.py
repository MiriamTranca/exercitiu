class FunctionCall:
    def __init__(self, function_name, *function_arguments):
        self.__function_name = function_name
        self.__function_parameters = function_arguments

    def call(self):
        self.__function_name(*self.__function_parameters)

    def __call__(self, *arguments, **key_arguments):
        self.call()

class Operation:
    def __init__(self, function_undo: FunctionCall, function_redo: FunctionCall):
        self.__function_undo = function_undo
        self.__function_redo = function_redo

    def undo(self):
        self.__function_undo()

    def redo(self):
        self.__function_redo()

class CascadedOperation:
    def __init__(self, *operations):
        self.__operations = operations

    def undo(self):
        for operation in self.__operations:
            operation.undo()

    def redo(self):
        for operation in self.__operations:
            operation.redo()

class UndoError(Exception):
    pass

class UndoService:
    def __init__(self):
        self.__history = []
        self.__index = -1

    def recordUndo(self, operation: Operation):
        self.__history.append(operation)
        self.__index = len(self.__history) - 1

    def undo(self):
        if self.__index == -1:
            raise UndoError("No more undos available")

        self.__history[self.__index].undo()
        self.__index -= 1

    def redo(self):
        if self.__index == len(self.__history) - 1:
            raise UndoError("No more redos available")

        self.__index += 1
        self.__history[self.__index].redo()