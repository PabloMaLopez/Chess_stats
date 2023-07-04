from json import loads
from requests import get
from re import compile
from chessregex import *
from datetime import time , timedelta, datetime

""" DEPRECATED    def date_iterator(username, initial_year, initial_month,final_year, final_month,argument_function): #verano
    if argument_function==wasted_on_chess:#ES POSIBLE QUE EN EL FUTURO TENGA QUE AMPLIAR ESTA LISTA DE FUNCIONES
        collective_sum=timedelta()
    if argument_function==enpassant_counter:
        collective_sum=[]
  
    final_year=int(final_year)
    final_month=int(final_month)
    initial_month=int(initial_month)
    #no hacer calculos innecesarios de cuando la cuenta aún no ha sido creada
    if get_user_creation_date(username).strftime("%Y")>initial_year:
        initial_year=int(get_user_creation_date(username).strftime("%Y"))
        initial_month=int(get_user_creation_date(username).strftime("%m"))

    else:
        initial_year=int(initial_year)
        if int(get_user_creation_date(username).strftime("%m"))>int(initial_month):
            initial_month=int(get_user_creation_date(username).strftime("%m"))
        else:
            initial_month=int(initial_month)
         

    stringlist=["01","02","03","04","05","06","07","08","09","10","11","12"]

    while initial_year < final_year:
        collective_sum+=argument_function(username,str(initial_year),stringlist[initial_month-1])
        initial_month+=1
        if initial_month==13:
            initial_month=1
            initial_year+=1 
            
    while initial_month<=final_month:
            collective_sum+=argument_function(username,str(initial_year),stringlist[initial_month-1])
            initial_month+=1
            if initial_month==13:
                initial_month=1
    return collective_sum  """  

def get_list_of_games(username, initial_year, initial_month, final_year, final_month):

    def get_list_of_games_in_month(username, year, month): ##funcion interna, antigua funcion excerna
        request=get("https://api.chess.com/pub/player/" + username +"/games/" +year +"/"+ month)
    
        try:    
            parsedJson=loads(request.text) 
            return parsedJson["games"] #JSON parseado en una lista de partidas
        except:
            print(year+"/"+month) 
            print("error al realizar la request en este mes") 

    list_of_games=[] #cambiar nombre a list_of_games
    final_year=int(final_year)
    final_month=int(final_month)
    initial_month=int(initial_month)
    #no hacer calculos innecesarios de cuando la cuenta aún no ha sido creada
    if get_user_creation_date(username).strftime("%Y")>initial_year:
        initial_year=int(get_user_creation_date(username).strftime("%Y"))
        initial_month=int(get_user_creation_date(username).strftime("%m"))

    else:
        initial_year=int(initial_year)
        if int(get_user_creation_date(username).strftime("%m"))>int(initial_month):
            initial_month=int(get_user_creation_date(username).strftime("%m"))
        else:
            initial_month=int(initial_month)

    ########################################################################################3

    stringlist=["01","02","03","04","05","06","07","08","09","10","11","12"]

    while initial_year < final_year:
        list_of_games+=get_list_of_games_in_month(username,str(initial_year),stringlist[initial_month-1])
        initial_month+=1
        if initial_month==13:
            initial_month=1
            initial_year+=1 
            
    while initial_month<=final_month:
            list_of_games+=get_list_of_games_in_month(username,str(initial_year),stringlist[initial_month-1])
            initial_month+=1
            if initial_month==13:
                initial_month=1
    return list_of_games    

def get_user_creation_date(username):
    request=get("https://api.chess.com/pub/player/"+ username)
    return datetime.fromtimestamp(loads(request.text)["joined"]).date()

def wasted_on_chess(game_list):
    suma_total= timedelta()

    for element in game_list:#element es un dict

        if "pgn" not in element:#i the dictionary received (element) checks for games without pgn such as bughouse etc
            continue


        try:
            partidaActual=game_list[game_list.index(element)]["pgn"] ###esto creo que lo puedo borrar, es
            #simplemente un debuggeador por si la partida no tiene pgn por ser bughouse o algo
        except:
            print("problema con el pgn en la siguiente partida")
            print(game_list[game_list.index(element)]["url"])

        
        if is_daily.search(partidaActual):
            #print(game_list[game_list.index(element)]["url"]) simple debugeador para comprobar  qué partidas
            continue

        #HORA INICIAL
        result = startTime.search(partidaActual) # PRIMERA CRIBA DE LA REGEX
        horaInicial=hora.search(result.group(0))
            
            #-----------------------------------------------------------------------------------

            #HORAFINAL
        result2 = endTime.search(partidaActual) # PRIMERA CRIBA DE LA REGEX
        horaFinal=hora.search(result2.group(0))#segunda criba
            
            #-----------------------------------------------------------------------------------

            #FECHAINICIAL
        result3 = startDate.search(partidaActual) # PRIMERA CRIBA DE LA REGEX
        fechaInicial=fecha.search(result3.group(0))#segunda criba

            #-----------------------------------------------------------------------------------

           #FECIAFINAL
        result4 = endDate.search(partidaActual) # PRIMERA CRIBA DE LA REGEX
        fechaFinal=fecha.search(result4.group(0))#segunda criba

            #----------------------------------------------------------------------------------

            #ASIGNACIÓN DE PRINCIPIO Y FIN DE LA PARTIDA
        inicio=datetime.strptime(fechaInicial.group(0)+"/"+horaInicial.group(0),r"%Y.%m.%d/%H:%M:%S")
        fin=datetime.strptime(fechaFinal.group(0)+"/"+horaFinal.group(0),r"%Y.%m.%d/%H:%M:%S")
        
        delta=fin-inicio
        suma_total+=delta

    return suma_total

