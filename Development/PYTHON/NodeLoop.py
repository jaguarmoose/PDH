import adnod
I,J,K = 0,0,0
while I < 5:
    I=I+1
    NS="1:"+str(I)
    adnod.adnod(NS)
    print(NS)
    while J < 4:
        J=J+1
        NS="1:"+str(I)+":"+str(J)
        print(NS)
        adnod.adnod(NS)
        while K < 29:
            K=K+1
            NS="1:"+str(I)+":"+str(J)+":"+str(K)
            print(NS)
            adnod.adnod(NS)
        K=0
    J=0   
