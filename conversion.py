# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 14:37:30 2018

@author: Guy
"""

def listOfUniqueAtomsLetters(KnowB):
    """A function returning a list of the unique atoms in a Knowledge Base"""
    KB=KnowB
    atoms=[]
    for i in KB:
        for j in i:
            if j in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if j not in atoms:
                    atoms.append(j)
                else:
                    continue
            
    return atoms

def noOfUniqueAtomsLetters(listOfAtoms):
    """A function returning the number of Unique Atoms there are in a knowledge base"""
    strAtoms=listOfAtoms
    counter=0
    atoms=[]
    for i in strAtoms:
        for j in i:
            if j in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if j not in atoms:
                    atoms.append(j)
                    counter+=1
                else:
                    continue
            
    return counter


def convertLettersListToNo(listOfAtoms):
    """A function that returns a list of numbers corresponding to each atom 
       to help with the conversion to SAT-Solver Format"""
    letters=listOfAtoms
    numbers=[]
    counter=1
    for letter in letters:
        numbers.append(counter)
        counter+=1;
    return numbers

def distributeNegation(sentence):
    """A recursive function that propogates the negation to the innermost brackets 
       and then returns the sentence"""
    sen= sentence
    newsen=sen
    sen=sen.replace('--','') #Getting rid of all the double negations
    newsen=newsen.replace('--','')
    if (newsen.find('-(')==-1): #No negation needing to be propagated
        return newsen
    else:
        ind=newsen.index('-(') +2 #The index that traversing is started at
        counter=0 #Keeps track Brackets Traversed in current brackets being looked at
        counter1=0 #Keeps track of indice increases
        counter2=0 #Keeps track of indice increases
        if (newsen[ind:len(newsen)].find(")")<newsen[ind:len(newsen)].find("(")): #if there are no brackets inside the current bracket
            for i in range(ind,len(newsen)):
                if (newsen[i+counter2]==')'):
                    break
                elif (newsen[i+counter2] =='|'): #Replacing ors
                    newsen=newsen[:i+counter2]+'&'+newsen[i+counter2+1:]
                elif (newsen[i+counter2] == '&'): #Replacing Ands
                    newsen=newsen[:i+counter2]+'|'+newsen[i+counter2+1:]
                elif (newsen[i+counter2].isalpha()): #Atoms
                    newsen=newsen[:i+counter2]+'-'+newsen[i+counter2:]
                    counter2+=1
            return newsen[:newsen.index('-(')] + distributeNegation(newsen[newsen.index('-(')+1:])
       
        for i in range(ind, len(newsen)):
            if (newsen[i+counter1]==")") and (counter==0):
                break
            elif (newsen[i+counter1]=='(') and (counter==0): #bracket inside the one being checked
                counter+=1
                newsen=newsen[:i+counter1]+'-'+newsen[i+counter1:]
                counter1+=1
            elif (newsen[i+counter1]=='('): #ignoring the bracket inside the brackets
                counter+=1
            elif (newsen[i+counter1]==')'):
                counter-=1
            elif (newsen[i+counter1]=='|') and (counter==0): #Replacing or relative to the current bracket
                newsen=newsen[:i+counter1]+'&'+newsen[i+counter1+1:]
            elif (newsen[i+counter1]=='&') and (counter==0): #Replacing and relative to the current bracket
                newsen=newsen[:i+counter1]+'|'+newsen[i+counter1+1:]
        
        return newsen[:sen.index('-(')] + distributeNegation(newsen[newsen.index('-(')+1:]) #Once negation is propagated once it is done again until it is not needed
 
def convertForSAT(KB):
    """A function that converts the Knowledge Base to SAT-Solver Format and
       then returns the list"""
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
    """Converts the Knowledge Base to be in terms of the corresponding Numbers
       rather than letters"""
    newKB=[]
    letters=listOfLetters
    numbers=listOfNumbers
    for sentence in KB:
        newSentence=sentence
        for letter in letters:
            newSentence=newSentence.replace(letter, str(numbers[letters.index(letter)]))
        newKB.append(newSentence)
    return newKB




def convertCNF(Sentence):
    """Converts a given sentence to CNF and returns it"""
    sen=Sentence
    if "(" in sen:
        if ">" in sen:
            newsen=sen
            bracketPair=bracketPairs(sen)
            counter=0
            
            for i in range(len(bracketPair)):                
                ind1=bracketPair[i][0] #Relevant bracket index
                ind2=bracketPair[i][2] #Relevant bracket index
                if (newsen[ind1-1]=='>'):
                    newsen=newsen[:ind2]+'-'+newsen[ind2:]
                    newsen=newsen[:ind1]+'|'+newsen[ind1+1:]
                    counter+=ind2
                        
                    for bracket in bracketPair:
                        for k in range(len(bracket)):
                            if (bracket[k]>counter):
                                bracket[k]+=1 #Increasing index of brackets after the negation that was added
                    counter=0
                    
            return newsen
    elif ">" in sen:
        sen=sen.replace(">", "|")
        sen= '-'+sen
    return sen 



def convertCNFArray(KB):
    """Takes in a Knowledge base as input. Calls convertCNF for each 
       sentence in the Knowledge Base, then it calls distribute Negation,
       then propogate disjunction. Returns a sentence that is abe to be 
       converted to SAT-Solver format"""
    final=[]
    for i in KB:
        halfConvertedSentence=distributeNegation(convertCNF(i))
        final.append(propogateDisjunction(halfConvertedSentence))
    return final

def propogateDisjunctionNeeded(sen):
    """"Determines whether or not propogation of disjunction is needed. 
        Returns True if it is"""
    bracketPair=bracketPairs(sen)
    check=False
    for i in bracketPair:
        if (sen[i[0]-1]=='&') & (check):
            if (i[0]-1>checker[0] and i[0]-1<checker[1]) or (i[0]-1>checker[2] and i[0]-1<checker[3]):
                return True
        elif sen[i[0]-1] == '|':
            check=True
            checker=i
    return False

def propogateDisjunction(sen):
    """This function takes in a sentence as input and returns the sentence with the
       disjunction operators propogated as far as possible."""
    bracketPair=bracketPairs(sen)
    newsen=sen
    check=False
    if (propogateDisjunctionNeeded(sen)):
        for i in bracketPair:
            if (sen[i[0]-1]=='&') & (check):
                if (i[0]-1>checker[0] and i[0]-1<checker[1]) or (i[0]-1>checker[2] and i[0]-1<checker[3]):
                    andind=i[0]-1 #Getting the index of the relevant and operator
                    break
            elif sen[i[0]-1] == '|':
                orind=i[0]-1 #Getting the index of the relevant or operator
                check=True
                checker=i
        
        if (orind>andind): #Checking if the and operator is in the antecedent
            relevantInd=[]
            relevantIndbigger=[]
            for x in bracketPair:
                if (x[0]+1==andind) or (x[0]-1==andind):
                    relevantInd=x
                    break
            
            for y in  bracketPair:
                if (y[0]+1==orind) or (y[0]-1==orind):
                    relevantIndbigger=y
                    break
            firstPart='('+sen[relevantInd[2]:relevantInd[3]+1]+'|'+sen[relevantIndbigger[0]:relevantIndbigger[1]+1]+')' #taking the antecedent of the and operator disjuncted with the consequence of the or operator 
            secondPart='('+sen[relevantInd[0]:relevantInd[1]+1]+'|'+sen[relevantIndbigger[0]:relevantIndbigger[1]] +')' #taking the consequence of the and operator disjuncted with the consequence of the or operator
            newsen=sen[:relevantIndbigger[2]]+firstPart+"&"+secondPart+sen[relevantIndbigger[1]:]
            return propogateDisjunction(newsen) #recursively calling once it has been done once
        else: #The and operator is in the consequence
            relevantInd=[]
            relevantIndbigger=[]
            for x in bracketPair:
                if (x[0]+1==andind) or (x[0]-1==andind):
                    relevantInd=x
                    break
            
            for y in  bracketPair:
                if (y[0]+1==orind) or (y[0]-1==orind):
                    relevantIndbigger=y
                    break
            firstPart='('+sen[relevantInd[2]:relevantInd[3]+1]+'|'+sen[relevantIndbigger[2]:relevantIndbigger[3]+1]+')' #taking the antecedent of the and operator disjuncted with the antecedent of the or operator 
            secondPart='('+sen[relevantInd[0]:relevantInd[1]+1]+'|'+sen[relevantIndbigger[2]:relevantIndbigger[3]+1] #taking the consequence of the and operator disjuncted with the antecedent of the or operator
            newsen=sen[:relevantIndbigger[2]]+firstPart+'&'+secondPart+sen[relevantIndbigger[1]:]
            return propogateDisjunction(newsen) #recursively calling once it has been done once
    else: #If propogation isn't needed
        return sen


    
def bracketPairs(bracketpair):
    """Takes a sentence as input and returns 2D list of bracket pairs paired up.
       Each list represents the indices of the brackets the antecedent and consequence
       of each operator. This is reversed so it can represent the outermost brackets first"""
    bracketPairs=[]
    bracket=[]
    bracketIndex=[]
    counter=0
    bracketPairsPaired=[]
    for letter in bracketpair:#Pairing each bracket with the bracket that closes it 
        if letter=="(":
            bracket.append(counter)
        elif letter==")":
            bracketIndex.append(bracket[-1])
            bracketIndex.append(counter)
            bracket.remove(bracket[-1])
            bracketPairs.append(bracketIndex)
            bracketIndex=[]
        counter+=1 
    bracketPairs=bracketPairs[::-1] #reversing it to start with the last brackets closed
    for i in  range(len(bracketPairs)): #Pairing each bracket pair with the other bracket pair that would only be separated by an operator
        currentBrackets=[]
        ind1=bracketPairs[i][0]
        for j in range(len(bracketPairs)):
            if (bracketPairs[j][1]+2==ind1):
                currentBrackets.append(bracketPairs[i][0])
                currentBrackets.append(bracketPairs[i][1])
                currentBrackets.append(bracketPairs[j][0])
                currentBrackets.append(bracketPairs[j][1])
                bracketPairsPaired.append(currentBrackets)
    return bracketPairsPaired


def SATSolverFormat(KnowB):
    """Calls all the functions needed for the conversion of
    a Knowledge Base to a format compatible with the SAT-Solver. 
    Takes input of the Knowledge Base. Returns Knowledge base 
    in SAT Solver format"""
    KB=KnowB
    KBno= convertLettersToNo(listOfUniqueAtomsLetters(KB), convertLettersListToNo(listOfUniqueAtomsLetters(KB)), convertCNFArray(KB))
    return convertForSAT(KBno)


def SATSolverFormatLM(KnowB, letters):
    """Calls all the functions needed for the conversion of
    a Knowledge Base to a format compatible with the SAT-Solver. 
    Takes input of the Knowledge Base and the unique letters in 
    the Knowledge Base. Returns Knowledge base in SAT Solver format"""
    KB=KnowB
    Letters=letters
    KBno= convertLettersToNo(Letters, convertLettersListToNo(Letters), convertCNFArray(KB))
    return convertForSAT(KBno)