def game_is_rated(partidaActual):
    return partidaActual["rated"]

def get_list_of_games_in_month(username, year, month):
    request=get("https://api.chess.com/pub/player/" + username +"/games/" +year +"/"+ month)
    
    try:    
        parsedJson=loads(request.text) 
        return parsedJson["games"] #JSON parseado en una lista de partidas
    except:
        print(year+"/"+month) 
        print("error al realizar la request en este mes") 

def userisblack(corrected_username,partidaActual):
        
        black= re.search("Black \"" + corrected_username, partidaActual) #COMO ES POSIBLE QUE DE EL MISMO RESULTADO CON UNA STRING RAW QUE SIN ELLA
        
        if black:
            return True
        else:
            return False
        
""" DEPRECATED   def enpassant_counter(username, year, month):
    counter=0
    white_counter=0
    black_counter=0
    lista_enpassant=[]
    
    game_list=get_list_of_games_in_month(username, year, month)

    ############################################# FUNCIÓN DE CORRECTOR DE NOMBRE #################################
    
    def case_corrected_username(username):
        try:
            regex= re.search(username, game_list[0]["pgn"], re.IGNORECASE)
            corrected_username=regex.group()
            return corrected_username
        except IndexError:
            pass
            
    
    corrected_username=case_corrected_username(username)
    
    for element in game_list: #CHECKEA SI (Y CUÁNTAS) HA HABIDO CAPTURAS AL PASO Y LAS SUMA AL CONTADOR TOTAL
        white_counter=0
        black_counter=0
        #DEBUGGING. SHOWS URS OF BUGHOUSE
        ######################################################################################### 
        # try:
        #     partidaActual=game_list[game_list.index(element)]["pgn"] 
        # except:
        #     print("problema con el pgn en la siguiente partida")
        #     print(game_list[game_list.index(element)]["url"])
        #############################################################################################

        if "pgn" not in element:#checks for games without pgn such as bughouse etc
            continue

        partidaActual=element["pgn"]
        if game_is_rated(element):
            # print(userisblack(username, partidaActual))
            if userisblack(corrected_username,partidaActual): #Cuando blanco come a negro
                if match:=black_takes_white.findall(partidaActual):
                    counter+=match.__len__() 
                    black_counter+=match.__len__() 
                    lista_enpassant.append(element["url"]) #DEBUGGING. SHOWS URL OF ENPASSANT GAMES

            if not userisblack(corrected_username, partidaActual):#cuando negro come a blanco
                if match:=white_takes_black.findall(partidaActual):               
                    counter+=match.__len__() 
                    white_counter+=match.__len__() 
                    lista_enpassant.append(element["url"]) #DEBUGGING. SHOWS URL OF ENPASSANT GAMES

    #contadores_individuales--------------------------------------------------------------------           
    # print("black_counter="+str(black_counter))
    # print("white_counter="+str(white_counter))
    #-------------------------------------------------------------------------------------------
    
    return lista_enpassant  """
    
def get_games_url(list_of_games):
    url_list=[]
    for i in list_of_games:
        url_list.append(i["url"])
    return url_list

def get_enpassant_list_of_games(username, game_list):
    counter=0
    white_counter=0
    black_counter=0
    lista_enpassant=[]
    def case_corrected_username(username):
        i=0
        j=False
        while j==False:
            try:
                regex= re.search(username, game_list[i]["pgn"], re.IGNORECASE)
                corrected_username=regex.group()
                j=True
                return corrected_username
            except IndexError:
                pass
                i=+1##### por si el valiente gilipollas se ha creado al cuenta y ha decidido lo primero echar una bughouse
            
    
    corrected_username=case_corrected_username(username) # (verano) aquí se corrige el nombre que usaremos luego
    
    ############################################# FUNCIÓN DE CORRECTOR DE NOMBRE #################################
       
    
    
    for element in game_list: #CHECKEA SI (Y CUÁNTAS) HA HABIDO CAPTURAS AL PASO Y LAS SUMA AL CONTADOR TOTAL
        white_counter=0
        black_counter=0
        #DEBUGGING. SHOWS URS OF BUGHOUSE
        ######################################################################################### 
        # try:
        #     partidaActual=game_list[game_list.index(element)]["pgn"] 
        # except:
        #     print("problema con el pgn en la siguiente partida")
        #     print(game_list[game_list.index(element)]["url"])
        #############################################################################################

        if "pgn" not in element:#checks for games without pgn such as bughouse etc
            continue

        partidaActual=element["pgn"]
        if game_is_rated(element):
            # print(userisblack(username, partidaActual))
            if userisblack(corrected_username,partidaActual): #Cuando blanco come a negro (verano ?????? debe ser un lapsus)
                if match:=black_takes_white.findall(partidaActual):
                    counter+=match.__len__() 
                    black_counter+=match.__len__() 
                    lista_enpassant.append(element) #DEBUGGING. SHOWS URL OF ENPASSANT GAMES

            if not userisblack(corrected_username, partidaActual):#cuando negro come a blanco
                if match:=white_takes_black.findall(partidaActual):               
                    counter+=match.__len__() 
                    white_counter+=match.__len__() 
                    lista_enpassant.append(element) #DEBUGGING. SHOWS URL OF ENPASSANT GAMES

    #contadores_individuales--------------------------------------------------------------------           
    # print("black_counter="+str(black_counter))
    # print("white_counter="+str(white_counter))
    #-------------------------------------------------------------------------------------------
    
    return lista_enpassant