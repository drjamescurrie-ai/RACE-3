#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math

import time

def complexityBreak(w): 

# Let the set of factors of w of length n be c[n]. If for some 
# 0<i<depth+1 we have |c[i]|>2i+1, return c[i] for the least such
# i. Otherwise return 0.
    
    depth=20
    for i in range(1,depth+1):
        c=[]
        for j in range(len(w)-i+1):
            if not(w[j:j+i]in c):
                c.append(w[j:j+i])
        if (len(c)>2*i+1):
            c.sort()
            return(c) # 
    return(0)

def goodMorphism(L):
# Does L=[a,b,c] satisfy the conditions of the Morphism Lemma?

    def prefix(a,b):
    
    # Does word b have prefix a?
        if (len(b)<len(a)):
            return(False)
        else:
            return(b[:len(a)]==a)

    def goodsuff(a,c):
    
    # Do c and a have a common suffix of length |a|/2?

        for i in range(math.ceil(len(a)/2),len(a)+1):
            if (a[-i:]==c[-i:]):
                return(True)
        return(False)    
    
    a=L[0]
    b=L[1]
    c=L[2]
    return(prefix(a,b)and prefix(b,c)and goodsuff(a,c) 
           and (2*len(a)>=len(c)))

def dualMorphism(L):
    
# Does L=[a,b,c] satisfy the conditions of the Dual Morphism Lemma?
    
    A=L[0][::-1]
    B=L[1][::-1]
    C=L[2][::-1]
    L=[A,B,C]
    return(goodMorphism(L))

def morph(L): 
    
# Returns a conjugate of morphism L which satisfies the Morphism Lemma
# or the Dual Morphism Lemma. If no such conjugate exists, returns 0.

    def morphism_conjugates(L): 
    
    # Given a morphism L (a list of length 3) such that L[0]<=L[1]<=L[2],
    # returns a list of the conjugates of L. 

        conjugates=[]
        conjugates.append(L)
        M=L
    # To begin, M is a copy of L. We iteratively conjugate by (prefix) 
    # letters
        i=0
        while(i<len(L[0])):
            if ((M[0][0]==M[1][0])and(M[1][0]==M[2][0])):
                # M = [xa,xb,xc], so B=[ax,bx,cx] is a conjugate.
                B=[]
                for j in range(3):
                    B.append(M[j][1:]+M[j][0])
                M=B    
                conjugates.append(B)
            i=i+1
    # Again, M is a copy of L. We iteratively conjugate by (suffix) 
    # letters
        M=L
        i=1
        while(i<len(L[0])):
            if ((M[0][-1]==M[1][-1])and(M[1][-1]==M[2][-1])):
                # M = [ax,bx,cx], so B=[xa,xb,xc] is a conjugate.
                B=[]
                for j in range(3):
                    B.append(M[j][-1]+M[j][:-1])
                M=B    
                conjugates.append(B)
            i=i+1
        return(conjugates)

    C=morphism_conjugates(L)
    for M in C:
        if goodMorphism(M):
            N=[M[1],M[0],M[2]]
            return([1,N])
        if dualMorphism(M):
            N=[M[1],M[0],M[2]]
            return([2,N])
    return([0,[]])

