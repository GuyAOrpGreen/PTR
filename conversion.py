# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 14:37:30 2018

@author: Guy
"""

def listOfUniqueAtomsLetters(listOfAtoms):
    stra=listOfAtoms
    atoms=[]
    for i in stra:
        for j in i:
            if j in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if j not in atoms:
                    atoms.append(j)
                else:
                    continue
            
    return atoms

def noOfUniqueAtomsLetters(listOfAtoms):
    stra=listOfAtoms
    counter=0
    atoms=[]
    for i in stra:
        for j in i:
            if j in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if j not in atoms:
                    atoms.append(j)
                    counter+=1
                else:
                    continue
            
    return counter


#Probably redundant. Can Just use index of letters or index+1
def convertLettersListToNo(listOfAtoms):
    letters=listOfAtoms
    numbers=[]
    counter=1
    for letter in letters:
        numbers.append(counter)
        counter+=1;
    return numbers

def distributeNegation(sentence):
    sen= sentence
    newsen=sen
    sen=sen.replace('--','')
    newsen=newsen.replace('--','')
    if (newsen.find('-(')==-1):
        return newsen
    else:
        ind=newsen.index('-(') +2
        counter=0
        counter1=0
        counter2=0
        if (newsen[ind:len(newsen)].find(")")<newsen[ind:len(newsen)].find("(")):
            for i in range(ind,len(newsen)):
                if (newsen[i+counter2]==')'):
                    break
                elif (newsen[i+counter2] =='|'):
                    newsen=newsen[:i+counter2]+'&'+newsen[i+counter2+1:]
                elif (newsen[i+counter2] == '&'):
                    newsen=newsen[:i+counter2]+'|'+newsen[i+counter2+1:]
                elif (newsen[i+counter2].isalpha()):
                    newsen=newsen[:i+counter2]+'-'+newsen[i+counter2:]
                    counter2+=1
            return newsen[:newsen.index('-(')] + distributeNegation(newsen[newsen.index('-(')+1:])
       
        for i in range(ind, len(newsen)):
            if (newsen[i+counter1]==")") and (counter==0):
                break
            elif (newsen[i+counter1]=='('):
                counter+=1
                #print(newsen[:i+counter1]+'-'+newsen[i+counter1:])
                newsen=newsen[:i+counter1]+'-'+newsen[i+counter1:]
                counter1+=1
            elif (newsen[i+counter1]==')'):
                counter-=1
            elif (newsen[i+counter1]=='|') and (counter==0):
                newsen=newsen[:i+counter1]+'&'+newsen[i+counter1+1:]
            elif (newsen[i+counter1]=='&') and (counter==0):
                newsen=newsen[:i+counter1]+'|'+newsen[i+counter1+1:]
        #print(newsen[:newsen.index('-(')])
        return newsen[:sen.index('-(')] + distributeNegation(newsen[newsen.index('-(')+1:])
 
def convertForSAT(KB):
    returnedKB=[]
    actualKB=KB
    check=False
    for sentence in actualKB:
        returnedSentence=[]
        for letter in sentence:
            if str.isdigit(letter):
                if check:
                    returnedSentence.append(-int(letter))
                    check=False
                else:
                    returnedSentence.append(int(letter))
            elif letter=="&":
                returnedKB.append(returnedSentence)
                returnedSentence=[]
            elif letter=="-":
                if (check):
                    check=False
                else:
                    check=True
        returnedKB.append(returnedSentence)
    return returnedKB

def convertLettersToNo(listOfLetters, listOfNumbers, KB):
    newKB=[]
    letters=listOfLetters
    numbers=listOfNumbers
    for sentence in KB:
        newSentence=sentence
        for letter in letters:
            newSentence=newSentence.replace(letter, str(numbers[letters.index(letter)]))
        newKB.append(newSentence)
    return newKB

def convertAnd(Sentence):
    return False



def convertCNFBetter(Sentence):
    sen=Sentence
    if "(" in sen:
        if ">" in sen:
            newsen=sen
            bracketPair=bracketPairs(sen)
            bracketPair=bracketPair[::-1]
            counter=0
            check=True
            
            for i in range(len(bracketPair)-1):                
                if (check):
                    ind1=bracketPair[i][0]
                    ind2=bracketPair[i+1][0]
                    if (i%2==0):
                        if (newsen[ind1-1]=='>'):
                            newsen=newsen[:ind2]+'-'+newsen[ind2:]
                            newsen=newsen[:ind1]+'|'+newsen[ind1+1:]
                            counter+=ind2
                            check=False
                    
                else:
                    for badcode in bracketPair:
                        for k in range(len(badcode)):
                            if (badcode[k]>counter):
                                badcode[k]+=1
                    counter=0
                    check=True
                    ind1=bracketPair[i][0]
                    ind2=bracketPair[i+1][0]
                    
            return newsen
    elif ">" in sen:
        sen=sen.replace(">", "|")
        sen= '-'+sen
    return sen
 
#This works for basic implication but not for complex implications atm
#Feel like this is the main code I need to edit :thinking:
#Including brackets in this 
def convertCNF(sentence):
    sen=sentence
    #while('>' in sen):
    if ">" in sen:
        if "(" in sen:
            ind=sen.index("(")
            if ind<sen.index(">"):
                 atom=sen[ind]
                 newAtom= "-" + atom
                 sen=sen.replace(">","|")
                 sen=sen.replace(atom, newAtom)
            else:
                sen=sen.replace(">", "|")
                sen= '-'+sen
                
           
        else:
            ind=sen.index(">")
            atom=sen[ind-1]
            newAtom= "-" + atom
            sen=sen.replace(">","|")
            sen=sen.replace(atom, newAtom)
    return sen

def convertCNFArray(KB):
    lol=KB
    final=[]
    for i in KB:
        okay=distributeNegation(convertCNFBetter(i))
        final.append(hardcode(okay))
    return final

def bracketPairs(life):
    bracketPairs=[]
    bracket=[]
    bracketIndex=[]
    counter=0
    for letter in life:
        if letter=="(":
            bracket.append(counter)
        elif letter==")":
            bracketIndex.append(bracket[-1])
            bracketIndex.append(counter)
            bracket.remove(bracket[-1])
            bracketPairs.append(bracketIndex)
            bracketIndex=[]
        counter+=1
    return bracketPairs
    
def bracketPairPair(bracketpair):
    bp=bracketpair
    print(bp)
    return "This shit doesn't work Guy.  Why are you testing it????"
def hardcode(funlife):
    sen = funlife
    counter=0
    check=False
    bracketpair=bracketPairs(sen)
    if len(bracketpair)!=2:
        return sen
    for letter in sen:
        if letter=='(' and check:
            break
        elif letter==')':
            break
        elif letter.isalpha():
            counter+=1
        elif letter=='(':
            check=True
    counter1=0
    check2=False
    for i in range(bracketpair[1][0],bracketpair[1][1]):
        if sen[i]=='(' and check2:
            break
        elif sen[i]==')':
            break
        elif sen[i].isalpha():
            counter1+=1
        elif sen[i]=='(':
            check2=True
    if (counter==1) and (counter1==2):
        if (sen[bracketpair[0][1]+1]=='|'):
            if (sen.find('&')!=-1):
                if (sen.index('&')-bracketpair[1][0]==2):
                    if (sen.index('&')-bracketpair[1][1]==-2):
                        impstr=sen[bracketpair[0][0]+1:bracketpair[0][1]]
                        impstr1=sen[bracketpair[1][0]+1]
                        impstr2=sen[bracketpair[1][1]-1]
                        return ('('+impstr+'|'+impstr1+")&("+impstr+"|"+impstr2+')')
                    elif (sen.index('&')-bracketpair[1][1]==-3):
                        impstr=sen[bracketpair[0][0]+1:bracketpair[0][1]]
                        impstr1=sen[bracketpair[1][0]+1]
                        impstr2=sen[bracketpair[1][1]-2:bracketpair[1][1]]
                        return ('('+impstr+'|'+impstr1+")&("+impstr+"|"+impstr2+')')
                elif (sen.index('&')-bracketpair[1][0]==3):
                    if (sen.index('&')-bracketpair[1][1]==-2):
                        impstr=sen[bracketpair[0][0]+1:bracketpair[0][1]]
                        impstr1=sen[bracketpair[1][0]+1:bracketpair[1][0]+3]
                        impstr2=sen[bracketpair[1][1]-1]
                        return ('('+impstr+'|'+impstr1+")&("+impstr+"|"+impstr2+')')
                        
                    elif (sen.index('&')-bracketpair[1][1]==-3):
                        impstr=sen[bracketpair[0][0]+1:bracketpair[0][1]]
                        impstr1=sen[bracketpair[1][0]+1:bracketpair[1][0]+3]
                        impstr2=sen[bracketpair[1][1]-2:bracketpair[1][1]]
                        return ('('+impstr+'|'+impstr1+")&("+impstr+"|"+impstr2+')')
    return sen
        
        
        
#Possibly add distribution code  for ands and ors and imp code
def SATSolverFormat(KnowB):
    KB=KnowB
    KBno= convertLettersToNo(listOfUniqueAtomsLetters(KB), convertLettersListToNo(listOfUniqueAtomsLetters(KB)), convertCNFArray(KB))
    return convertForSAT(KBno)
def SATSolverFormatLM(KnowB, letters):
    KB=KnowB
    lettes=letters
    KBno= convertLettersToNo(lettes, convertLettersListToNo(lettes), convertCNFArray(KB))
    return convertForSAT(KBno)
a=[]
b=[]
c=[]
#e='(a&b)|(c)'
#f='a|b'
g='(a&c)>(b)'
k='(--a)>(b)'
l='-(a)>(b)'
m='--(a)>(b)'
n='-(-a)>(b)'
a.append('a>b>c')
b.append('(p&-p)>(b)')
c.append('(b)>(p&-p)')
d='((p&b)>(a|c))>(a&b)'
lol='(p&-p)>(b)'
blol='(b)>(p&-p)'
KnowB=["(p)>(b)", "(*b)>(f)", "(*p)>(-f)"]

    
ok=distributeNegation(convertCNFBetter(lol))
ok2=distributeNegation(convertCNFBetter(blol))
ok3=distributeNegation(convertCNFBetter(k))
ok4=distributeNegation(convertCNFBetter(d))
#print(ok3)
#print(distributeNegation(convertCNFBetter(l)))
#print(distributeNegation(convertCNFBetter(m)))
#print(distributeNegation(convertCNFBetter(n)))
#print(ok4)
#print(hardcode(ok))
#print(hardcode(ok2))
#print(hardcode(ok3))
#print(hardcode(ok4))

#print(SATSolverFormat(b))
#print(SATSolverFormat(c))
#print(SATSolverFormat(KnowB))
#print(distributeNegation('(-a)!b'))
#print(distributeNegation('(--a)!b'))
#print(bracketPairPair(bracketPairs(d)))
#print(convertCNFBetter(e))
#print(convertCNFBetter(f))
#print(distributeNegation(convertCNFBetter(d)))
#print(distributeNegation(convertCNFBetter(lol)))
#print(distributeNegation(convertCNFBetter(blol)))
#print(convertCNFBetter(g))
#print(convertCNFArray(b))
#print(convertCNFArray(c))
#print(convertForSAT(convertLettersToNo(listOfUniqueAtomsLetters(b), convertLettersListToNo(listOfUniqueAtomsLetters(b)), convertCNFArray(b))))
#print(convertForSAT(convertLettersToNo(listOfUniqueAtomsLetters(c), convertLettersListToNo(listOfUniqueAtomsLetters(c)), convertCNFArray(c))))
#print(bracketPairs(d))
#KnowB=["a>b","a&b", "a|b", "c>a" ]
#KBno=convertLettersToNo(listOfUniqueAtomsLetters(KnowB), convertLettersListToNo(listOfUniqueAtomsLetters(KnowB)), convertCNFArray(KnowB))
#print("This knowledge base has "+str(noOfUniqueAtomsLetters(KnowB))+" unique atoms")
#print(listOfUniqueAtomsLetters(KnowB))
#print(convertLettersListToNo(listOfUniqueAtomsLetters(KnowB)))
#print(KnowB)
#print(convertCNFArray(KnowB))
#print(KBno)
#print(convertForSAT(KBno))
#removeBrackets("&&&&")
#removeBrackets('(a&b)')
#print('-(a|b)|c'+'                think some more about this')

#print(SATSolverFormat(["a&b"]))
#print(SATSolverFormat(["a|b"]))
#print(len(SATSolverFormat(["a&b"])))
#print(len(SATSolverFormat(["a|b"])))
#removeBrackets('-(a|b)|c')