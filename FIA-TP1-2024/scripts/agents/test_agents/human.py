class HumanAgent:
    def action(self, board):
        col = input("Ingrese la columna (1-16):")
        while col not in [str(i) for i in range(1, 16)]:
            col = input("Ingrese la columna bien!!: ")

        row = input("Ingrese la fila (1-16): ")
        while row not in [str(i) for i in range(1, 16)]:
            row = input("Ingrese la fila bien!!: ")

        return ((int(row) - 1) * board.shape[1]) + int(col) - 1

    def name(self):
        return {"nombre": "Human", "apellido": "Player", "legajo": 2}
