from deslab import *

def current_state_op(G, Xs, Xns):
    """
    Return True if the current state opacity exists, otherwise return False.
    Xs represents the secret states, and Xns represents the non-secret states.
    """
    
    SigmaOb = list(G.Sigobs)
    
    G2 = observer(G, SigmaOb)
    draw(G2)
    
    all_states = G2.X
    
    
    for  states in all_states:
        secret_state = False
        nonsecret_state = False
        for x in states:
            if x in Xs:
                secret_state = True
            if x in Xns:
                nonsecret_state = True
        if secret_state and not nonsecret_state:
            #print("Opacidade de estado corrente não existe")
            return False
    #print("Opacidade de estado corrente existe")
    return True

def inverse_automaton(G):
    trans = transitions(G)
    for x1, t1, x2 in trans:
        G = G.deletetransition((x1, t1, x2))
        G = G.addtransition([x2,t1,x1])

    return G

def initial_state_opac(G, Xs, Xns):
    """
    Return True if the initial state opacity exists, otherwise return False.
    Xs represents the secret states, and Xns represents the non-secret states.
    """
    
    SigmaOb = list(G.Sigobs)
    
    if sorted(G.X) == sorted(G.X0):
        allow_states = list(G.X0)
        G1 = G.setpar(Xm = G.X)
        G2 = inverse_automaton(G)
        G3 = observer(G2, SigmaOb)
        draw(G,G1,G2,G3)
    else:
        if not any(x in list(G.X0) for x in Xs):
            print("The secret state is not part of the initial states.")
            return False
        else:
            allow_states = list(G.X0)
            G1 = G.setpar(X0 = G.X, Xm = G.X0)
            G2 = inverse_automaton(G1)
            G3 = observer(G2, SigmaOb)
            draw(G, G1, G2, G3)

    
    marked_states = G3.Xm
    for states in marked_states:
        secret_state = False
        nonsecret_state = False
        for x in states:
            if (x in Xs) and (x in allow_states):
                secret_state = True
            if (x in Xns) and (x in allow_states):
                nonsecret_state = True
        if secret_state and not nonsecret_state:
            #print("Opacidade de estado inicial não existe")
            return False
    #print("Opacidade de estado inicial existe")
    return True
    
def language_based_opac(G1, G2):
    """
    Return True if the language based opacity exists, otherwise return False.
    G1 represents the secret language, and G2 represents the non-secret language.
    """
    
    SigmaOb = list(G1.Sigobs)
    
    G1o = observer(G1, SigmaOb)
    G2o = observer(G2, SigmaOb)
    G3 = coac(product(G1o, G2o))
    G1oc = complement(G1o)
    G4 = coac(product(G3, G1oc))

    draw(G1, G2)
    draw(G1o,G2o)
    draw(G3, G1oc, G4)
    
    if G3.X != []:
        if langdiff(G4,G1o).X != []:
            #print("Opacidade de linguagem existe")
            return True
    else:
        #print("Opacidade de linguagem não existe")
        return False
    
def initial_final_state_opac(G, xsp, xnsp):
    m0 = []
    keys = []
    m_aux = []
    m_aux1 = []
    SigmaNob = []
    trans_nob = []
    remove_keys = []
    X0 = G.X0
    trans = list(G.transitions())
    contador = 0
    states = {}
    states_i = {}
    states_aux = {}

    SigmaOb = list(G.Sigobs)
    # construindo m0
    for i in X0:
        aux = (i,i)
        m0.append(aux)
    

    for begin, event, end in trans:
        if event not in SigmaOb:
            SigmaNob.append(event)
        if begin in X0 and event not in SigmaOb:
            aux = (begin, end)
            m0.append(aux)

    nome_lista = f'm_{contador}'
    states_i[nome_lista] = m0

    for begin, event, end in trans:
        if event in SigmaNob:
            aux = (begin, end)
            trans_nob.append(aux)

    count = 0
    # construindo outros m
    while len(states_i) != 0:
        count = count + 1
        keys = []
        remove_keys = []

        for i in states_i.keys():
            remove_keys.append(i)
            states[i] = states_i[i]
            
            for e in SigmaOb:
                m_aux = []
                m_aux1 = []
                m_existe = False

                # duplas a partir dos estados possiveis ocorrendo o evento observavel
                for state in states_i[i]:
                    for begin, event, end in trans:
                        if begin == state[1] and e == event:
                            aux = (state[0],end)
                            m_aux.append(aux)

                # duplas juntando os evento observaveis com os nao observaveis
                while len(m_aux) != 0:
                    m_aux2 = m_aux
                    m_aux = []
                    for dupla in m_aux2:
                        m_aux1.append(dupla)
                        for begin,end in trans_nob:
                            if dupla[1] == begin:
                                aux = (dupla[0],end)
                                m_aux.append(aux)

                # verifica se ja existe esse m               
                for nome_lista, lista in states.items():
                    if m_aux1 == lista:
                        m_existe = True
                
                # cria o m se nao existir
                if m_existe == False:
                    contador = contador+1
                    nome_lista = f'm_{contador}'
                    states_aux[nome_lista] = m_aux1

        for i in states_aux.keys():
            keys.append(i)
        
        for i in keys:
            states_i[i] = states_aux.pop(i)

        for key in remove_keys:
            del states_i[key]
     
    
    for i in states.keys():
        estado_s = False
        estado_ns = False

        for par in states[i]:
            if par in xsp:
                estado_s = True
            if par in xnsp:
                estado_ns = True

        if estado_s and not estado_ns:
            #print("Sistema nao possui opacidade de estado inicial-final")
            return False
    if not (estado_s and not estado_ns):
        #print("Sistema possui opacidade de estado inicial-final")
        return True
        