def fhpf(w): # Word w has no suffix of exponent 5/2 or greater
    p=1 #potential period of suffix of exponent 5/2 or greater
    while (5*p<=2*len(w)):
        if (w[-3*p//2:]==w[-5*p//2:-p]):
            return(False)
        p=p+1
    return(True)

def test(w,forbidden_factors): 
    
# This returns true if no suffix of w is in forbidden_factors or has
# exponent at least 5/2

    for f in forbidden_factors:
        if (len(w)>=len(f)):
            if (w[-len(f):]==f):
                return(False)
    return(fhpf(w))

def backtrack(target,forbidden_factors):

# Call a ternary word _low if it contains no factor having exponent 
# 5/2 or greater. This routine returns a low word w starting 
# with 0 of length target such that w contains no factor in F. If no 
# such word exists, it returns the length of the longest low word
# starting with 0 with no factor in forbidden_factors.
    
    largest_letter='2'
    w='0'
    mx=1 # Greatest length attained so far

    while(1==1):
        success=test(w,forbidden_factors)
        if (success):
            if (len(w)>mx):
                mx=len(w)
            if (len(w)==target):
                return(w)
            else:
                w=w+'0'
        else:
            while((len(w)>1) and w[-1]==largest_letter):
                w=w[:-1]
            if (len(w)==1):
#               Search fails. Longest word has length mx.
                return(mx)
            else:
                w=w[:-1]+chr(ord(w[-1])+1)
    

def good(w,forbidden_factors):
    
# Call a word _good if it is low and has no factor in 
# forbidden_factors.

    for i in range(1,len(w)+1):
        if not(test((w[:i]),forbidden_factors)):
            return(False)
    return(True)

def doubler(n,forbidden_factors):
    
# This returns the set of all good words of length n. It produces
# the words recursively, testing concatenations of good words of 
# lengths ceil(n/2) and floor(n/2). 
    
    if (n==0):
        return([''])
    if (n==1):
        return(['0','1','2'])
    G=[]
    for s in doubler(math.ceil(n/2),forbidden_factors):
        for t in doubler(n//2,forbidden_factors):
            u=s+t
            if good(s+t,forbidden_factors):
                G.append(s+t)
    return(G)


def blocks(b,depth,forbidden_factors): 
    
# Finds certain b-blocks: words bu such that bub is 
# good, |u|<=depth, and there are exactly two instances of b in bub, 
# namely as prefix and suffix.

    myBlocks=[]
    for i in range(depth+1):
        forbidden_factors.append(b) # We seek good words u not 
                                    # containing b
        U=doubler(i,forbidden_factors)
        forbidden_factors.pop()
        for u in U:        
            if good(b+u+b,forbidden_factors):
                if ((b+u+b)[1:].find(b)==(len(b)+len(u)-1)):
                    myBlocks.append(b+u)
    return(myBlocks)

def factors(w,n):
    
# Returns the set of factors of w of length n    
    
    f=[]
    for j in range(len(w)-n+1):
        if not(w[j:j+n] in f):
            f.append(w[j:j+n])
    f.sort()
    return(f)

Morphisms=[]
Dual_Morphisms=[]
longest_b=1

def findMorph(w,k,forbidden_factors):
    
# Given word w and set of excluded words forbidden_factors, we 
# consider factors b # of w of length up to k. Suppose that every 
# good word of length v+1 contains b. We find the b-blocks bu.
# If there are exactly b-blocks (or four b-blocks 
# of which the first can only occur once) then any good word has 
# a final segment concatenated from the three b-blocks. We 
# form a morphism from these b-blocks. We then test whether 
# one of its conjugates satisfies the Morphism Lemma or the Dual 
# Morphism Lemma, 

    global Morphisms
    global Dual_Morphisms
    global longest_b
    indent='    '
    n=1
    while(n<=k):
        Fact=doubler(n,forbidden_factors)
        for b in Fact:
            forbidden_factors.append(b)
            depth=backtrack(200,forbidden_factors)
            forbidden_factors.pop()
            if(isinstance(depth,int)): 
                # Longest good word not containing b has length 
                # depth              
                Blocks=blocks(b,depth,forbidden_factors)
                if(len(Blocks)>=3):
                    if(len(Blocks)<=4):
                            myMorph=[	Blocks[-3],	Blocks[-2],	Blocks[-1]]
                            N=morph(myMorph)
                            if(N[0]==1): 
                            # This conjugate of myMorph satisfies 
                            # the Morphism Lemma. We check that 
                            # 	Blocks[0] cannot appear twice
                            # in a good concatenation of the return 
                            # words
                                check=True
                                for p in Blocks:
                                    for s in Blocks:
                                        if (good(p+	Blocks[0]+s,
                                                 forbidden_factors)):
                                            check=False
                                if (check):
                                    print(indent+'The ',b,'-blocks are:')
                                    print()

                                    print(Blocks,'.')
                                    print()

                                    print(indent+'Word ',	Blocks[0],
                                    'cannot occur twice in a '+
                                    'concatenation of these.')
                                    print()

                                    print(indent+'Thus a final '+
                                    'segment of w is concatenated '+
                                    'from:')
                                    print()

                                    print(myMorph)
                                    print()

                                    print(indent+'Taking conjugates,'+
                                    ' a final segment is the image '+
                                    'under morphism')
                                    print()

                                    print(N[1],'.')
                                    print()

                                    if (not(N[1]in Morphisms)):
                                        Morphisms.append(N[1])
                                    print(indent+'which satisfies'+
                                    ' the Morphism Lemma.')
                                    print()

                                    return()
                            if(N[0]==2): # This conjugate of myMorph 
                                         # satisfies the Dual Morphism Lemma
                                check=True
                                for p in Blocks:
                                    for s in Blocks:
                                        if (good(p+	Blocks[0]+s,
                                                 forbidden_factors)):
                                            check=False
                                if (check):
                                    print(indent+b,'-blocks are among ',
                                    Blocks,'.')
                                    print()

                                    print(indent+'Word ',	Blocks[0], 
                                    'cannot occur twice in a '+
                                    'concatenation of these.')
                                    print()

                                    print(indent+'Thus a final ' 
                                    +'segment of w is '+
                                    ' concatenated from ',myMorph,'.')
                                    print()

                                    print(indent+'Taking conjugates,'+
                                    ' a final segment is the image '+
                                    'under morphism')
                                    print()

                                    
                                    print(N[1],'.')
                                    print()

                                    if (not(N[1]in Dual_Morphisms)):
                                        Dual_Morphisms.append(N[1])
                                    print(indent+'which satisfies'+
                                    ' the Dual Morphism '+
                                    'Lemma.')
                                    print()

                                    return()
        n=n+1
        longest_b=max(longest_b,n)
    print(indent+'No morphism found up to length ', k,'.')
    print()

    return()
            
def resolveCase(forbidden_factors,caseString):

    global resolved_cases
    global resolved_case_labels
    
    k=3 # Maximum length of b considered in b-blocks bu

    if (caseString==''):
        print('We assume F includes ',forbidden_factors,'.')
        print()


    w=backtrack(250,forbidden_factors)
    if (isinstance(w,int)):
        print('No good word longer than ',w,' avoids these factors.')
        print()

        F=[]
        for f in forbidden_factors:
            F.append(f)
        resolved_cases.append(F)
        resolved_case_labels.append(caseString)
        print(resolved_cases)
        print(resolved_case_labels)
        return()
    
#   The case being resolved is labelled by forbidden_factors. 
#   However, we may find that additional factors are also necessarily
#   avoided in this case. We will sharpen our further backtracking 
# searches within this case by avoiding these additional factors.
#
#   To put it another way, when there is exactly one unneeded factor,
#   we would get one new subcase. Since there is no branching, it is
#   more intuitive to simply say the subcase is the "same" case, but 
#   we specify additional avoided factors in factorsToAvoid. The "base
#   case" is still labelled by the set forbidden_factors
    factorsToAvoid=[]
    for f in forbidden_factors:
        factorsToAvoid.append(f)
        
    unneeded_factors=[]

    while(len(unneeded_factors)<2):
        w=backtrack(250,factorsToAvoid)
        N=complexityBreak(w)
        if (N==0): #complexity is good
            M=findMorph(w,k,factorsToAvoid)
            F=[]
            for f in forbidden_factors:
                F.append(f)
            resolved_cases.append(F)
            resolved_case_labels.append(caseString)
            return()
        else:

            Mx=0
            needed_factors=[]
            unneeded_factors=[]
            for s in N:
                factorsToAvoid.append(s)
                w=backtrack(250,factorsToAvoid)
                factorsToAvoid.pop()
                if (isinstance(w,int)):
                    Mx=max(Mx,w)
                    needed_factors.append(s)
                else:
                    unneeded_factors.append(s)

            if(len(needed_factors)>0):
                print('Every good word longer than ',Mx, 
                'must include factor(s)')
                print()
                print(needed_factors,'.')
                print()

                if(len(needed_factors)>2*len(N[0])+1):
                    print('Word w has ',len(needed_factors),
                    '> 2 x',len(N[0]),'+ 1 factors of length ',
                    len(N[0]) ,'. This is impossible.')
                    print()

                    F=[]
                    for f in forbidden_factors:
                        F.append(f)
                    resolved_cases.append(F)
                    resolved_case_labels.append(caseString)
                    return()
            if (len(unneeded_factors)==1):
                print('In this case w must omit factor ',
                unneeded_factors[0],'.')
                print()
                s=unneeded_factors[0]
                factorsToAvoid.append(s)
    unneeded_factors.sort()
    j=0
    print('Word w must omit a factor from')
    print()
    print(unneeded_factors,'.')
    print()
    print('This gives rise to ',len(unneeded_factors),
    ' cases:')
    for s in unneeded_factors:
        if (caseString==''):
            subcase=chr(ord('1')+j)
        else:
            subcase=caseString+'.'+chr(j+49)
        j=j+1
        factorsToAvoid.append(s)
        print('Case '+subcase+': F includes ',factorsToAvoid)
        factorsToAvoid.pop()
    print()
    j=0

    
    

    for s in unneeded_factors:
        if (caseString==''):
            subcase=chr(ord('1')+j)
        else:
            subcase=caseString+'.'+chr(j+49)
        j=j+1
        factorsToAvoid.append(s)
        print('Case '+subcase+': F includes ',factorsToAvoid,'.')
        print()

        # Test whether case was resolved previously
        resolved=False
        for c in resolved_cases:
            resolved=True
            for d in c:
                if not(d in factorsToAvoid):
                    resolved=False
                    break
            if (resolved):
                i=resolved_cases.index(c)
                print('This was previously resolved in Case '+
                resolved_case_labels[i]+'.')
                print()

                print('(This concludes Case '+subcase+').')
                print()

                break
        if(not(resolved)):
            resolveCase(factorsToAvoid,subcase)
            print('(This concludes Case '+subcase+').')
            print()
            factorsToAvoid.pop()
    F=[]        
    for f in forbidden_factors:
        F.append(f)
    resolved_cases.append(F)
    resolved_case_labels.append(caseString)
        
    return() 

print('Here is the resolution of S={22,11}:')
print(' ')
resolved_cases=[]
resolved_case_labels=[]
startTime=time.time()
resolveCase(['22','11'],'')
endTime=time.time()
print('Computation took ',(endTime-startTime),' seconds.')
print(' ')
print(' ')
print(' ')
print('Here is the resolution of S={01,12,20,00}:')
print(' ')
resolved_cases=[]
resolved_case_labels=[]
startTime=time.time()
resolveCase(['01','12','20','00'],'')
endTime=time.time()
print('Computation took ',(endTime-startTime),' seconds.')
print(' ')
print(' ')
print(' ')
print('Here are the morphisms satisfying the Morphism Lemma used '+
'in the case resolutions:')
print(' ')
for m in Morphisms:
    print(m)
print(' ')
print(' ')
print(' ')

print('Here are the morphisms satisfying the Dual Morphism Lemma '+
'used in the case resolutions:')
print(' ')
for m in Dual_Morphisms:
    print(m)
print(' ')
print(' ')
print(' ')


print('Here is the length of the longest word in the backtracks of'+
' Lemma 2:')
      
S=['1121', '1122', '1211', '1212', '1221', '2112',
'2121', '2122', '2211', '2212']
F=['10','20','00']
longest=0
for s in S:
        for t in S:
            if (s!=t):
                F.append(s)
                F.append(t)
                w=backtrack(500,F)
                longest=max(w,longest)
                F.pop()
                F.pop()
print(' ')
print(longest)
    


# In[ ]:





# In[ ]:




