from tag import Tag
from token import Token
from lexer import Lexer

'''
Esse eh o programa principal. Basta executa-lo.
'''

if __name__ == "__main__":
   lexer = Lexer('prog1.txt')

   print("\n=>Lista de tokens:")
   token = lexer.proxToken()
   linha = 1
   coluna = 0

   while(token is not None and token.getNome() != Tag.EOF):
      coluna += 1
      print(token.toString(), "Linha: " + str(linha) + " Coluna: " + str(coluna))
      if str(token.toString()) == '<SMB_PV, ";">' or str(token.toString()) == '<SMB_FC, "}">' or str(token.toString()) == '<SMB_AC, "{">':
         linha += 1
         coluna = 0
      token = lexer.proxToken()

   print("\n=>Tabela de simbolos:")
   lexer.printTS()
   lexer.closeFile()
    
   print('\n=> Fim da compilacao')