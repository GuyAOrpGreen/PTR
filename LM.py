# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 13:21:12 2018

@author: Guy
"""

import conversion
import minisolvers
import itertools

S=minisolvers.MinisatSolver()
def createRankedModel(knowB):
    """Takes in a knowledge base as input and returns the LM-Minimal Ranked model
       that the LM Algorithm produces and returns it as a dictionary"""
    #Initialising Variables
    KB=knowB
    letters=conversion.listOfUniqueAtomsLetters(KB)
    interpretations=createInterpretations(KB)
    rankedModel={}
    rankedModel[0]=interpretations
    
    
    if (len(rankedModel)==1): #The First Level
        rankedModel[1]=moveInterpretations(rankedModel[0],KB) #Moving interpretations up a level
        rankedModel[0]=removeContradictoryInterpretations(rankedModel[0], KB) #Keeping the consistent ones 
    if(len(rankedModel)>1):
        counter=1 # Represents level
        while (len(rankedModel[counter-1])!=0): #Checking if the level below is empty
            tempkb=[]
            if (len(rankedModel[counter])==0):
                break
            else:
                nonTypical=checkNonTypicalLetters(rankedModel, letters)
                for sentence in KB:
                    if (hasTypicalityOperator(sentence)):
                        for atomTyp in letters:
                            if (sentence.find('*'+atomTyp)!=-1): #CHecking for each atom in a sentence
                                iOfT=sentence.index('*'+atomTyp)
                                if atomTyp in nonTypical: #If it is non typical, make it unconditionally false
                                    sentence=sentence.replace(sentence[iOfT]+sentence[iOfT+1],"(-"+sentence[iOfT+1]+')&('+sentence[iOfT+1]+')')
                                    
                    
                    tempkb.append(sentence)
                    
               
                rankedModel[counter+1]=moveInterpretations(rankedModel[counter], tempkb)
                rankedModel[counter]=removeContradictoryInterpretations(rankedModel[counter], tempkb)
               
            counter+=1
    return rankedModel

def indOfTypicality(sen):
    """Returns the indices of all the typicality operators in a given sentence"""
    indOfTyp=[]
    for i in range(len(sen)):
        if (sen[i]=='*'):
            indOfTyp.append(i)
    return indOfTyp


def checkNonTypicalLetters(rankedModel, letters):
    """Returns all letters that are not typical on
       the current level of a given Ranked Model"""
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
    """Returns a dictionary showing what level each atom is typical on"""
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
    """Removes all the typicality operators from a given Knowledge base."""
    kb=knowB
    newKb=[]
    for sentence in kb:
        if (hasTypicalityOperator(sentence)):
            newKb.append(sentence.replace("*",""))
        else:
            newKb.append(sentence)
    return newKb

def createInterpretations(knowB):
    """Returns a list of all the possible interpretations of a knowledge base"""
    KB=knowB
    uniqueVar=conversion.noOfUniqueAtomsLetters(KB)
    interpretations=list(itertools.product([0,1], repeat=uniqueVar))
    return interpretations

def hasTypicalityOperator(sentence):
    """Checks if a given sentence has a Typicality Operator. Returns True if it does"""
    sen=sentence
    return sen.__contains__("*")
    
def classicalStatements(knowB):
    """Takes a given knowledge base and returns all the sentences that do not
       contain the Typicality Operator."""
    kb=knowB
    newkb=[]
    for sentence in kb:
        if hasTypicalityOperator(sentence)==False:
            newkb.append(sentence)
    return newkb


def convertInterpretationsToLetters(interpretations, knowB):
    """Takes in interpretations and converts the interpretations 
       to the appropriate letters corresponding to the knowledge base
       and returns this new list."""
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

def removeContradictoryInterpretations(interpretations, knowB):
    """Returns the list of interpretations that are consistent 
       with a given Knowledge Base."""
    inte=interpretations
    kb=knowB
    check=False
    for inter in inte: #Checking if the interpretations are numbers or letters
        for numbers in inter:
            if type(numbers)==int:
                check=True
    if (check):
        newkb=convertInterpretationsToLetters(inte, kb)
    else:
        newkb=inte
        
    finalkb=[]
    
    for i in newkb:
        if (checkInterpretations(i, kb)): #If it's consistent, Keep it
            finalkb.append(i)
   
    return finalkb

def removeContradictoryInterpretationsLM(interpretations, knowB, letters):
    """Returns the list of interpretations that are consistent 
       with a given Knowledge Base. It also takes the list of unique
       atoms as input."""
    inte=interpretations
    kb=knowB
    Letters=letters #Takes Atoms as an extra input
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
    
    for i in newkb:
        if (checkInterpretationsLM(i, kb, Letters)):
            finalkb.append(i)
   
    return finalkb

def moveInterpretations(interpretations, knowB):
    """Returns the List of interpretations which contridict the given knowledge base"""
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
    
    for i in newkb:
        if (checkInterpretations(i, kb)==False): #If it's not consistent, it gets added to the list to be moved
            finalkb.append(i)
   
    return finalkb

def checkInterpretationsLM(interpretations, knowB, letters):
    """Checks if given interpretations are consistent with a given knowledge base.
       also takes a list of unique letters as input as well. Returns True if it is"""
    inte=conversion.SATSolverFormatLM(interpretations, letters)
    kb=knowB
    Letters=letters
    m=minisolvers.MinisatSolver()
    KBno=conversion.SATSolverFormatLM(kb, Letters)
    for i in range(len(Letters)):
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
    """Checks if given interpretations are consistent with a given knowledge base .
       Returns True if it does."""
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
    """Checks Classical Entailment without a Ranked Model. Returns True if it does entail"""
    KB=knowB
    uniqueVar=conversion.noOfUniqueAtomsLetters(KB)
    KBno=conversion.SATSolverFormat(KB)
    sen=sentence
    uni=conversion.listOfUniqueAtomsLetters(KB)
    Ent=minisolvers.MinisatSolver()
    uniNo=conversion.convertLettersListToNo(uni)
    check=addNegation(sen, uniNo, uni) #Sentence being checked is negated
    for i in check: #Check is already in SAT-SOlver format
        KBno.append(i)
        
    
    for i in range(uniqueVar):
        Ent.new_var()

    for clause in KBno:
        Ent.add_clause(clause)
        
    if (Ent.solve()):
        return False
    else:
        return True

def LMEntailment(KnowB, sentence):
    """Checks if a given sentence entails from a given knowledge base.
       It returns true if it does"""
    KB=KnowB
    
    
    lll=conversion.listOfUniqueAtomsLetters(KB)
    anolll=conversion.listOfUniqueAtomsLetters(KB)
    RM=createRankedModel(KB)
    sen=sentence
    if hasTypicalityOperator(sen):
        typ=TypicalityLetters(RM, lll)
        check=False
        letter=[]
        for i in sen: #Looking for the atoms with the typicality operator being applied
            if i=="*":
                check=True
            elif (i.isalpha()) and (check):
                letter.append(i)
                check=False
        check2=False
        for j in typ: #Comparing and checking levels for which those atoms are most typical
            for k in letter:
                if (k in typ[j]) and (check2==False):
                    level=j
                    check2=True
                elif(k in typ[j]) and (j!=level) and (check2):
                    return False
        releventInterpretations=RM[level] #returning the relevent level needing to be checked
        if sen.find(">")!=-1:
            left=[]
            left.append(sen[:sen.index(">")])
            releventInterpretations=removeContradictoryInterpretationsLM(releventInterpretations, left, anolll) #Only looking at the relevant interpretations to the sentence
        for inte in releventInterpretations:
            if (checkEntailment(inte, sen)==False): #if there is a contradiction
                return False
        return True
                
    
    else: #IF it is a classical statement being checked checking each interpretation
        for lev in RM:
            rellev=RM[lev]
            if (len(rellev)==0):
                return True 
            for interpret in rellev:
                if (checkEntailment(interpret, sen)==False):
                    return False

    


def checkConsistency(knowB):
    """Checks if a Knowledge Base is consistent with itself. Returns True if it is"""
    KB=knowB
    uniqueVar=conversion.noOfUniqueAtomsLetters(KB)
    KBno=conversion.SATSolverFormat(KB)
    
    for i in range(uniqueVar):
        S.new_var()

    for clause in KBno:
        S.add_clause(clause)
    
    return S.solve()

def getModel():
    """Returns the model of what is currently in the SAT-Solver"""
    return S.get_model()

def addNegation(sentence, listOfNumbers, letters):
    """Given a sentence, it returns the negation of that sentence in SAT-Solver Format"""
    sent=[]
    sent.append(sentence)
    numbers=listOfNumbers
    ll=letters #converting the sentence to SAT Solver format
    sent=conversion.SATSolverFormat(conversion.convertLettersToNo(ll, numbers, conversion.convertCNFArray(sent)))
    newSent=[]
    andSent=[] 
    if len(sent)==1:
        for i in sent:
            for k in i:
                if type(k) is int: #Converting the ors to ands
                    newSent.append([(k*-1)])
                elif type(k) is list:
                    for j in k:
                        newSent.append([int(j)*-1]) #multiply by -1 to get the negation
    else:
        for j in sent:
            for i in j: #converting the ands to ors
                andSent.append(int(i)*-1)
        newSent.append(andSent)
    return newSent




