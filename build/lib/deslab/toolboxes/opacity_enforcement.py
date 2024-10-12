from deslab import *

syms('q0 q1 q2 q3 q4 q5 a1 b1 c1 d1 e1 a b c d e f x y t1 t2')
#s = list(s) retirar frozenset
#deepcopy para salvar o estado original e poder alterar o automato
#lexgraph alphamap(G1) pra chregar
#olhar variaveis
#os estados em Y ou Z tem que ser ajustados, olhar o final do que tem no artigo

def auto1():

    table = [(a1,'a_1'),(b1,'b_1'),(e1,'e_1'),(q1,'q_1'),(q2,'q_2'),(q3,'q_3'),(q0,'q_0')]
    X = [q0,q1,q2,q3, q4, q5]
    Sigma = [a1,b1,e1]
    X0 = [q0]
    Xm = [q5]
    T =[(q0,a1,q1),(q0,e1,q2),(q1,b1,q3),(q3,a1,q3),(q2,b1,q4), (q4,a1,q3)]
    G = fsa(X,Sigma,T,X0,Xm,table,name='$G_1$')
    
    return G

def auto2():

    table = [(a,'a'),(b,'b'),(c,'c'),(d,'d'),(e,'e'),(q1,'q_1'),(q4,'q_4'),(q5,'q_5'),(q2,'q_2'),(q3,'q_3'),(q0,'q_0')]
    X = [q0,q1,q2,q3,q4,q5]
    Sigma = [a,b,c,d]
    Sigmao = [a,b,c,d]
    X0 = [q0]
    Xm = []
    T =[(q0,d,q1),(q0,a,q4),(q0,b,q5),(q1,a,q2),(q2,b,q3),(q3,c,q0),(q4,b,q5),(q5,c,q0)]
    G = fsa(X,Sigma,T,X0,Xm,table,Sigobs=Sigmao, name='$G_2$')
    
    return G

def estimator():

    table = [(a,'a'),(b,'b'),(c,'c'),(d,'d'),(e,'e'),(q1,'q_1'),(q4,'q_4'),(q5,'q_5'),(q2,'q_2'),(q3,'q_3'),(q0,'q_0')]
    X = [q0,q1,q2,q3,q4,q5]
    Sigma = [a,b,c,d,e]
    X0 = [q0]
    Xm = []
    T =[(q0,d,q1),(q0,a,q4),(q0,b,q5),(q1,a,q2),(q2,b,q3),(q3,c,q0),(q4,b,q5),(q5,c,q0)]
    G = fsa(X,Sigma,T,X0,Xm,table,name='$G_2$')
    
    return G

def estimator_old():

    table = [(a,'a'),(b,'b'),(c,'c'),(d,'d'),(e,'e'),(q1,'q_1'),(q4,'q_4'),(q5,'q_5'),(q6,'q_6'),(q7,'q_7'),(q8,'q_8'),(q2,'q_2'),(q3,'q_3'),(q0,'q_0')]
    X = [q0,q1,q2,q3,q4,q5,q6,q7,q8]
    Sigma = [a,b,c,d,e]
    X0 = [q0]
    Xm = []
    T =[(q0,e,q0),(q0,d,q1),(q0,a,q5),(q0,b,q8),(q1,a,q2),(q2,b,q3),(q3,c,q4), (q5,b,q6),(q6,c,q7)]
    G = fsa(X,Sigma,T,[q0,q0],Xm,table,name='$G_2$')
    
    return G

