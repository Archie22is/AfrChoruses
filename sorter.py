#!/usr/bin/env python

t = [('chap1', 9),('chap2', 13),('chap3', 6),('chap4', 12),('chap5', 9),('chap6', 10),('chap7', 17),('chap8', 14),('chap9', 14),('chap10', 14),('chap11', 10),('chap12', 8),('chap13', 4),('chap14', 11),('chap15', 22),('chap16', 19),('chap17', 12),('chap18', 17),('chap19', 16),('chap20', 9),('chap21', 12),('chap22', 9),('chap23', 26),('chap24', 7),('chap25', 7),('chap26', 12),('chap27', 7),('chap28', 10),('chap29', 8),('chap30', 12),('chap31', 10),('chap32', 18),('chap33', 14),('chap34', 12),('chap35', 12),('chap36', 7),('chap37', 19),('chap39', 8),('chap40', 17),('chap41', 7),('chap43', 16),('chap44', 16),('chap45', 17),('chap46', 27),('chap47', 17),('chap48', 22),('chap49', 13),('chap50', 14),('chap51', 11),('chap52', 14),('chap53', 46),('chap54', 28),('chap55', 37),('chap56', 28),('chap57', 22),('chap58', 22),('chap59', 27),('chap61', 27),('chap62', 27),('chap64', 12),('chap66', 9),('chap67', 11),('chap68', 15),('chap69', 20),('chap71', 13),('chap72', 24),('chap73', 17),('chap74', 16),('chap75', 29),('chap76', 10),('chap77', 18),('chap78', 26),('chap79', 12),('chap80', 6),('chap81', 11),('chap82', 27),('chap83', 32),('chap84', 5),('chap85', 9),('chap86', 12),('chap87', 15),('chap88', 32),('chap89', 30),('chap90', 26)]
# ,('chap', )
#('chap60', 17),('chap38', 13),('chap42', 18),('chap63', 32),('chap65', 33)

#,('chap964', 19),('chap965', 13),('chap966', 12),('chap967', 11),('chap968', 24)] # the wedding songs

pagesize = 38
badness=1
lockedup = 100
lockupcounter = 0
outofchaps=False

def fillpage(avchaps, lpp, invocation):
    """see which chap will fit on the current page
    it is entered with a list of available chapter-tuples and 
    the number of empty lines left on the current page.
    it calls itself when more chaps are needed to fill the page.
    When ripup is needed the list of available chapter-tuples is artificially decreased
    so that the next song is tried from the next available chap-tuple.
    it exits for 3 reasons:
    1. page is full (within the badness): return chap tuple.
    2. we found one but we have run out of available tuples : sets outofchaps flag and return chap tuple.
    3. tuples are available, but none fits : sets outofchaps flag and return none.
    """
    global outofchaps
    global badness
    page=[]
    nexthymn=[]
    chapsleft = copy.copy(avchaps)
    linesleft=lpp
    invocation = invocation +1
    print 'invocation = ',invocation, ';   linesleft = ', linesleft
    for i in avchaps:
        if i[1] % pagesize > linesleft:
            continue
        elif lpp - i[1] % pagesize < 0:
            continue
        else:
            #we found a hymn that fits
            linesleft = lpp - (i[1] % pagesize)
            if ((linesleft <= badness) and (linesleft >= 0)):
                #we are at the bottom of the page and the page is full
                page.append(i)
                print invocation,'-a-  ',
                print page
                return page
            else:
                chapsleft.remove(i)
                if chapsleft != []:
                    nexthymn = fillpage(chapsleft, linesleft, invocation)
                    if nexthymn == None:
                        #rip up this hymn and continue with the next one
                        print 'ripup'
                        continue
                    elif outofchaps==True and chapsleft > 1:
                        #ran out of tuples on the lower level
                        l = 0
                        for k in nexthymn:
                            l = l + k[1]
                        if linesleft - l > badness:
                            # but the page is not full
                            print invocation, 'lower level material shortage'
                            return None
                        else:
                            # notto worry the page is full anyway
                            page.append(i)
                            page.extend (nexthymn)
                            print invocation,'-b-  ',
                            print page
                            return page
                    else: 
                        #this page has worked, we are on the way back up
                        page.append(i)
                        page.extend (nexthymn)
                        print invocation,'-c-  ',
                        print page
                        return page
                else:
                    #ran out of tuples==========================
                    outofchaps=True
                    page.append(i)
                    print invocation,'-d-  ',
                    print page
                    return page
    else:
        #ran out of tuples
        outofchaps=True
        print invocation, 'material shortage'
        return None

def fillsbook(avchaps, lpp):  
    """fill a book with chapters of various length
    in such a way that the pages are maximally filled.
    It is entered with a list of available chapters and lines per page.
    When ripup is needed the list of available chapter-tuples is artificially decreased
    so that the next new page is tried from the next available chap-tuple.
    A chapter may be bigger than a page but take care that is is the top chapter
    on a page after sorting. It should happen automatically but there are conditions where
    this will not work!
    There is a lockup prevention mechanism incase the sorting start to oscillate.
    After the 1st page gets ripped up because fitting problems,
    the badness will be increased and the process will run again.
    """
    global badness
    global outofchaps
    outofchaps=False
    global lockupcounter
    global lockedup
    book = []
    nextpage=[]
    chapsleft = copy.copy(avchaps)
    cavchaps = copy.copy(chapsleft)   
    while outofchaps == False:
        nextpage = fillpage(cavchaps, lpp, 0)
        if nextpage != None:
            # it will go as long as it goes
            book.append(nextpage)
            for i in nextpage:
                chapsleft.remove(i)
            lockupcounter = lockupcounter - 2
            print '+1 page'
        else:
            while book != [] and lockupcounter < lockedup:
                print 'lockupcounter = ',lockupcounter
                print '=======================================badness = ',badness
                # then keep on ripping up a page and retying
                outofchaps=False
                lastpage = book.pop()
                for i in lastpage:
                    chapsleft.append(i)
                lockupcounter = lockupcounter + 1
                print '-1 page'
                cavchaps = copy.copy(chapsleft)
                while outofchaps == False:
                    cavchaps.pop()
                    nextpage = fillpage(cavchaps, lpp, 0)
                    if nextpage == None:
                        continue
                    else:
                        book.append(nextpage)
                        for i in nextpage:
                            chapsleft.remove(i)
                        lockupcounter = lockupcounter + 1
                        print '+1 retried page'
                        break
                else:
                    continue
                break
            else:
                badness = badness + 1
                lockupcounter = 0
                book = []
                chapsleft = copy.copy(avchaps)
        cavchaps = copy.copy(chapsleft)
        if cavchaps != []:
            outofchaps=False
            continue
        else:
            break
    print book
    return book

def printbook(book):
    """ Prints the book as a component ready for tex
    """
    i = []
    j = []
    f = open('sorted.tex', 'w')
    for i in reversed(book):
        for j in i:
            f.write ('\component ')
            f.write (str(j[0]))
            f.write('\n')
            f.write ('\\vfill')
            f.write('\n')
        f.write ('\page')
        f.write('\n')
#    f.write ('\midaligned{------ THE END ------}')
#    f.write('\n')
    f.close()
                   
if __name__ == "__main__":
    import sys
    import copy
    global t
    # biggest chapters first, makes life easier!
    t.sort(lambda x,y: cmp(y[1],x[1]))
    thisbook = fillsbook (t, pagesize)
    printbook (thisbook)
    print '\n done, badness was: ', badness, '\n'
#the end
