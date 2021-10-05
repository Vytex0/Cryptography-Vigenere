from math import *

# Cette fonction transforme un dictionnaire en une liste de couples (clé, valeur) triée par ordre croissant
def sortDictionnaryToList(dictionnary):
    marklist = sorted(dictionnary.items(), key=lambda x:x[1])
    return marklist

# Cette fonction renvoie la liste des diviseurs d'un nombre entier
def getListDividers(nb):
    dividers = []
    for i in range(1, int(sqrt(nb)+1)):
        if(nb%i == 0):
            dividers.append(i)
    return dividers

# Cette fonction prend en paramètres un texte (text) et une taille de syllabe (syllableSize) et renvoie un dictionnaire contenant toutes les syllabes avec leur nombre d'apparitions dans le texte
def getListRepetitions(text, syllableSize):
    repetitionsSyllables = {}
    for i in range(len(text)-syllableSize+1):
        syllable = ""
        for j in range(syllableSize):
            syllable = syllable + text[i+j]
        # On enregistre toutes les suites de caractères de taille syllableSize
        repetitionsSyllables[syllable] = repetitionsSyllables.get(syllable, 0)+1
    return repetitionsSyllables

# Cette fonction renvoie la liste de toutes les syllables les plus présentes dans le texte
# Algo : on recherche la répétition de caractères la plus présente et on récupères toutes les répétitions qui sont apparues au moins 70% de fois autant que la répétition la plus présente
def getMostRepeatedSyllables(sortedRepetitions):
    mostRepeatedSyllables = []
    (bestRep, nbBestRep) = sortedRepetitions[-1]
    minRep = nbBestRep*0.7
    for e in sortedRepetitions:
        (syllable, rep) = e
        if(rep >= minRep):
            mostRepeatedSyllables.append(syllable)
    return mostRepeatedSyllables

# Cette fonction renvoie la liste des différentes positions d'une syllabe donnée dans le texte
def getListPositionSyllables(text, syllableToFind):
    syllableSize = len(syllableToFind)
    positions = []
    for i in range(len(text)-syllableSize+1):
        syllable = ""
        for j in range(syllableSize):
            syllable = syllable + text[i+j]
        if(syllable == syllableToFind):
            positions.append(i)
    return positions

# Cette fonction renvoie le dictionnaire de tous les diviseurs possibles (selon la différence entre les positions de mêmes répétitions) avec leur nombre d'apparitions
def getListDividersPossibility(text, syllableSize):
    allDividers = {}
    for syllable in getMostRepeatedSyllables(sortDictionnaryToList(getListRepetitions(text, syllableSize))):
        allPositionsOfSyllable = getListPositionSyllables(text, syllable)
        for i in range(len(allPositionsOfSyllable)-1):
            for divider in getListDividers(allPositionsOfSyllable[i+1]-allPositionsOfSyllable[i]):
                if(divider > 1):
                    allDividers[divider] = allDividers.get(divider, 0)+1
    return sortDictionnaryToList(allDividers)

# Cette fonction détermine la taille de la clé du texte chiffré fournie en paramètre
# Algo : pour toutes les longueurs de syllabl
def getKeyLength(text):
    pursue = True
    syllableSize = 2
    topPositions = {}
    # Tant qu'on trouve des répétitions, on augmente la taille des répétitions à chercher
    while(pursue):
        dividersList = getListDividersPossibility(chiffre, syllableSize)
        
        # On enregistre les diviseurs trouvés
        if(len(dividersList) >= 1):
            (divider, _) = dividersList[-1]
            topPositions[divider] = topPositions.get(divider, 0)+1
            syllableSize+=1
        else:
            pursue = False
    (divider, nbTopPos) = sortDictionnaryToList(topPositions)[-1]
    return divider

# Cette fonctione retourne un dictionnaire (de taille K, K étant la longueur de la clé) de liste de couples (lettre, nb répétitions de la lettre) dans le chacun des sous-textes
def getLetterRepetitionsByGap(text, keyLength):
    lenText = len(text)

    letterRepetitionsByGap = {}
    for keyPlaceInText in range(lenText//keyLength):
        for posInKey in range(keyLength):
            pos = keyPlaceInText*keyLength+posInKey
            if(pos < lenText):
                letter = chiffre[pos]
                gapDict = letterRepetitionsByGap.get(posInKey, {})
                gapDict[letter] = gapDict.get(letter, 0)+1
                letterRepetitionsByGap[posInKey] = gapDict

    for posInKey in range(keyLength):
        letterRepetitionsByGap[posInKey] = sortDictionnaryToList(letterRepetitionsByGap[posInKey])

    return letterRepetitionsByGap

# Cette fonction renvoie une liste de couple (lettre, nb répétitions) dans un texte normal (afin de récupérer la lettre la plus présente dans un texte d'une certaine langue)
def getLetterRepetitionsInText(text):
    repetitions = {}
    text = text.lower()
    for letter in text:
        if letter in "abcdefghijklmnopqrstuvwxyz":
            repetitions[letter] = repetitions.get(letter, 0)+1
    return sortDictionnaryToList(repetitions)

# Cette fonction renvoie la liste des clés à partir d'un dictionnaire de couple (clé, valeur)
def listCoupleToKeyList(list):
    newList = []
    for couple in list:
        (key, val) = couple
        newList.append(key)
    return newList

# Cette fonction retourne la clé d'un texte chiffré en prenant un paramètre un texte dans la langue du texte chiffré ainsi que l'alphabet à utiliser
def findKey(chiffre, text_lang, alphabet):
    keyLength = getKeyLength(chiffre)

    letterRepetitionsInTextLang = listCoupleToKeyList(getLetterRepetitionsInText(text_lang))
    mostUsedLetter = letterRepetitionsInTextLang[-1]

    letterRepetitionsByGapInChiffre = getLetterRepetitionsByGap(chiffre, keyLength)

    key = ""

    for i in range(keyLength):
        letterRepetitionsInGap = listCoupleToKeyList(letterRepetitionsByGapInChiffre[i])
        key = key + alphabet[(alphabet.index(letterRepetitionsInGap[-1]) - alphabet.index(mostUsedLetter)) % len(alphabet)]

    return key

# Cette fonction déchiffrer un chiffré en prenant en pamaètre le chiffré, la clé et l'alphabet
def dechiffrer(chiffre, key, alphabet):
    text = ""
    keyLength = len(key)

    for i in range(len(chiffre)):
        text = text + alphabet[(alphabet.index(chiffre[i]) - alphabet.index(key[i%keyLength]) % 26)]

    return text
            


chiffreFile = open("chiffré", "r")
chiffre = chiffreFile.readline().lower()
chiffreFile.close()

textFrFile = open("text_fr", "r")
textFr = textFrFile.readline().lower()
textFrFile.close()

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


print("La clé est : " + str(findKey(chiffre, textFr, ALPHABET)))

print("Le texte déchiffré est : \n" + dechiffrer(chiffre, findKey(chiffre, textFr, ALPHABET), ALPHABET))