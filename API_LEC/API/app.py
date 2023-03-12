#LEC API Guillermo López Sanz

from flask import Flask, request, render_template, jsonify, abort
from flask_cors import CORS, cross_origin
import sqlite3

application = Flask(__name__)
cors = CORS()
application.config['CORS_HEADERS'] = 'Content-Type'

#funcion inicial para crear o conectar a la bbdd y crear tablas si no existen
@application.route("/init")
def iniciar():
    con = sqlite3.connect("lec.db")
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS TEAMS(NAME,WINS,DEFEATS)')
    cur.execute('CREATE TABLE IF NOT EXISTS PLAYERS(NAME,TEAM,POSITION)')
    cur.execute('CREATE TABLE IF NOT EXISTS POSITIONS(POSITION)')
    cur.execute('CREATE TABLE IF NOT EXISTS RESULTS(TEAM1,TEAM2,WINNER)')
    con.close()
    return "API STARTED CORRECTLY!",200

#Obtener json de todos los equipos con sus datos
@application.route("/teams",methods = ['GET'])
def get_teams():
    con = sqlite3.connect("lec.db")
    cur = con.cursor()
    teams = cur.execute('SELECT * FROM TEAMS;')
    cont = 0
    json={}
    for row in teams:
        json[cont]={}
        json[cont]["name"]=row[0]
        json[cont]["wins"]=row[1]
        json[cont]["defeats"]=row[2]
        cont+=1
    con.close()
    return json,200

#Obtener JSON con resultados
@application.route("/results",methods = ['GET'])
def get_results():
    con = sqlite3.connect("lec.db")
    cur = con.cursor()
    results = cur.execute('SELECT * FROM RESULTS;')
    cont = 0
    json={}
    for row in results:
        json[cont]={}
        json[cont]["local"]=row[0]
        json[cont]["visitor"]=row[1]
        json[cont]["winner"]=row[2]
        cont+=1
    con.close()
    return json,200

#Obtener json de jugadores
@application.route("/players",methods = ['GET'])
def get_players():
    con = sqlite3.connect("lec.db")
    cur = con.cursor()
    players = cur.execute('SELECT * FROM PLAYERS;')
    cont = 0
    json={}
    for row in players:
        json[cont]={}
        json[cont]["name"]=row[0]
        json[cont]["team"]=row[1]
        json[cont]["position"]=row[2]
        cont+=1
    con.close()
    return json,200

#Obtener json de posiciones
@application.route("/positions",methods = ['GET'])
def get_positions():
    con = sqlite3.connect("lec.db")
    cur = con.cursor()
    players = cur.execute('SELECT * FROM POSITIONS;')
    cont = 0
    json={}
    for row in players:
        json[cont]={}
        json[cont]["position"]=row[0]
        cont+=1
    con.close()
    return json,200
   
#Insert player a traves de un template
@application.route("/insert_player",methods=['GET'])
def render_insertplayer():
    con = sqlite3.connect("lec.db")
    cur = con.cursor()
    teams = cur.execute('SELECT NAME FROM TEAMS;')
    array_teams=[]
    for row in teams:
        array_teams.append(row[0])
    positions = cur.execute('SELECT POSITION FROM POSITIONS;')
    array_positions = []
    for row2 in positions:
        array_positions.append(row2[0])    
    con.close()
    data = {
        "teams" :array_teams,
        "positions": array_positions
    }
    return render_template('insert_player.html',**data),200

@application.route("/insert_player", methods=['POST'])
def insert_player():
    name = request.form["name"]
    team = request.form["team"]
    position = request.form["position"]
    if name != None and name != '' and team!='null' and position!='null':
        con = sqlite3.connect("lec.db")
        cur = con.cursor()
        data = ()
        data = (name,team,position)
        cur.execute('INSERT INTO PLAYERS VALUES (?,?,?)',data)
        con.commit()
        con.close()
        return "PLAYER "+data[0]+", "+data[1]+", "+data[2]+" INTROUCED",200
    else:
        abort(404)

#Renders para errores 400 y 404
@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@application.errorhandler(400)
def page_not_found2(e):
    return render_template('400.html'), 400

#Delete player sin template (navegador no coge, hacerlo mediante herramientas como postman)
@application.route("/delete_player", methods=['DELETE'])
def delete_player():
    name = request.args.get("name")
    con = sqlite3.connect("lec.db")
    cur = con.cursor()
    players = cur.execute('SELECT NAME FROM PLAYERS;')
    players_array=[]
    for row in players:
        players_array.append((row[0]))
    if name != None:
        if name in players_array:
            cur.execute('DELETE FROM PLAYERS WHERE NAME=?',(name,))
            con.commit()
            con.close()
            return "PLAYER "+name+" WAS DELETED",200
        else:
            abort(404)
    else:
        abort(400)

