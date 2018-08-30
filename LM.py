# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 13:21:12 2018

@author: Guy
"""

import conversion
import minisolvers
import itertools

S=minisolvers.MinisatSolver()
#Dictionaries for ranked interpretation
def createRankedModel(knowB):
    KB=knowB
    letters=conversion.listOfUniqueAtomsLetters(KB)
    interpretations=createInterpretations(KB)
    rankedModel={}
    rankedModel[0]=interpretations
    if (len(rankedModel)==1):
        rankedModel[1]=moveInterpretations(rankedModel[0],KB)
        rankedModel[0]=removeContradictoryInterpretations(rankedModel[0], KB)
    if(len(rankedModel)>1):
        counter=1
        while (len(rankedModel[counter-1])!=0):
            tempkb=[]
            if (len(rankedModel[counter])==0):
                break
            else:
                nonTypical=checkNonTypicalLetters(rankedModel, letters)
                for sentence in KB:
                    if (hasTypicalityOperator(sentence)):
                        iOfT=sentence.index("*")
                        if sentence[iOfT+1] in nonTypical:
                            sentence=sentence.replace(sentence[iOfT]+sentence[iOfT+1],"-"+sentence[iOfT+1]+'&'+sentence[iOfT+1])
                    tempkb.append(sentence)
               # print("Before")
               # print(rankedModel[counter])
               # print("Before")
               # print(tempkb)
                rankedModel[counter+1]=moveInterpretations(rankedModel[counter], tempkb)
                rankedModel[counter]=removeContradictoryInterpretations(rankedModel[counter], tempkb)
               # print("")
               # print(tempkb)
               # print("")
                #print(rankedModel[counter+1])
                #print("")
                #print(rankedModel[counter])
                #print("")
                #Make a list of letters that typicality sentences have already been changed for and check that.
            
                
            counter+=1
          #  print("No idea yet")
          #  counter+=1
    return rankedModel

def checkNonTypicalLetters(rankedModel, letters):
    rm=rankedModel
    l=letters
    nonTypicalAtoms=[]
    for level in rm:
        if level+1==len(rm):
            return nonTypicalAtoms
        else:
            for a in l:
                letter=True
                for inte in rm[level]:
                    if inte[l.index(a)].__contains__("-"+a)==False:
                        letter=False
                if (letter==False):
                    nonTypicalAtoms.append(a)
            
        
    return nonTypicalAtoms

def TypicalityLetters(rankedModel, letters):
    rm=rankedModel
    l=letters
    TypicalAtoms={}
    for level in rm:
        if level+1==len(rm):
            return TypicalAtoms
        else:
            k=[]
            for a in l:
                letter=True
                for inte in rm[level]:
                    if inte[l.index(a)].__contains__("-"+a)==False:
                        letter=False
                if (letter==False):
                    k.append(a)
            TypicalAtoms[level]=k
            for b in k:
                l.remove(b)
            
        
    return TypicalAtoms


def convertToClassical(knowB):
    kb=knowB
    newKb=[]
    for sentence in kb:
        if (hasTypicalityOperator(sentence)):
            newKb.append(sentence.replace("*",""))
        else:
            newKb.append(sentence)
    return newKb

def createInterpretations(knowB):
    KB=knowB
    uniqueVar=conversion.noOfUniqueAtomsLetters(KB)
    interpretations=list(itertools.product([0,1], repeat=uniqueVar))
    return interpretations

def hasTypicalityOperator(sentence):
    sen=sentence
    return sen.__contains__("*")
    
def classicalStatements(knowB):
    kb=knowB
    newkb=[]
    for sentence in kb:
        if hasTypicalityOperator(sentence)==False:
            newkb.append(sentence)
    return newkb


def convertInterpretationsToLetters(interpretations, knowB):
    inte=interpretations
    kb=knowB
    letters=conversion.listOfUniqueAtomsLetters(kb)
    newkb=[]
    for inter in inte:
        counter=0
        singleinte=[]
        for i in inter:
            if i == 1:
                singleinte.append(letters[counter])
                
                counter+=1
            elif i==0:
                singleinte.append("-"+letters[counter])
                counter+=1
        newkb.append(singleinte)
    return newkb

def removeContradictoryInterpretations(interpretations, knowB):# Should seperate this functionn into converting letters and check
    inte=interpretations
    kb=knowB
    check=False
    for inter in inte:
        for numbers in inter:
            if type(numbers)==int:
                check=True
    if (check):
        newkb=convertInterpretationsToLetters(inte, kb)
    else:
        newkb=inte
        
    finalkb=[]
    
    for i in newkb:#this where my first bug is 
        if (checkInterpretations(i, kb)):
            finalkb.append(i)
   
    return finalkb

def removeContradictoryInterpretationsLM(interpretations, knowB, letters):# Should seperate this functionn into converting letters and check
    inte=interpretations
    kb=knowB
    letters=letters
    check=False
    for inter in inte:
        for numbers in inter:
            if type(numbers)==int:
                check=True
    if (check):
        newkb=convertInterpretationsToLetters(inte, kb)
    else:
        newkb=inte
        
    finalkb=[]
    
    for i in newkb:#this where my first bug is 
        if (checkInterpretationsLM(i, kb, letters)):
            finalkb.append(i)
   
    return finalkb

def moveInterpretations(interpretations, knowB):
    inte=interpretations
    kb=knowB
    check=False
    
    for inter in inte:
        for numbers in inter:
            if type(numbers)==int:
                check=True
    if (check):
        newkb=convertInterpretationsToLetters(inte, kb)
    else:
        newkb=inte
    
    finalkb=[]
    
    for i in newkb:#this where my first bug is 
        if (checkInterpretations(i, kb)==False):
            finalkb.append(i)
   
    return finalkb

def checkInterpretationsLM(interpretations, knowB, lettes):
    inte=conversion.SATSolverFormat(interpretations)
    kb=knowB
    letters=lettes
    m=minisolvers.MinisatSolver()
    KBno=conversion.SATSolverFormatLM(kb, letters)
    for i in range(len(letters)):
        m.new_var()
    
    for clause in KBno:
        m.add_clause(clause)
    
    for clause2 in inte:
        m.add_clause(clause2)
        
    if (m.solve()):
        return True
    else:
        return False

def checkInterpretations(interpretations, knowB):
    inte=conversion.SATSolverFormat(interpretations)
    kb=knowB
    m=minisolvers.MinisatSolver()
    uniqueVar=conversion.noOfUniqueAtomsLetters(kb)
    KBno=conversion.SATSolverFormat(kb)
    for i in range(uniqueVar):
        m.new_var()
    
    for clause in KBno:
        m.add_clause(clause)
    
    for clause2 in inte:
        m.add_clause(clause2)
        
    if (m.solve()):
        return True
    else:
        return False
    
def checkEntailment(knowB, sentence):
    KB=knowB
    uniqueVar=conversion.noOfUniqueAtomsLetters(KB)
    KBno=conversion.SATSolverFormat(KB)
    sen=sentence
    #Might have to add negation to sen
    uni=conversion.listOfUniqueAtomsLetters(KB)
    Ent=minisolvers.MinisatSolver()
    uniNo=conversion.convertLettersListToNo(uni)
    check=addNegation(sen, uniNo, uni)
    for i in check:
        KBno.append(i)
        
    
    for i in range(uniqueVar):
        Ent.new_var()

    for clause in KBno:
        Ent.add_clause(clause)
        
    if (Ent.solve()):
        return False
    else:
        return True
""""def checkInLM(interp, knowb):
    LMEnt=minisolvers.MinisatSolver()
    KB=knowb
    inte=interp
    uniqueVar=conversion.noOfUniqueAtomsLetters(inte)
    letters=conversion.listOfUniqueAtomsLetters(inte)
    numbers=conversion.convertLettersListToNo(letters)
    inte=conversion.SATSolverFormat(inte)
    KB=addNegation(sen,numbers, letters)"""
def LMEntailment(KnowB, sentence):
    KB=KnowB
    
    
    lll=conversion.listOfUniqueAtomsLetters(KB)
    RM=createRankedModel(KB)
    sen=sentence
    if hasTypicalityOperator(sen):
        typ=TypicalityLetters(RM, letters)
        check=False
        letter=[]
        for i in sen:
            if i=="*":
                check=True
            elif (i.isalpha()) and (check):
                letter.append(i)
                check=False
        check2=False
        for j in typ:
            for k in letter:
                if (k in typ[j]) and (check2==False):
                    level=j
                    check2=True
                elif(k in typ[j]) and (j!=level) and (check2):
                    return False
        print(level)
        releventInterpretations=RM[level]
        if sen.find(">")!=-1:
            left=[]
            left.append(sen[:sen.index(">")])
            releventInterpretations=removeContradictoryInterpretationsLM(releventInterpretations, left, lll)
        for inte in releventInterpretations:
            if (checkEntailment(inte, sen)==False):
                return False
        return True
        #gotta check interpretations with sentence still
                
                
                    
        # Maybe do this 
                
    #create a new one check interpretations
    
    else:
        #gotta check every level of ranked model
        for lmao in RM:
            rellev=RM[lmao]
            if (len(rellev)==0):
                return True #not checking only interpretations that are true for what is being checked
            for okay in rellev:
                if (checkEntailment(okay, sen)==False):
                    return False
    
    #for i in sen:
     #   if i.isalpha():
      #      letter=i
       #     break
    #for i in typ:
     #   if (letter in typ[i]):
      #      level=RM[i]
       #     break
    
    #for i in range(uniqueVar):
     #   LMEnt.new_var()
    
    #for lol in level:
      #     lol=conversion.SATSolverFormat(lol)
     #      for j in lol:
    #           LMEnt.add_clause(j)
           
   # sen=addNegation(sen,numbers, letters)
    
    
    
    #for i in sen:
     #   LMEnt.add_clause(i)
        
    #for clause in newlevel:
     #   LMEnt.add_clause(clause)
        
    #if (LMEnt.solve()):
     #   return False
   # else:
    #    return True

def checkConsistency(knowB):
    KB=knowB
    uniqueVar=conversion.noOfUniqueAtomsLetters(KB)
    KBno=conversion.SATSolverFormat(KB)
    
    for i in range(uniqueVar):
        S.new_var()

    for clause in KBno:
        S.add_clause(clause)
    
    return S.solve()

def getModel():
  return S.get_model()

def addNegation(sentence, listOfNumbers, letters):
    sent=[]
    sent.append(sentence)
    numbers=listOfNumbers
    ll=letters
    sent=conversion.SATSolverFormat(conversion.convertLettersToNo(ll, numbers, conversion.convertCNFArray(sent)))
    newSent=[]
    andSent=[]
    if len(sent)==1:
        for i in sent:
            for k in i:
                if type(k) is int:
                    newSent.append([(k*-1)])
                elif type(k) is list:
                    for j in k:
                        newSent.append([int(j)*-1])
    else:
        for j in sent:
            for i in j:
                andSent.append(int(i)*-1)
        newSent.append(andSent)
    return newSent

KnowB=["(p)>(b)", "(*b)>(f)", "(*p)>(-f)"]
KnowB3=["(p)>(b)", "(b)>(*f)", "(p)>(-f)"]
#print(conversion.SATSolverFormat(KnowB))
KnowB2=["p>b", "*b>f", "*p>-f"]
sen='(*p)>(*b)'
#print(conversion.SATSolverFormat(KnowB2))
inter=createInterpretations(KnowB)
#print(len(inter))
#print(inter)
#print(removeContradictoryInterpretations(inter,KnowB))
#nte=createInterpretations(KnowB2)
letters=conversion.listOfUniqueAtomsLetters(KnowB)
numbers=conversion.convertLettersListToNo(letters)
'''
print(letters)
print(numbers)
print(addNegation('(*p)>(f)',numbers ,letters))
print()
print(conversion.SATSolverFormatLM(['(*p)>(f)'], letters))
'''

#inte=[['-p','b','-f'],['p','-b','-f'],['p','-b','f'],['p','b','-f'],['p','b','-f']]
#satisfiable=removeContradictoryInterpretations(inte, KnowB2)
#print(satisfiable)



if (LMEntailment(KnowB, sen)):
    print('entailment FTW')
else:
    print('Fuck')


'''

RM2=createRankedModel(KnowB3)
RM=createRankedModel(KnowB)
for k in RM:
    print(k)
    print(RM[k])
print()
print("This is what it should produce")
for i in RM2:
    print(i)
    print(RM2[i])
'''
#print("")
#print(TypicalityLetters(RM,letters))
#print(len(RM))
#print(len(RM[0]))
#print(len(RM[1]))