###########################################################
def verifier_estimator(G, Xs):
    events = G.Sigma
    G = G.addevent('new_event')
    G = G.setpar(Sigobs=events)
    e = observer(G, G.Sigobs)

    #montando E_d
    e_d = e
    all_states = e.X
    for  states in all_states:
        secret_state = False
        nonsecret_state = False
        for x in states:
            if x in Xs:
                secret_state = True
            else:
                nonsecret_state = True
        if secret_state and not nonsecret_state:
            e_d = e_d.deletestate(states)
    e_d = ac(e_d)

    #montando E_f
    trans = e.transitions()
    e_f = e

    for x1,ev,x2 in trans:  
        if (x1 != x2) and (ev in G.Sigobs):
            e_f = e_f.addtransition([x1,f,x2])
    for i in e_f.Sigma:
        evi = i + "i"
        e_f = e_f.addevent(evi)
    for states in all_states:
        s_events = []
        for x1,ev,x2 in trans:  
            if states == x1 and x1 == x2:
                s_events.append(ev)
        for ev in e.Sigma:
            if ev not in s_events:
                evi = ev + "i"
                e_f = e_f.addtransition([states,evi,states])

    return (e,e_d,e_f)

###########################################################
def verifier_parallel_composition(e,e_d, e_f):
    
    new_states = []
    all_states = []
    initial_state = []
    v_fvo = []
    v_fvi = []
    v_fve = []

    x01 = next(iter(e_d.X0))
    x02 = next(iter(e_f.X0))
    
    trans1 = e_d.transitions()
    trans2 = e_f.transitions()

    aux = (list(x01)[0],list(x02)[0])
    new_states.append(aux)
    initial_state.append(aux)
    new_xv = []
    while len(new_states) != 0:
        
        

        #isso pode dar errado por causa do frozenset
        for state in new_states:
            state_d = state[0]
            state_f = state[1]
            all_states.append(state)
            
            for i in e_d.Sigma:
                #transicao em e_d
                trans_d = [group for group in trans1 if state_d in group[0] and group[1] == i]

                #transicao normal
                trans_fo = [group for group in trans2 if state_f in group[0] and group[1] == i] 
                #transicao self loop criado
                trans_fi = [group for group in trans2 if state_f in group[0] and group[1] == i+"i"]
                
                #transicao epsilon - pega a mesma info varias vezes mas ta mais bonito deixar aqui
                trans_fe = [group for group in trans2 if state_f in group[0] and group[1] == "f"]
                
                
                if trans_d != [] and trans_fo != []:
                    x1 = (state_d,state_f)
                    x2 = (next(iter(trans_d[0][2])),next(iter(trans_fo[0][2])))
                    v_fvo.append([x1,i,x2])
                    new_xv.append(x2)
                if trans_d != [] and trans_fi != []:
                    x1 = (state_d,state_f)
                    x2 = (next(iter(trans_d[0][2])),state_f)
                    v_fvi.append([x1,i,x2])
                    new_xv.append(x2)
                if trans_fe != []:
                    x1 = (state_d,state_f)
                    x2 = (state_d,next(iter(trans_fe[0][2])))
                    v_fve.append([x1,i,x2])
                    new_xv.append(x2)
        
        aux1 = set()
        new_xv_aux = []
        for sublist in new_xv:
            if sublist not in new_xv_aux:
                new_xv_aux.append(sublist)

        new = []
        new_xv_aux = new_xv_aux
        for item in new_xv_aux:
            if item not in all_states:
                new.append(item)

        new_states = []
        new_states = new


    T = []


    for sublist in v_fvo:
        T.append(sublist)
    for sublist in v_fvi:
        T.append(sublist)
    for sublist in v_fve:
        T.append(sublist)

    v = fsa(all_states,list(e.Sigma),T,initial_state,[],name='$V$')
    #draw(v)
    return (v,v_fvo,v_fvi,v_fve)