#Put player sin template (navegador no coge, hacerlo mediante herramientas como postman)
@application.route("/modify_player",methods=['PUT'])
def modify_player():
    name = request.args.get("name",None,str)
    team = request.args.get("team",None,str)
    position = request.args.get("position",None,str)
    con = sqlite3.connect("lec.db")
    cur = con.cursor()
    players = cur.execute('SELECT NAME FROM PLAYERS;')
    players_array = []
    for row in players:
        players_array.append(row[0])
    positions = cur.execute('SELECT POSITION FROM POSITIONS;')
    positions_array=[]
    for row in positions:
        positions_array.append(row[0])
    teams = cur.execute('SELECT NAME FROM TEAMS;')
    teams_array=[]
    for row in teams:
        teams_array.append(row[0]) 
    if name in players_array:
        if team != None and position !=None and team in teams_array and position in positions_array:
            cur.execute('UPDATE PLAYERS SET TEAM=?,POSITION=? WHERE NAME=?',(team,position,name))
            con.commit()
            con.close()
            return "PLAYER UPDATED",200
        elif team!=None and team in teams_array:
            cur.execute('UPDATE PLAYERS SET TEAM=? WHERE NAME=?',(team,name))
            con.commit()
            con.close()
            return "PLAYER UPDATED",200
        elif position!=None and position in positions_array:
            cur.execute('UPDATE PLAYERS SET POSITION=? WHERE NAME=?',(position,name))
            con.commit()
            con.close()
            return "PLAYER UPDATED",200
        else:
            abort(400)
    else:
        abort(400)

#Put team sin template (navegador no coge, hacerlo mediante herramientas como postman)
@application.route('/modify_team',methods=['PUT'])
def modify_team():
    new_team = request.args.get("new-team",None,str)
    team = request.args.get("team",None,str)
    con = sqlite3.connect("lec.db")
    cur = con.cursor()
    teams = cur.execute('SELECT * FROM TEAMS;')
    teams_array = []
    for row in teams:
        teams_array.append(row[0])
    if team in teams_array:
        if new_team!=None:
            cur.execute('UPDATE TEAMS SET NAME=? WHERE NAME=?',(new_team,team))
            cur.execute('UPDATE PLAYERS SET TEAM=? WHERE TEAM=?',(new_team,team))
            con.commit()
            con.close()
            return "TEAM AND PLAYERS OF THAT TEAM UPDATED",200
        else: 
            abort(400)
    else:
        abort(400)

#Insert resultado a través de template
@application.route('/new_result',methods=['GET'])
def render_result():
    con = sqlite3.connect("lec.db")
    cur = con.cursor()
    teams = cur.execute('SELECT * FROM TEAMS;')
    teams_array = []
    for row in teams:
        teams_array.append(row[0])
    con.close()
    return render_template('insert_result.html',teams=teams_array)

@application.route("/new_result", methods=['POST'])
def insert_result():
    team1 = request.form["team1"]
    team2 = request.form["team2"]
    winner = request.form["winner"]

    if team1 != None and team1 != 'null'and team2!=None and team2!='null' and winner!=None and winner!='null' and (winner == team1 or winner==team2):
        con = sqlite3.connect("lec.db")
        cur = con.cursor()
        teams = cur.execute('SELECT * FROM TEAMS;')
        teams_array = []
        for row in teams:
            teams_array.append(row[0])
        print(team1+" "+team2+" "+winner)
        print(teams_array)
        if team1 in teams_array and team2 in teams_array and team1!=team2:
            data=()
            data= (team1,team2,winner)
            cur.execute('INSERT INTO RESULTS VALUES (?,?,?)',data)
            if winner==team1:
                wins1 = cur.execute('SELECT WINS FROM TEAMS WHERE NAME=?',(team1,))
                wins1_array = []
                for row in wins1:
                    wins1_array.append(row[0])

                wins1_num = wins1_array[0]
                wins1_num = int(wins1_num)
                wins1_num+=1
                cur.execute('UPDATE TEAMS SET WINS=? WHERE NAME=?',(wins1_num,team1))
                defs2 = cur.execute('SELECT DEFEATS FROM TEAMS WHERE NAME=?',(team2,))
                defs2_array = []
                for row in defs2:
                    defs2_array.append(row[0])
                defs2_num = defs2_array[0]
                defs2_num = int(defs2_num)
                defs2_num+=1
                cur.execute('UPDATE TEAMS SET DEFEATS=? WHERE NAME=?',(defs2_num,team2))
                con.commit()
                con.close()
                return "RESULT "+team1+"-"+team2+"  WINNER:"+winner+" INTROUCED",200
            else:
                wins2 = cur.execute('SELECT WINS FROM TEAMS WHERE NAME=?',(team2,))
                wins2_array = []
                for row in wins2:
                    wins2_array.append(row[0])
                
                wins2_num = wins2_array[0]
                wins2_num = int(wins2_num)
                wins2_num+=1
                cur.execute('UPDATE TEAMS SET WINS=? WHERE NAME=?',(wins2_num,team2))
                defs1 = cur.execute('SELECT DEFEATS FROM TEAMS WHERE NAME=?',(team1,))
                defs1_array = []
                for row in defs1:
                    defs1_array.append(row[0])
                defs1_num = defs1_array[0]
                defs1_num = int(defs1_num)
                defs1_num+=1
                cur.execute('UPDATE TEAMS SET DEFEATS=? WHERE NAME=?',(defs1_num,team1))
                con.commit()
                con.close()
                return "RESULT "+team1+"-"+team2+"  WINNER:"+winner+" INTROUCED",200
        else:
            abort(400)
    else:
        abort(400)

