import random
#========================================================================
def normList(L, normalizeTo=1):
    '''normalize values of a list to make its max = normalizeTo'''

    vMax = max(L)
    return [ x/(vMax*1.0)*normalizeTo for x in L]
#========================================================================
def findIndex(sortedList, x, indexBuffer=0):
  ''' Given a sortedList and value x, return the index i where
      sortedList[i-1] <= x < sortedList[i]

      Which means,
        sortedList.insert( findIndex(sortedList, x), x )
      will give a sorted list  
  '''

  if len(sortedList)==2:
    
    if x==sortedList[-1]:   return indexBuffer+2
    elif x>=sortedList[0]:  return indexBuffer+1

  else:
    L = len(sortedList)  
    firstHalf  = sortedList[:L/2+1]
    secondHalf = sortedList[(L/2):]

    if secondHalf[-1]<=x:
      return indexBuffer + len(sortedList)
    elif x< firstHalf[0]:
      return indexBuffer
    else:
      if firstHalf[-1] < x:
        return findIndex(secondHalf, x, indexBuffer=L/2+indexBuffer)
      else:
        return findIndex(firstHalf,x, indexBuffer=indexBuffer)

#========================================================================
def deepList(LString):
    '''
    Given string representation of a nested list tree,
    return a list containing all the deepest list contents.

    For example:

    '[[1,[2, 2a]],[[3,3b],4]]'
    ==> ['2, 2a', '3,3b']

    '[[[1,[2, 2a]],[[3,3b],4]],6]'
    ==> ['2, 2a', '3,3b']

    '[[[[a1,a2],out],o1],[o2,o3]]'
    ==> ['a1,a2', 'o2,o3']

    '[[[[[a1,a2], out], [o1,o2]],[o3,o4]],[o5,o6]]'
    ==> ['a1,a2', 'o1,o2', 'o3,o4', 'o5,o6']

    The code: [x.split(']') for x in code.split('[')]
    returns something like:
    [[''], [''], [''], [''], [''], ['a1,a2', ', out', ', '],
    ['o1,o2', '', ','], ['o3,o4', '', ','], ['o5,o6', '', '']]

    '''
    result= [x[0] for x in \
            [x.split(']') for x in LString.split('[')] \
            if len(x)>1]
    if result==['']: result =[]
    return result


#========================================================================
def getListStartsWith(aList, startsWith, isStrip=1):
    ''' for a list:   L= ['abcdef', 'kkddff', 'xyz', '0wer'...],

        getListStartWith(L, 'kk') will return:
           ['kkddff', 'xyz', '0wer'...],

        getListStartWith(L, 'xy') will return:
           ['xyz', '0wer'...],

        if isStrip: any item '  xyz' will be considered 'xyz'
        else:       the spaces in '  xyz' count.
           
    '''
    tmp = aList[:]
    if isStrip: tmp = [x.strip() for x in tmp]
    startLineIndex = 0
    for i in range(len(tmp)):
        if tmp[i].startswith(startsWith):
            startLineIndex = i
    return aList[startLineIndex:]

#========================================================================
def rezip(aList):
    ''' d = [[1, 5, 8, 3], [2, 2, 3, 9], [3, 2, 4, 6]]
        rezip(d):
        [(1, 2, 3), (5, 2, 2), (8, 3, 4), (3, 9, 6)]

    If a =[1, 5, 8], b=[2, 2, 3], c=[3, 2, 4]
    then it's eazy to: zip(a,b,c) = [(1, 2, 3), (5, 2, 2), (8, 3, 4)]

    But it's hard for d = [[1, 5, 8], [2, 2, 3], [3, 2, 4]]    
    '''

    tmp = [ [] for x in range(len(aList[0])) ]
    for i in range(len(aList[0])):
        for j in range(len(aList)):
            tmp[i].append(aList[j][i])
    return tmp