##########################################################################
def unfolded_verifier(v,fvo,fvi,fve):
    if True:
        y = []
        z = []
        final_y = []
        final_z = []
        f_zy = []
        f_yz = []
        vu_sigma = []
        states_v = v.X
        sigma_v = v.Sigma
        
        y0 = v.X0
        y = y0
    
    while y != []:
        for state_y in y:
            
            for i in sigma_v:    
                
                v_fvo_e = [group for group in fvo if group[0] == state_y and group[1] == i]
                v_fve_e = [group for group in fve if group[0] == state_y and group[1] == i]
                
                if v_fvo_e != []:
                    f_yz.append([state_y,i,(state_y,i)])
                    if (state_y,i)not in z:
                        z = z + [(state_y,i)] 
                elif v_fve_e != []:
                    f_yz.append([state_y,i,(state_y,i)])
                    if (state_y,i)not in z:
                        z = z + [(state_y,i)]

        final_y += y
        y = []
        v_aux = fsa()
        auto_vazio = True
        trans = {}
        #state_z[0] eh o estado e state_z[1] o evento
        if True:
            for state_z in z:
                xv_aux = []
                vz = v
                vz = vz.setpar(X0 = state_z[0])
                vz_ac = ac(vz)
                t_vz = vz_ac.transitions() #acho que pode dar problema                
                aux2 = []
                for x1,ev,x2 in t_vz:
                    #print("x1",x1)
                    if ev == state_z[1]:      
                        for group in fvo:
                            if group[0] == x1 and group[1] == ev and group[2] == x2:
                                xv_aux.append([group[0],group[2]])

                #problema eh aqui
                for state,final in xv_aux:
                    if True: #state_z[0] != state:
                        v_aux = fsa(list(states_v),list(sigma_v),fvi,state_z[0],[state])
                        v_aux = coac(v_aux)
                        auto_vazio = v_aux.empty
                        xv_linha1 = state
                        #final_linha = final
                        if not auto_vazio:
                            trans = lexgraph_alphamap(v_aux)
                            aux2.append([state,final,trans])
                    
                if xv_aux != [] and aux2 != []:
                    for xv_linha,final_linha,trans in aux2:
                        #trans = lexgraph_alphamap(v_aux)
                        xv_way = trans[xv_linha]
                        vu_sigma.append(xv_way)
                        f_zy.append([state_z,xv_way,final_linha])
                        if final_linha not in final_y:
                            y.append(final_linha)
                

                for group in fve:
                    if group[0] == state_z[0] and group[2] == xv_linha1:
                        if xv_linha not in final_y:
                            vu_sigma.append('f')
                            f_zy.append([state_z,'f',xv_linha1])
                            y.append(xv_linha)
                
        #print("olhar aqui Y\n", y)
        #print("f_zy\n",f_zy)

        final_z += z
        z = []

    #print(vu_sigma)
    #print("Y\n", final_y + final_z)
    #print("Z\n", final_z)
    #print("F_zy \n", f_zy+f_yz)
    #print("F_yz\n",f_yz)

    return final_y,final_z,f_zy,f_yz, list(set(vu_sigma))
    
    
#####################################################
def all_edit_structure_c(vu,y,z,f_zy,f_yz, edit_const):
    vum = vu.setpar(Xm = y)
    for state in edit_const:
        vum = vum.deletestate(state)
    vum = trim(vum)
    
    aes_c = supCont(vum,vu)

##################
#Faz o que eh descrito no 
# artigo de outra forma
def all_edit_structure_c_teste(vu, edit_const):
    
    trans_old = []
    vum = vu
    for state in edit_const:
        vum = vum.deletestate(state)
    
    vum = ac(vum)
    
    all_states = vum.X
    trans_new = vum.transitions()
    state_active = []
    
    for x1,ev,x2 in trans_new:
        if x1 not in state_active:
            state_active.append(x1)
    
    while trans_old != trans_new:
        trans_old = trans_new
        
        for state in all_states:
            if state not in state_active:
                vum = vum.deletestate(state)

        vum = ac(vum)
        
        all_states = vum.X
        trans_new = vum.transitions()
        state_active = []
        for x1,ev,x2 in trans_new:
            if x1 not in state_active:
                state_active.append(x1)
        
    return vum

