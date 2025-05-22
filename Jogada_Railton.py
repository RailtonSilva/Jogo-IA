import numpy as np

NAME = "Railton"

def jogada(board, piece):
  
    profundidade_maxima = 4  
    coluna, _ = minimax(board, profundidade_maxima, -np.inf, np.inf, True, piece)
    return coluna

def minimax(board, profundidade, alfa, beta, maximizando, piece):
    opponent_piece = 1 if piece == 2 else 2

    if profundidade == 0 or checar_vitoria(board, piece) or checar_vitoria(board, opponent_piece):
        return None, avaliar_board(board, piece)
    
    if maximizando:
        valor_max = -np.inf
        melhor_coluna = np.random.choice([c for c in range(7) if board[0, c] == 0])  
        for coluna in range(7):
            if board[0, coluna] == 0:
                linha = obter_linha_vazia(board, coluna)
                board[linha, coluna] = piece
                _, novo_valor = minimax(board, profundidade - 1, alfa, beta, False, piece)
                board[linha, coluna] = 0 
                if novo_valor > valor_max:
                    valor_max = novo_valor
                    melhor_coluna = coluna
                alfa = max(alfa, valor_max)
                if alfa >= beta:
                    break
        return melhor_coluna, valor_max

    else:
        valor_min = np.inf
        melhor_coluna = np.random.choice([c for c in range(7) if board[0, c] == 0])  
        for coluna in range(7):
            if board[0, coluna] == 0:
                linha = obter_linha_vazia(board, coluna)
                board[linha, coluna] = opponent_piece
                _, novo_valor = minimax(board, profundidade - 1, alfa, beta, True, piece)
                board[linha, coluna] = 0  
                if novo_valor < valor_min:
                    valor_min = novo_valor
                    melhor_coluna = coluna
                beta = min(beta, valor_min)
                if alfa >= beta:
                    break
        return melhor_coluna, valor_min

def obter_linha_vazia(board, coluna):
    for linha in range(5, -1, -1):
        if board[linha, coluna] == 0:
            return linha

def checar_vitoria(b, p):
    for LN in range(6):
        for CL in range(4):
            if np.all(b[LN, CL:CL + 4] == p):
                return True
    for LN in range(3):
        for CL in range(7):
            if np.all(b[LN:LN + 4, CL] == p):
                return True
    for LN in range(3):
        for CL in range(4):
            if all(b[LN + i, CL + i] == p for i in range(4)) or \
               all(b[LN + 3 - i, CL + i] == p for i in range(4)):
                return True
    return False

def avaliar_board(board, piece):
    opponent_piece = 1 if piece == 2 else 2
    score = 0
   
    center_array = [int(board[i][3]) for i in range(6)]
    score += center_array.count(piece) * 3

    for r in range(6):
        row_array = [int(i) for i in board[r, :]]
        for c in range(4):
            janela = row_array[c:c + 4]
            score += avaliar_janela(janela, piece)
    
  
    for c in range(7):
        col_array = [int(board[r][c]) for r in range(6)]
        for r in range(3):
            janela = col_array[r:r + 4]
            score += avaliar_janela(janela, piece)
    
   
    for r in range(3):
        for c in range(4):
            janela = [board[r + i][c + i] for i in range(4)]
            score += avaliar_janela(janela, piece)
        for c in range(4):
            janela = [board[r + 3 - i][c + i] for i in range(4)]
            score += avaliar_janela(janela, piece)
    
    return score

def avaliar_janela(janela, piece):
    opponent_piece = 1 if piece == 2 else 2
    score = 0
    if janela.count(piece) == 4:
        score += 100
    elif janela.count(piece) == 3 and janela.count(0) == 1:
        score += 5
    elif janela.count(piece) == 2 and janela.count(0) == 2:
        score += 2
    if janela.count(opponent_piece) == 3 and janela.count(0) == 1:
        score -= 4
    return score
