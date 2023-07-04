import re
#EXPRESIONES REGULARES PARA CAPTURAR LAS FECHAS/HORAS DE INICIO/FIN
#primera criba
startTime=re.compile(r"\[StartTime \"\d\d:\d\d:\d\d") 
endTime=re.compile(r"\[EndTime \"\d\d:\d\d:\d\d")
startDate=re.compile(r"\[Date \"\d\d\d\d.\d\d.\d\d") 
endDate=re.compile(r"\[EndDate \"\d\d\d\d.\d\d.\d\d")
#segunda criba
hora=re.compile(r'\d\d:\d\d:\d\d') 
fecha=re.compile(r'\d\d\d\d.\d\d.\d\d') 
#-----------------------------------------------------------------------

#REGEX EN PASSANT

#no hace falta asegurarse de que la pieza que come es un peon porque en el primer caso le decimos que tiene que ser el mismo
#movimiento y en el segundo introducimos literalmente la expresión literal de tiempo del reloj


black_takes_white=re.compile("(\d+). ([abcdefgh])4 .+ (\\1)+... [abcdefgh]x(\\2)3") 
#tuve que añadir por alguna razon misteriosa una backslash a cada numero...

white_takes_black=re.compile("\d+... ([abcdefgh])5 \{\[.clk \d+:\d+:\d+\.\d]} \d+. .x(\\1)6") #idem, hay una backslash añadida
#esta funciona

#------------------------------------------------------------------------------------
is_daily=re.compile('l \\"1/')