###############################
def string_run_and_projection(aes_c,y):
    all_states = aes_c.X
    y0 = list(aes_c.X0)
    
    aes_t = aes_c
    
    for state in all_states:
        state_real = False
        for s in y:
            if state == s:
                state_real = True
        if not state_real:
            aes_t = aes_t.deletestate(state)
        
    aes_t = ac(aes_t)
    
    trans = aes_t.transitions()
    
    current_state = y0[0]   
    s_run = []
    s_run_p = []
    while trans != []:
        
        for t in trans:
            if t[0] == current_state:
                initial_state = t[0]
                e_aux = t[1]
                current_state = t[2]
                x = t
                break
        
        trans.remove(x)
        for t in trans:
            if t[0] == current_state:
                gamma_aux = t[1]
                current_state = t[2]
                x = t
                break
        
        trans.remove(x)
        
        
        if gamma_aux != 'epsilon':
            s_run.append([initial_state,(gamma_aux+e_aux),current_state])
            s_run_p.append([initial_state,(e_aux),current_state])
        else:
            s_run.append([initial_state,(e_aux),current_state])
            s_run_p.append([initial_state,(e_aux),current_state])
            
    #print("s_run ", s_run)
    #print("s_run_p ", s_run_p)
    
    final_transition = []
    for t in s_run:
        for p in s_run_p:
            if t[0]==p[0] and t[2]==p[2]:
                final_transition.append((t[0],(t[1],p[1]),(t[2],(t[1],p[1]))))
    
    ordem = 0
    current_state = y0[0]
    trans_ordenadas = []
    while final_transition != []:
        if trans_ordenadas == []:
            for t in final_transition:
                if t[0] == current_state:
                    trans_ordenadas.append(t)
                    x = t
                    current_state = t[2]
                    break
        else:
            for t in final_transition:
                if t[0] == current_state[0]:
                    new_t2 = (t[2][0],(current_state[1][0]+t[2][1][0],current_state[1][1]+t[2][1][1]))
                    trans_ordenadas.append([t[0],t[1],new_t2])
                    
                    x = t
                    current_state = new_t2
                    break
        final_transition.remove(x)
    
    return trans_ordenadas
    
    
###################################################
def all_edit_structure_t(aes_c):
    if True:
        y0 = list(aes_c.X0)
        trans = aes_c.transitions()
        way_dic = {y0[0] : [y0[0]]}#rever isso se tiver mais de um estado inicial
        aux_dic = {}
        way_end = {}
    
    while way_dic != {}:
        
        if True:
            del_key = []
            aux_dic = {}
            trans_def = False
        for key, state in way_dic.items():
            for x in trans:
                if key == x[0]:
                    aux_dic[x[2]] = state +  [x[0]]
                    trans_def = True
                    #states_z.append(x[2])
            if not trans_def:
                way_end[len(way_end)+1] = state +  [key]
            del_key.append(key)
        
        for key in del_key:
            way_dic.pop(key)
         
        del_key = []
        for key, state in aux_dic.items():
            for x in trans:
                if key == x[0]:
                    way_dic[x[2]] = state +  [x[0]]
            del_key.append(key)
        
        for key in del_key:
            aux_dic.pop(key)
        
        del_key = []
        for key, state in way_dic.items():
            if key in state:
                way_end[len(way_end)+1] = state +  [key]
                del_key.append(key)
        
        for key in del_key:
            way_dic.pop(key)
    
    for key, state in way_end.items():
        state.pop(0)
        way_end[key] = state
    
    new_y = []
    for key,state in way_end.items():
        new_y.append(string_run_and_projection(aes_c,state))
    
    #print("new_y", new_y)
    fw_dic = {}
    n_way = 0
    if len(new_y)>1:        
        for way in new_y:
            fw_dic[n_way] = []
            hold = False
            for item in way:
                if not hold:
                    initial = item[0]
                final = item[2]
                trans = item[1][1]
                trans2 = item[1][0]
                trans2 = trans2.replace(trans,'')
                if trans2 == '':
                    trans2 = 'epsilon'
                if not hold:
                    aux = [initial,trans,(initial,trans)]
                else:
                    aux = [initial,trans,(initial[0],trans)]
                #print("aux  1 ",aux)
                fw_dic[n_way] = fw_dic[n_way] + [aux]
                
                
                if not hold:
                    aux = [(initial,trans),trans2,final]
                else:
                    aux = [(initial[0],trans),trans2,final]
                #print("aux  2 ",aux)
                fw_dic[n_way] = fw_dic[n_way] + [aux]
                
                initial = item[2]
                hold = True

            n_way += 1
    else:
        fw_dic[0]=[]
        for item in new_y:
            initial = item[0]
            final = item[2]
            trans = item[1][1]
            trans2 = item[1][0]
            trans2 = trans2.replace(trans,'')
            
            aux = [initial,trans,(initial,trans)]
            fw_dic[0] = fw_dic[0] + [aux]
            aux = [(initial,trans),trans2,final]
            fw_dic[0] = fw_dic[0] + [aux]
    
    return fw_dic #fazer o automato tbm
     

