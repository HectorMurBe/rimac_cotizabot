def response(request):
    path=os.path.realpath("string_cache/algo.pkl")
    import re
    save=False
    if request.method == 'GET':
        message = request.GET.get('message')
        message=message.lower().replace("?","")
        message=message.lower()
        bot_ans=interaction.get_bot_subs(message,"chepix")
        #hardcode for tipe
        tarjetita=False
        m = re.search('(?<=md )\w+',bot_ans)#modelos
        m2 = re.search('(?<=mr )\w+',bot_ans)#marcas
        mb=None
        mr=None
        save=False
        if m!= None:
            mb=[m.group(0)]
            tarjetita=True
            save=True

            if m2 == None:
                mr=modelos[mb[0]][0]
        else:
            mb="bla"
        #hardcore for brand
        if m2!= None:
            mr=m2.group(0)
            tarjetita=True
            if m==None:
                lista_coches=marcas[mr]
                random.shuffle(lista_coches)
                mb=lista_coches[0:3]
        elif mr==None:
            mr="bla"
        #hardcore for year
        year="2015"
        for word in bot_ans.split(" "):
            if word.isdigit() and len(word)==4:
                tarjetita=True
                year=word

        cars=[]
        for i in mb:
            car={}
            car["year"]=year
            car["brand"]=mr
            car["model"]=i
            cars.append(car)
        path=os.path.realpath("bot/string_cache/algo2.pkl")
        tal_vez=open_list(path)
        if len(tal_vez)==2 and save==False:
                            year=get_date(message)
                            car={}
                            car["year"]=year
                            car["brand"]=tal_vez[1]
                            car["model"]=tal_vez[0][0]
                            respuesta["cars"]=[car]
                            respuesta["texto"]="Perfecto, te ofrezco un seguro para el coche"
                            respuesta["founded"]=True
        if save==True:
            print "holi"
            save_list([mb,mr],path)
            respuesta={
                        "texto":" Perfecto, solo necesito saber la fecha de salida al mercado del coche "+mb[0]+" "+mr+"?",
                        "founded":"false",
                        "cars":"--",
                            }
        else:
            save_list([],path)
