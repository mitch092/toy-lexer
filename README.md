# toy-lexer
This is a lexer for a very simple, imaginary programming language called "TinyPie". This language only has the keywords "if", "else" and "int". The only supported opperators are "=", "+" and ">". The supported separators are "(", ")", ":" and all quotation marks. Identifiers are letters or letters followed by digits. Literals are integers embedded into the source code. 
# examples
"int A1 = 5" should produce the following list of tokens: "<keyword,int>,<identifier,A1>,<operator,=>,<literal,5>"
"int result=   A1  +5  +   B2" should also print the correct tokens, and adding extra spaces or formatting strangely will not change the tokens produced.
Another example:
"if result  >10):
    print("Hello world   "    )"
