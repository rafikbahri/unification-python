#verify if an expression is an atom
def isAtom(e):
    return len(e)==1


#return an expression from a function f(...)
def expression(e):
    #list contains the elements of the expression
    listofelements=[]
    #remove the ()
    expr=e[e.find("(")+1:e.rfind(")")]

    #while the expression still contains elements
    while not expr=="":
        #the expression contains only 1 element
        if not ',' in expr:
            listofelements.append(expr)
            expr=""
        else:
            #if the first element in the expression is not a function
            if not '(' in expr[:expr.find(',')]:
                listofelements.append(expr[:expr.find(',')])
                expr=expr[expr.find(',')+1:]
            else:
                #if the first element in the expression is a function
                begin=0
                end=0
                nb_of_opening_par=0
                nb_of_closing_par=0
                end_of_elements=False
                i=0
                while not end_of_elements:
                    c=expr[i]
                    if c=='(':
                        if begin==0:
                            begin=i
                        nb_of_opening_par+=1
                    else:
                        if c==')':
                            nb_of_closing_par+=1
                            if nb_of_opening_par==nb_of_closing_par and nb_of_opening_par>0:
                                end=i
                                end_of_elements=True
                                i=0
                    i+=1
                listofelements.append(expr[begin-1:end+1])
                #In case of the last element is a function
                if end==len(expr)-1:
                    expr=""
                else:
                    expr=expr[end+2:]
    return  listofelements


#unify two expressions, expr1 and expr2 are 2 lists of strings
def unify(expr1,expr2):
    #if one of the expression is an Atom
    if isAtom(expr1) or isAtom(expr2):
        return unifyAtoms(expr1,expr2)
    #get the first element from expr1
    f1=expr1[0]
    #save the rest
    del expr1[0]
    t1=expr1

    #get the first element from expr2
    f2=expr2[0]
    #save the rest
    del expr2[0]
    t2=expr2
    #---
    e1=[f1]
    e2=[f2]
    #unify the 2 first expressions from expr1 and expr2
    z1=unify(e1,e2)

    #if fail
    if z1=="FAIL":
        return "FAIL"

    #apply substitution on the rest of expr1 and expr2
    g1=substitute(t1,z1)
    g2=substitute(t2,z1)
    #unify the rest
    z2=unify(g1,g2)
    if z2=="FAIL":
        return "FAIL"
    return z1+" "+z2


#substitution of t1 by the unifier z1
def substitute(t1,z1):
    chg=z1.strip().split()
    tmp=[]
    for i in chg:
        tmp.append(i.split('/'))
    b=[]
    for i in tmp:
        for j in i:
            b.append(j)

    if not z1=="":
        for i in range(0,len(t1)):
            for j in range(0,len(b),2):
                t1[i]=t1[i].replace(b[j],b[j+1])
    return t1



#unify 2 atoms
def unifyAtoms(ex1,ex2):
    e1=ex1[0]
    e2=ex2[0]
    #e1 et e2 are the same
    if e1==e2:
        return ""
    #e1 variable
    if e1[0]=='?':
        #e2 contains e1 ==> FAIL
        if e1 in e2:
            return "FAIL"
        #otherwise
        return e1+"/"+e2
    #e2 variable
    if e2[0]=='?':
        return e2+"/"+e1
    #e1 and e2 2 functions
    if (('(' in e1) and ('(' in e2)):
        l1=expression(e1)
        l2=expression(e2)
        return unify(l1,l2)
    #else
    return "FAIL"

#read test cases
def readTC(filename):
    expressions=[]
    file=open(filename,"r")
    for testcase in file.read().split('\n'):
        expressions.append(testcase)
    return expressions





#------- TEST ---------
tracefile=open("trace.txt","w")
testcases=readTC("test_cases.txt")
i=1
for testcase in testcases:
    tracefile.write("****** TEST CASE N"+str(i)+"\n")
    exprs=testcase.split(':')
    expr1=exprs[0]
    expr2=exprs[1]
    tracefile.write("Expression 1: "+expr1+"\n")
    tracefile.write("Expression 2: "+expr2+"\n")
    tracefile.write("------- UNIFICATION -------- \n")
    tracefile.write(unify(expression(expr1),expression(expr2)))
    tracefile.write("\n\n")
    i+=1
tracefile.write("---- END TEST CASES ------\n")