def verifier_edit_function(runs,xs, x0):
    secret_run = False
    cj = []
    ck = []
    cj_final = []
    ck_final = []
    leaf = []
    map_runs = []
    used_leaf = []
    aux = []
    aux_run = []
    
    for num in runs:
        run = runs[num]
        secret_run = False
        for state in run:
            if state[0][0][1] in xs:
                secret_run = True
    
        if secret_run:
            aux = 0
            for state in run:
                if state[0][0][1] in xs:
                    if aux:
                        ck.append(aux[0][0])
                else:
                    aux = state
            cj.append(run[-1][-1])
        else:
            ck.append(run[-1][-1])
        
    for j in range(len(cj)):
        for k in range(len(ck)):
            if len(cj[j][1][0])<=len(ck[k][1][0]):
                ck_aux = ck[k][1][0][-len(cj[j][1][0]):]
                if ck_aux == cj[j][1][0]:
                    cj_final.append(cj[j])
                    ck_final.append(ck[k])
            
    #remove duplicates cj_final e ck_final
    cj_final = list(set(cj_final))
    ck_final = list(set(ck_final))
    
    leaf = cj_final + ck_final
    
    if leaf:
        for state in leaf:
            for num in runs:
                run = runs[num]
                if run[-1][-1]==state:
                    map_runs.append(run)
                    used_leaf.append(state)
    else:
        print("No edit function")
        return fsa()
                    
    for state in used_leaf:
        leaf.remove(state)
    
    if leaf:
        for state in leaf:
            for num in runs:
                aux = []
                run = runs[num]
                for i in run:
                    if state==i[2]:
                        map_runs.append(run)
                        
                    else:
                        aux.append(run)
                        
    
    state = []
    trans = []
    table = []
    # Percorre a tabela e extrai estados e transições
    for sublista in map_runs:
        table += sublista
        for tupla in sublista:
            state.append(tupla[0])
            trans.append(tupla[1])
            state.append(tupla[2])

    # Remove duplicatas nas listas
    state = list(set(state))
    transicoes = list(set(trans))

    #montar automato
    edit_function_auto = fsa(state,transicoes, table, x0)
    edit_function_auto.setgraphic(style = 'rectangle')
    
    return edit_function_auto


def edit_function(G,xs, constrantes = []):
    """
    This function receives a automaton G
    """

    
    e,ed,ef = verifier_estimator(G, xs)

    v,fvo,fvi,fve = verifier_parallel_composition(e,ed,ef)

    #a = Y, b = Z
    a,b,c,d,e = unfolded_verifier(v,fvo,fvi,fve)

    vu = fsa(a+b,list(v.Sigma)+e,c+d,list(v.X0),[],name='$Vu$')
    #vu.setgraphic(style = 'rectangle')

    aes_c = all_edit_structure_c_teste(vu,constrantes)
    runs= all_edit_structure_t(aes_c)
    pp_enforce = verifier_edit_function(runs,xs,v.X0)     
    
    return pp_enforce
    
"""
g1 = estimator()
secreto = [q5]
pp = edit_function(g1,secreto)
  
"""


        

             
                
  