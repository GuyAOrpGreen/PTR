# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 23:05:51 2018

@author: Guy
"""


import LM
while True:
    print("Choose a sample knowledge base:")
    print("The options are the Tweety (T), Flying Fish (F), the Paper (P), Make your own (O) or quit(x)")
    choice =input("Please Type either T, F, P, O or x: ")
    if (choice=='x'):
        break
    elif (choice=="T"):
        KnowB=["(p)>(b)", "(*b)>(f)", "(*p)>(-f)"]
        RM=LM.createRankedModel(KnowB)
        print("")
        print("The Knowledge Base you have chosen is as follows:")
        print(KnowB)
        print()
        print("Would you like to Check Entailment (E) of a sentence, see the LM-Minimal Model (LM) of the Knowledge Base or both (B)")
        choice =input("Please Type either E, LM, or B: ")
        if (choice=="LM"):
            print("")
            print("The LM-Minimal Model is as follows:")
            print()
            check=False
            for i in RM:
                if (len(RM[i])==0):
                    check=True
                elif (len(RM[i])!=0) and (check):
                    print("Linf:  "+str(RM[i]))
                elif (len(RM[i])!=0):
                    print("L"+str(i)+"  :  "+str(RM[i]))    
        elif choice=="B":
            print("")
            print("The LM-Minimal Model is as follows:")
            print()
            check=False
            for i in RM:
                if (len(RM[i])==0):
                    check=True
                elif (len(RM[i])!=0) and (check):
                    print("Linf:  "+str(RM[i]))
                elif (len(RM[i])!=0):
                    print("L"+str(i)+"  :  "+str(RM[i])) 
            print("")
            sentence=input("What sentece would you like to see if it is entailed: ")
            if (sentence==""):
                sentence="(p)>(-*b)"
            print()
            try:
                if (LM.LMEntailment(KnowB,sentence)):
                    print("The sentence, "+sentence+", does entail from the knowledge base.")
                else:
                    print("The sentence, "+sentence+", does not entail from the knowledge base.")
            except:
                print("An error occurred.")
        elif choice=="E":
            print("")
            sentence=input("What sentece would you like to see if it is entailed: ")
            if (sentence==""):
                sentence="(p)>(-*b)"
            print()
            try:
                if (LM.LMEntailment(KnowB,sentence)):
                    print("The sentence, "+sentence+", does entail from the knowledge base.")
                else:
                    print("The sentence, "+sentence+", does not entail from the knowledge base.")
            except:
                print("An error occurred.")
        else:
            print("You entered an invalid option.")
            choice =input("Please Type either E, LM, or B: ")
            

    elif (choice=='F'):
        KnowB=["(*b)>(f)",'(e)>(-*f)', '(e)>(-b)', '(*f)>(w)']
        RM=LM.createRankedModel(KnowB)
        print("")
        print("The Knowledge Base you have chosen is as follows:")
        print(KnowB)
        print()
        print("Would you like to Check Entailment (E) of a sentence, see the LM-Minimal Model (LM) of the Knowledge Base or both (B)")
        choice =input("Please Type either E, LM, or B: ")
        if (choice=="LM"):
            print("")
            print("The LM-Minimal Model is as follows:")
            print()
            check=False
            for i in RM:
                if (len(RM[i])==0):
                    check=True
                elif (len(RM[i])!=0) and (check):
                    print("Linf:  "+str(RM[i]))
                elif (len(RM[i])!=0):
                    print("L"+str(i)+"  :  "+str(RM[i]))    
        elif choice=="B":
            print("")
            print("The LM-Minimal Model is as follows:")
            print()
            check=False
            for i in RM:
                if (len(RM[i])==0):
                    check=True
                elif (len(RM[i])!=0) and (check):
                    print("Linf:  "+str(RM[i]))
                elif (len(RM[i])!=0):
                    print("L"+str(i)+"  :  "+str(RM[i])) 
            print("")
            sentence=input("What sentece would you like to see if it is entailed: ")
            if (sentence==""):
                sentence="(*e)>(w)"
            print()
            try:
                if (LM.LMEntailment(KnowB,sentence)):
                    print("The sentence, "+sentence+", does entail from the knowledge base.")
                else:
                    print("The sentence, "+sentence+", does not entail from the knowledge base.")
            except:
                print("An error occurred.")
        elif choice=="E":
            print("")
            sentence=input("What sentece would you like to see if it is entailed: ")
            if (sentence==""):
                sentence="(*e)>(w)"
            print()
            try:
                if (LM.LMEntailment(KnowB,sentence)):
                    print("The sentence, "+sentence+", does entail from the knowledge base.")
                else:
                    print("The sentence, "+sentence+", does not entail from the knowledge base.")
            except:
                print("An error occurred.")
        else:
            print("You entered an invalid option.")
            choice =input("Please Type either E, LM, or B: ")
            
        
        
    elif (choice=="P"):
        KnowB=['(*t)>(-p&-r)', '(t)>(p|-p)', '(-p|t)&(p|t)', '(*p)>(*y)', '(y)>(-f)', '(-f)>(y)', '(*r)>(*f)']
        RM=LM.createRankedModel(KnowB)
        print("")
        print("The Knowledge Base you have chosen is as follows:")
        print(KnowB)
        print()
        print("Would you like to Check Entailment (E) of a sentence, see the LM-Minimal Model (LM) of the Knowledge Base or both (B)")
        choice =input("Please Type either E, LM, or B: ")
        if (choice=="LM"):
            print("")
            print("The LM-Minimal Model is as follows:")
            print()
            check=False
            for i in RM:
                if (len(RM[i])==0):
                    check=True
                elif (len(RM[i])!=0) and (check):
                    print("Linf:  "+str(RM[i]))
                elif (len(RM[i])!=0):
                    print("L"+str(i)+"  :  "+str(RM[i]))    
        elif choice=="B":
            print("")
            print("The LM-Minimal Model is as follows:")
            print()
            check=False
            for i in RM:
                if (len(RM[i])==0):
                    check=True
                elif (len(RM[i])!=0) and (check):
                    print("Linf:  "+str(RM[i]))
                elif (len(RM[i])!=0):
                    print("L"+str(i)+"  :  "+str(RM[i])) 
            print("")
            sentence=input("What sentece would you like to see if it is entailed: ")
            if (sentence==""):
                sentence="(p)>(-*f)"
            print()
            try:
                if (LM.LMEntailment(KnowB,sentence)):
                    print("The sentence, "+sentence+", does entail from the knowledge base.")
                else:
                    print("The sentence, "+sentence+", does not entail from the knowledge base.")
            except:
                print("An error occurred.")
        elif choice=="E":
            print("")
            sentence=input("What sentece would you like to see if it is entailed: ")
            if (sentence==""):
                sentence="(p)>(*-f)"
            print()
            try:
                if (LM.LMEntailment(KnowB,sentence)):
                    print("The sentence, "+sentence+", does entail from the knowledge base.")
                else:
                    print("The sentence, "+sentence+", does not entail from the knowledge base.")
            except:
                print("An error occurred.")
        else:
            print("You entered an invalid option.")
            choice =input("Please Type either E, LM, or B: ")
    
    
    
    elif (choice=="O"):
        KnowB=[]
        while(True):
            print()
            print("Please input a sentence and please ensure there are the right number of brackets or 'x' when you are done: ")
            sen=input()
            if (sen=="x"):
                break
            else:
                KnowB.append(sen)
        RM=LM.createRankedModel(KnowB)
        print("")
        print("The Knowledge Base you have chosen is as follows:")
        print(KnowB)
        print()
        while (True):
            print("Would you like to Check Entailment (E) of a sentence, see the LM-Minimal Model (LM) of the Knowledge Base or both (B)")
            choice =input("Please Type either E, LM, or B: ")
            if (choice=="LM"):
                print("")
                print("The LM-Minimal Model is as follows:")
                print()
                check=False
                for i in RM:
                    if (len(RM[i])==0):
                        check=True
                    elif (len(RM[i])!=0) and (check):
                        print("Linf:  "+str(RM[i]))
                    elif (len(RM[i])!=0):
                        print("L"+str(i)+"  :  "+str(RM[i])) 
                ans=input("Would you like to use this Knowledge Base again? (y/n):")
                if (ans!='y'):
                    break
            elif choice=="B":
                print("")
                print("The LM-Minimal Model is as follows:")
                print()
                check=False
                for i in RM:
                    if (len(RM[i])==0):
                        check=True
                    elif (len(RM[i])!=0) and (check):
                        print("Linf:  "+str(RM[i]))
                    elif (len(RM[i])!=0):
                        print("L"+str(i)+"  :  "+str(RM[i])) 
                print("")
                sentence=input("What sentece would you like to see if it is entailed: ")
                print()
                try:
                    if (LM.LMEntailment(KnowB,sentence)):
                        print("The sentence, "+sentence+", does entail from the knowledge base.")
                    else:
                        print("The sentence, "+sentence+", does not entail from the knowledge base.")
                except:
                    print("An error occurred.")
                ans=input("Would you like to use this Knowledge Base again? (y/n):")
                if (ans!='y'):
                    break
            elif choice=="E":
                print("")
                sentence=input("What sentece would you like to see if it is entailed: ")
                print()
                try:
                    if (LM.LMEntailment(KnowB,sentence)):
                        print("The sentence, "+sentence+", does entail from the knowledge base.")
                    else:
                        print("The sentence, "+sentence+", does not entail from the knowledge base.")
                except:
                    print("An error occurred.")
                ans=input("Would you like to use this Knowledge Base again? (y/n):")
                if (ans!='y'):
                    break
            else:
                print("You entered an invalid option.")
            
    else:
        print("You entered an invalid option.")
    print()