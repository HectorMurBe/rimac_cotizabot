
# -*- coding: utf-8 -*-
import rivescript
import interaction
import re
import diccs
import pickle
import os
def give_card(text,card_options):
    buttons=[]
    for option in card_options:
        buttons.append({
            "type":"postback",
            "tittle":option,
            "payload":"DEVELOPER_DEFINED_PAYLOAD"
        })

    message={
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"button",
            "text":text,
            "buttons":buttons
                    }
          }
          }
    return message
def give_text(text):
    message= {'text':text}

    return message
def give_final_offer(semantic):#TONYX AQUI ES DONDE HAY QUE PEDIR AL SERVIDOR LOS DATOS DE LA TARJETA
    #POR AHORA SOLO RESPONDE TEXTO
    #nota los botones ayudan a poder hacer nuevas peticiones es importante dejarlos
    return give_card("Se ofrece seguro con características: "+str(semantic),["confirmo","nueva consulta"])
    

def open_list(path):
    return pickle.load(open(path, "rb" ) )
def save_list(path,semantic):
    return pickle.dump(semantic,open(path, "wb"))
def get_response(message):
    message=message.lower().replace("?","")
    message=message.lower()
    bot_ans=interaction.get_bot_subs(message,"chepix")
    #semantic representated as an array which has [brand,model,year,gasConverted]
    #load semantic
    path=os.path.realpath("./string_cache/semantic.pkl")
    semantic=open_list(path)
    print semantic
    #charge semantic diferent values
    model = re.search('(?<=md )\w+',bot_ans)#modelos
    brand = re.search('(?<=mr )\w+',bot_ans)#marcas
    if brand!= None:
        semantic[0]=brand.group(0)
        if model ==None:
            semantic[1]=''
    if model != None:
        semantic[1]=model.group(0)
        semantic[0]=diccs.modelos[semantic[1]][0]
        print diccs.modelos[semantic[1]][0]
    #hardcode for year
    for word in bot_ans.split(" "):
        if word.isdigit():
            if len(word)==4:
                if int(word)>1970 and int(word)<2018:
                    semantic[2]=word
                else:
                    return give_text("El año debe ser mayor a 1970 y menor a 2017")
            if len(word)==2:
                if int(word)>70 and int(word)<=99:
                    semantic[2]='19'+word
                if int(word)>=0 and int(word)<18:
                    semantic[2]='20'+word
                else:
                    return give_text("El año debe ser mayot a 1970 y menor a 2017")


    if ("convertido" in message)and  ("gas" in message):
        if "no" in message:
            semantic[3]=False
        else:
            semantic[3]=True
    #save semantic
    save_list(path,semantic)
    #find action to do depanding on semantic values
    if semantic[0]=='':#check for brand
        return give_card("Para comprar un seguro, puede empezar seleccionando entre una de éstas marcas",["ford","nissan","chevrolet"])
    if semantic[1]=='':#cheack for model
        return give_card("Ahora podría decirme sobre algun modelo que le interece, entre los que tengo están",diccs.marcas[semantic[0]][0:3])
    if semantic[2]=='':#check for year
        return give_card("¿Podría proporcionarme el año de su vehículo? o ¿está dentro de los siguiéntes casos?",['2016','2015','2014','2013','2012'])
    if semantic[3]=='':#check for gas converted
        return give_card("Perfecto, solo falta saber si su coche fue convertido a gas",["mi coche fue convertido a gas","no fue convertido a gas"])
    else:
        return give_final_offer(semantic)#Call when now everything about the car
if __name__ == '__main__':
    msg=raw_input("Dame un texto: ")
    print get_response(msg)
