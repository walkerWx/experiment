grammar expr;

equation
   : expression relop expression
   ;

rules
   : (singleRule)*
   ;

singleRule
   : variable COLON expression ARROW expression (AT equation)? SEMICOLON
   ;

expression
   : expression (PLUS | MINUS) multiplyingExpression
   | multiplyingExpression 
   ;

multiplyingExpression
   : multiplyingExpression (TIMES | DIV) powExpression
   | powExpression 
   ;

powExpression
   : signedAtom (POW signedAtom)*
   ;

signedAtom
   : PLUS signedAtom
   | MINUS signedAtom
   | func
   | atom
   ;

atom
   : scientific
   | variable
   | constant
   | LPAREN expression RPAREN
   ;

scientific
   : SCIENTIFIC_NUMBER
   ;

constant
   : PI
   | EULER
   | I
   ;

variable
   : VARIABLE
   ;

func
   : funcname LPAREN expression (COMMA expression)* RPAREN
   ;

funcname
   : COS
   | COSH
   | POWF
   | EXP
   | TAN
   | SIN
   | SEC
   | CSC
   | COT
   | ACOS
   | ATAN
   | ASIN
   | LOG
   | LN
   | SQRT
   | GAMMA
   | BERNOULLI
   | SUM
   | ABS
   | FACTORIAL
   | GET_ARC
   ;

relop
   : EQ
   | GT
   | LT
   ;

POWF
   : 'pow'
   ;

EXP
   : 'exp'
   ;

COS
   : 'cos'
   ;

COSH
   : 'cosh'
   ;

SIN
   : 'sin'
   ;


TAN
   : 'tan'
   ;

COT
   : 'cot'
   ;

SEC
   : 'sec'
   ;

CSC
   : 'csc'
   ;

ACOS
   : 'acos'
   ;


ASIN
   : 'asin'
   ;


ATAN
   : 'atan'
   ;


LN
   : 'ln'
   ;


LOG
   : 'log'
   ;


SQRT
   : 'sqrt'
   ;

GAMMA
   : 'gamma'
   ;

BERNOULLI
   : 'bnl'
   ;

SUM
   : 'sum'
   ;

ABS
   : 'abs'
   ;

FACTORIAL
   : 'fac'
   ;

GET_ARC
   : 'get_arc'
   ;

LPAREN
   : '('
   ;


RPAREN
   : ')'
   ;


PLUS
   : '+'
   ;


MINUS
   : '-'
   ;


TIMES
   : '*'
   ;


DIV
   : '/'
   ;


GT
   : '>'
   ;


LT
   : '<'
   ;


EQ
   : '='
   ;


COMMA
   : ','
   ;

COLON
   : ':'
   ;

SEMICOLON
   : ';'
   ;

POINT
   : '.'
   ;


POW
   : '^'
   | '**'
   ;


PI
   : 'pi'
   ;


EULER
   : 'r'
   ;


I
   : 'I'
   ;


ARROW
   : '->'
   ;

AT
   : '@'
   ;

VARIABLE
   : VALID_ID_START VALID_ID_CHAR*
   ;


fragment VALID_ID_START
   : ('a' .. 'z') | ('A' .. 'Z') | '_'
   ;


fragment VALID_ID_CHAR
   : VALID_ID_START | ('0' .. '9')
   ;


SCIENTIFIC_NUMBER
   : NUMBER ((E1 | E2) SIGN? NUMBER)?
   ;


fragment NUMBER
   : ('0' .. '9') + ('.' ('0' .. '9') +)?
   ;


fragment E1
   : 'E'
   ;


fragment E2
   : 'e'
   ;


fragment SIGN
   : ('+' | '-')
   ;

WS
   : [ \r\n\t] + -> skip
   ;
