import random

sec_b_private_key = 36468281916720476773305072821816660957628314190540061902217404836373991523555

res_private_keys = [36468281916720476773692348642624046797595102259880790744179775916646337698103,36468281916720476773942831382225837488846225981320455941513535681271665349679]

dev_private_keys = [36468281916720476773848689837010266471444119586619256906188947833778973366388,36468281916720476773028637179747554607970777771135139711273988301458270714646,36468281916720476773479401918454020971282631820454190373405297243728334964334]

def create_pk():
    global sec_b_private_key
    sec_half = str(sec_b_private_key)
    sec_half = sec_half[:20]
    new_pk = str(random.getrandbits(256))
    new_pk = new_pk.replace(new_pk[:20],sec_half)
    new_pk = _verfy_private_key(new_pk)
    return int(new_pk)

def create_res_pk():
    pk = create_pk()
    res_private_keys.append(pk)

def create_dec_pk():
    pk = create_pk()
    dev_private_keys.append(pk)

def _verfy_private_key(p_K):
    #private key must be 77 char
    temp_pk = str(p_K)
    count = len(temp_pk)
    if count < 77 :
        diff = 77 - count
        for x in range(diff):
            temp_pk = temp_pk+str(random.randint(0,9))

    elif count > 77 :
        diff = count - 77
        for x in range(diff):
            temp_pk = temp_pk.replace(temp_pk[-1],'')


    return temp_pk