#Vista de la clasificacion   
@application.route('/leaderboard', methods=['GET'])
def clasificacion():
    con = sqlite3.connect("lec.db")
    cur = con.cursor()
    tabla = cur.execute('SELECT * FROM TEAMS ORDER BY WINS DESC, DEFEATS ASC')
    tabla_array = []
    for i in tabla:
        equipo = []
        for j in i:
            equipo.append(j)
        tabla_array.append(equipo)
    con.close()
    return render_template("table.html",tabla=tabla_array),200

#Vista de un equipo (stats y jugadores)
@application.route('/team_view',methods=['GET'])
def render_team():
    con = sqlite3.connect("lec.db")
    cur = con.cursor()
    teams = cur.execute('SELECT NAME FROM TEAMS;')
    array_teams=[]
    for row in teams:
        array_teams.append(row[0])  
    con.close()
    return render_template('select_team.html',teams=array_teams),200

@application.route('/team_view',methods=['POST'])
def team_view():
    team = request.form['team']
    if team!=None and team!="null":
        con = sqlite3.connect("lec.db")
        cur = con.cursor()
        players = cur.execute('SELECT * FROM PLAYERS WHERE TEAM=?',(team,))
        players_array=[]
        for row in players:
            player= []
            for i in row:
                player.append(i)
            players_array.append(player)
        equipo = cur.execute('SELECT * FROM TEAMS WHERE NAME=?',(team,))
        for i in equipo:
            equipo = []
            for j in i:
                equipo.append(j)   
        return render_template('team.html',team=equipo,players = players_array,name=team)
    else:
        abort(400)

#Json de equipo (info del club y jugadores) a través de query string params
@application.route('/team',methods=['GET'])
def team():
    team = request.args.get('name')
    con = sqlite3.connect("lec.db")
    cur = con.cursor()
    teams = cur.execute('SELECT NAME FROM TEAMS')
    teams_array = []
    for row in teams:
        teams_array.append(row[0])
    if team!=None and team in teams_array:
        json = {}
        players = cur.execute('SELECT * FROM PLAYERS WHERE TEAM=?',(team,))
        players_array=[]
        for row in players:
            player= []
            for i in row:
                player.append(i)
            players_array.append(player) 
        equipo = cur.execute('SELECT * FROM TEAMS WHERE NAME=?',(team,))
        for i in equipo:
            equipo = []
            for j in i:
                equipo.append(j)   
        json['club'] = {'name':equipo[0],'wins':equipo[1],'defeats':equipo[2]}
        jugadores=[]
        playersjson = {}
        for i in players_array:    
            playersjson[i[0]]={'team':i[1],'pos':i[2]}
        jugadores.append(playersjson)
        json['players']=jugadores
        return json   
    else:
        abort(400)

#reset de la bbdd      
@application.route("/reset",methods=['DELETE'])
def reset():
    con = sqlite3.connect("lec.db")
    cur = con.cursor()
    cur.execute('DELETE * FROM TEAMS') 
    cur.execute('DELETE * FROM PLAYERS') 
    cur.execute('DELETE * FROM RESULTS')
    con.commit()
    con.close()
    return "OK",200 