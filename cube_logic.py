import random

class RubiksCubeLogic:
    def __init__(self):
        # El estado inicial resuelto. 
        # Representamos cada sticker con la inicial de su cara (colores por defecto).
        self.state = {
            'U': ['U'] * 9, 'D': ['D'] * 9,
            'F': ['F'] * 9, 'B': ['B'] * 9,
            'R': ['R'] * 9, 'L': ['L'] * 9
        }
        self.history = []
        
        self.CYCLES = {
            'U': [('F',[0,1,2]), ('L',[0,1,2]), ('B',[0,1,2]), ('R',[0,1,2])],
            'D': [('F',[6,7,8]), ('R',[6,7,8]), ('B',[6,7,8]), ('L',[6,7,8])],
            'R': [('F',[2,5,8]), ('U',[2,5,8]), ('B',[6,3,0]), ('D',[2,5,8])],
            'L': [('F',[0,3,6]), ('D',[0,3,6]), ('B',[8,5,2]), ('U',[0,3,6])],
            'F': [('U',[6,7,8]), ('R',[0,3,6]), ('D',[2,1,0]), ('L',[8,5,2])],
            'B': [('U',[2,1,0]), ('L',[0,3,6]), ('D',[6,7,8]), ('R',[8,5,2])],
        }

    def _rotate_face(self, arr, clockwise=True):
        if clockwise:
            return [arr[6], arr[3], arr[0], arr[7], arr[4], arr[1], arr[8], arr[5], arr[2]]
        else:
            return [arr[2], arr[5], arr[8], arr[1], arr[4], arr[7], arr[0], arr[3], arr[6]]

    def apply_move(self, face, inverse=False, record_history=True):
        # Rotar la cara
        self.state[face] = self._rotate_face(self.state[face], clockwise=not inverse)
        
        # Ciclar los stickers adyacentes
        cyc = list(reversed(self.CYCLES[face])) if inverse else self.CYCLES[face]
        tmp = [self.state[cyc[3][0]][i] for i in cyc[3][1]]
        
        for i in range(3, 0, -1):
            for j, idx in enumerate(cyc[i][1]):
                self.state[cyc[i][0]][idx] = self.state[cyc[i-1][0]][cyc[i-1][1][j]]
        for j, idx in enumerate(cyc[0][1]):
            self.state[cyc[0][0]][idx] = tmp[j]

        if record_history:
            move_str = f"{face}'" if inverse else face
            self.history.append(move_str)

    def is_solved(self):
        for face, stickers in self.state.items():
            if len(set(stickers)) > 1:
                return False
        return True

    def reset(self):
        self.__init__()

    def undo_last_move(self):
        if not self.history:
            return None
        last_move = self.history.pop()
        face = last_move[0]
        inverse = len(last_move) == 1 # Si el último no fue inverso, ahora lo invertimos
        self.apply_move(face, inverse=inverse, record_history=False)
        return last_move

    @staticmethod
    def get_sticker_index(face_type, x, y, z):
        if face_type == 'U': return (z+1)*3 + (x+1)
        if face_type == 'D': return (1-z)*3 + (x+1)
        if face_type == 'F': return (1-y)*3 + (x+1)
        if face_type == 'B': return (1-y)*3 + (1-x)
        if face_type == 'R': return (1-y)*3 + (1-z)
        if face_type == 'L': return (1-y)*3 + (z+1)