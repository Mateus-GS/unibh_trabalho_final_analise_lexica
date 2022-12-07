import sys
from ts import TS
from tag import Tag
from token import Token

class Lexer():

   '''
   Classe que representa o Lexer (AFD):
   
   [1] Voce devera se preocupar quando incremetar as linhas e colunas,
   assim como, quando decrementar ou reinicia-las. Lembre-se, ambas 
   comecam em 1. Procure a marcacao [TAREFA].
   '''
   def __init__(self, input_file):
      try:
         self.input_file = open(input_file, 'rb')
         self.lookahead = 0
         self.n_line = 1
         self.n_column = 1
         self.ts = TS()
      except IOError:
         print('Erro de abertura do arquivo. Encerrando.')
         sys.exit(0)

   def closeFile(self):
      try:
         self.input_file.close()
      except IOError:
         print('Erro ao fechar arquivo. Encerrando.')
         sys.exit(0)

   def sinalizaErroLexico(self, message):
      print("[Erro Lexico]: ", message, "\n");

   def retornaPonteiro(self):
      '''Metodo importante para retornar a leitura no arquivo,
      uma posicao, ja que um caractere foi lido indicando fim
      de um lexema, porem indicando tambem o inicio de outro
      lexema. Isso esta evidente no AFD na leitura de 'outro'.
      '''
      if(self.lookahead.decode('ascii') != ''):
         self.input_file.seek(self.input_file.tell()-1)

   def printTS(self):
      self.ts.printTS()

   def proxToken(self):
      # Implementa um AFD.
      
      estado = 1
      lexema = ""
      # c = '\u0000'

      while(True):
         self.lookahead = self.input_file.read(1)
         c = self.lookahead.decode('ascii')

         if(estado == 1):
            if(c == ''):
               return Token(Tag.EOF, "EOF", self.n_line, self.n_column)
            elif(c == ' ' or c == '\t' or c == '\n'):
               estado = 1
            elif(c == '='):
               estado = 2
            elif(c == '!'):
               estado = 4
            elif(c == '<'):
               estado = 6
            elif(c == '>'):
               estado = 9
            elif(c.isdigit()):
               lexema += c
               estado = 12
            elif(c.isalpha()):
               lexema += c
               estado = 14
            elif(c == '/'):
               estado = 16
            elif(c == ';'):
               self.n_column += 1
               self.n_line += 1
               return Token(Tag.SMB_PV, ";", self.n_line, self.n_column)
            elif(c == '{'):
               self.n_line += 1
               return Token(Tag.SMB_AC, "{", self.n_line, self.n_column)
            elif(c == '}'):
               self.n_line += 1
               return Token(Tag.SMB_FC, "}", self.n_line, self.n_column)
            else:
               self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               return None
         elif(estado == 2):
            if(c == '='):
               return Token(Tag.OP_IGUAL, "==", self.n_line, self.n_column)
               
            self.retornaPonteiro()
            self.n_column += 1
            return Token(Tag.OP_ATRIB, "=", self.n_line, self.n_column)
         elif(estado == 4):
            if(c == '='):
               self.n_column += 1
               return Token(Tag.OP_DIFERENTE, "!=", self.n_line, self.n_column)

            self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
            str(self.n_line) + " e coluna " + str(self.n_column))
            return None
         elif(estado == 6):
            if(c == '='):
               return Token(Tag.OP_MENOR_IGUAL, "<=", self.n_line, self.n_column)

            self.retornaPonteiro()
            return Token(Tag.OP_MENOR, "<", self.n_line, self.n_column)
         elif(estado == 9):
            if(c == '='):
               return Token(Tag.OP_MAIOR_IGUAL, ">=", self.n_line, self.n_column)

            self.retornaPonteiro()
            return Token(Tag.OP_MAIOR, ">", self.n_line, self.n_column)
         elif(estado == 12):
            if(c.isdigit()):
               lexema += c           
            else:
               self.retornaPonteiro()
               self.n_column += 1
               return Token(Tag.NUM, lexema, self.n_line, self.n_column)
         elif(estado == 14):
            if(c.isalnum()):
               lexema += c
            else:
               self.retornaPonteiro()
               self.n_column = 1
               token = self.ts.getToken(lexema)
               if(token is None):
                  token = Token(Tag.ID, lexema, self.n_line, self.n_column)
                  self.ts.addToken(lexema, token)

               return token
         elif(estado == 16):
             return Token(Tag.SMB_AB, "/", self.n_line, self.n_column)
             estado = 17
         elif(estado == 17):
             if(c == '/'):
                return Token(Tag.SMB_AB, "/", self.n_line, self.n_column)
             elif(c == ' ' or c == '\t' or c == '\n'):
                estado = 1
             else:
                 self.retornaPonteiro()
                 estado = 17
         # [TAREFA 1] Implementar a contagem de linha e coluna.
         # [TAREFA 2 - opcional] Implementar o processamento de comentario no AFD,
         # ou seja, implementar os estados 16 e 17. Essa tarefa vale
         # + 2 pontos extras.

         # fim if's de estados
      # fim while