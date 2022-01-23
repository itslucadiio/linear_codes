# BY LUCA DIIORIO

import numpy as np
import math
import random
import json

def createGeneratorMatrix(code):
    """
    Creates a Generator Matrix with the elements of the code in an array.
    """
    m = []
    for element in code:
        e = []
        for item in element:
            e.append(item)
        m.append(e)
    return m

def createMatrix(code):
    """
    Creates a Matrix from the element of an array.
    """
    m = []
    for element in code:
        e = []
        for item in element:
            e.append(item)
        m.append(e)
    return m

def checkOrder(matrix):
    """
    Returns a touple with the dimensions of the matrix. 
    This dimensions also correspond to the [n, k] of the parameters of a linear code.
    """
    r = (len(matrix[0]), len(matrix))
    return r

def matriuBuida(m, n):
    """
    Crea una matriu buida de dimensions m x n.
    """
    matrix = []
    for i in range(m):
        matrix = matrix + [[0] * n]
    return matrix

def deleteABase(base, n):
    """
    Given a base that has a generator matrix with (I | A), deletes the A part. 
    """
    new_base = []
    for element in base:
        new_base.append(element[:len(element) - n])
    return new_base

def deleteIBase(base, n):
    """
    Given a base that has a generator matrix with (I | A), deletes the I part.
    """
    new_base = []
    for element in base:
        new_base.append(element[n:])
    return new_base

def npArrayToMatrix(np):
    """
    Transforms a numpy array to a regular matrix.
    """
    ordre = checkOrder(np)
    r = matriuBuida(ordre[1], ordre[0])
    for i in range(len(np)):
        for j in range(len(np[0])):
            if np[i][j] == '1.0':
                r[i][j] = '1'
            elif np[i][j] == '0.0':
                r[i][j] = '0'
            else:
                r[i][j] = np[i][j]
    return r

def transposaMatriu(m):
    """
    Retorna la matriu resultant de canviar les files per les columnes de la
    matriu m.
    Retorna: np Array
    """
    arr1 = np.array(m)
    arr1_transpose = arr1.transpose()
    # result = npArrayToMatrix(arr1_transpose)
    # return result
    return arr1_transpose

def createVector(i):
    """
    Given an element i, creates a vector (vertical) [].
    """
    e = []
    for item in i:
        e.append([item])
    return e

def createArray(i):
    """
    Given an element i, creates an array (horizontal) [].
    """
    e = []
    for item in i:
        e.append(item)
    return e

def matrixStringToInt(matrix):
    """
    Returns the result of changing the data type from string to int of a matrix.
    """
    order = checkOrder(matrix)
    r = matriuBuida(order[1], order[0])
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == '1':
                r[i][j] = 1
            elif matrix[i][j] == '0':
                r[i][j] = 0
            else:
                r[i][j] = matrix[i][j]
    return r

def isSystematic(matrix, base):
    """
    Returns True if and only if the matrix is as (I | A). Otherwise returns False.
    """
    order = checkOrder(matrix)
    if order[0] > order[1]:
        identity = createGeneratorMatrix(deleteABase(base, (order[0]-order[1])))
        identity_order = checkOrder(identity)
        c = 0
        for i in range(len(identity)):
            for j in range(len(identity[0])):
                if identity[i][j] == "1":
                    c += 1
        if c == identity_order[0]:
            return True
    return False

def createControlMatrix(base):
    """
    Given a base which is SYSTEMATIC, returns the system control matrix.
    """
    generator_matrix = createGeneratorMatrix(base)
    order = checkOrder(generator_matrix)
    matriu_A = createGeneratorMatrix(deleteIBase(base, order[1]))
    transposada = transposaMatriu(matriu_A)
    identity = np.identity(len(transposada))
    control_matrix = np.hstack((transposada, identity))
    control_matrix = npArrayToMatrix(control_matrix)
    return control_matrix

def createGeneratorMatrixFromAMatrix(a_matrix, k):
    """
    Given a matrix A, part of the Generator matrix SYSTEMATIC (I | A), 
    returns the generator matrix.
    """
    a_matrix_int = matrixStringToInt(a_matrix)
    a_matrix_np = np.array(a_matrix_int)
    identity = np.identity(k)
    generator_matrix = np.hstack((identity, a_matrix_np))
    generator_matrix = generator_matrix.astype('str')
    generator_matrix = npArrayToMatrix(generator_matrix)
    return generator_matrix

def getBase(gMatrix):
    """
    Given a generator matrix, outputs the base in a more usable way. EX:
    base = ["10000110", "01001010", "00101110", "00011101"]
    """
    base = []
    for element in gMatrix:
        a = ""
        for item in element:
            a += str(item)
        base.append(a)
    return base


def pasToModulusTwo(matrix):
    """
    Returns the matrix resultant of changing its elements to modulus two.
    """
    ordre = checkOrder(matrix)
    r = matriuBuida(ordre[1], ordre[0])
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            r[i][j] = matrix[i][j] % 2
    return r

def calculateSyndrome(h, y):
    """
    Returns te matrix result of the calculus of the syndrome: s(y) = H*y.
    """
    h_int = matrixStringToInt(h)
    y_int = matrixStringToInt(y)
    # MULTIPLIQUEM
    c = np.array(h_int)
    d = np.array(y_int)
    result = np.dot(c, d)
    # CANVIA DE BASE
    syndrome = npArrayToMatrix(result)
    syndrome_mod = pasToModulusTwo(syndrome)
    return syndrome_mod

def createListOfErrors(base):
    """
    Given a base, returns a dictionary of possible errors of one bit.
    """
    list_of_errors = {}
    identity = np.identity(len(base[0]))
    control_matrix = createControlMatrix(base)
    for row in identity:
        e = ""
        for element in row:
            e += str(int(element))
        list_of_errors[e] = calculateSyndrome(control_matrix, e)
    return list_of_errors

def isSyndromeFromCode(s):
    """
    Given a syndrome s, return True if is part from the code, thus its equal to zero. 
    """
    counter = 0
    for i in range(len(s)):
        for j in range(len(s[0])):
            if s[i][j] == 1:
                counter += 1
    if counter == 0:
        return True
    return False

def lookForError(s, list_err):
    """
    Given a syndrome and a list of errors, looks for the error with the syndrome associated,
    and returns it.
    """
    for key, value in list_err.items():
        if value == s:
            return key
    return None

def correctError(y, e):
    """
    Given the original y and the error e, corrects and returns the result
    in modulus two.
    """
    result = ""
    for index,letter  in enumerate(y):
        result += str((int(letter)+int(e[index])) % 2)
    return result

def asciiToBinary(a):
    """
    ---------- FONT ENCODING -----------
    Converts an ascii string into a binary string.
    Returna an array of strings containing a string for each character input.
    EX: 01001000010011110100110001000001
    """
    l,m=[],[]
    for i in a:
        l.append(ord(i))
    for i in l:
        m.append('0' + bin(i)[2:])
    return m

def binaryToASCII(bin):
    """
    Binary to ascii converter. Returns a string. 
    """
    binary_int = int(bin, 2)
    byte_number = binary_int.bit_length() + 7 // 8
    binary_array = binary_int.to_bytes(byte_number, "big")
    ascii_text = binary_array.decode()
    return ascii_text

def stringify(input):
    """
    Given an array of strings, retuns a unique string.
    """
    r = ""
    for item in input:
        r = r + str(item)
    return r

def matrixStringify(input):
    """
    Given a matrix, stringifies it.
    """
    a = ""
    for element in input:
        for item in element:
            a += str(item)
    return a

def channelEncoding(fet, gen_matrix, k):
    """
    ---------- CHANNEL ENCODING -----------
    Given a font encoded text, a generator matrix, and a code parameter k,
    returns and array.
    EX: ['01001010', '10000110', '01001010', '11111111', '01001010', '11001100', '01001010', '00011101']
    """
    # divide fet into m blocs of length k (will be the last one of length n-k)
    temp_fet_arr=[fet[y-k:y] for y in range(k, len(fet)+k,k)]
    # create array for each bloc, so it can be multiplicated
    temp_fet_array = []
    for item in temp_fet_arr:
        temp_fet_array.append(createArray(item))

    result = []

    # channel encoding
    for element in temp_fet_array:
        h_int = matrixStringToInt([element])
        y_int = matrixStringToInt(gen_matrix)
        # MULTIPLIQUEM
        c = np.array(h_int)
        d = np.array(y_int)
        res = c.dot(d)
        # CANVIA DE BASE
        res_matrix = npArrayToMatrix(res)
        res_matrix_mod = pasToModulusTwo(res_matrix)
        # FORMATTER
        result.append(matrixStringify(res_matrix_mod))
    
    return result    

def checkErrorCorrect(control_matrix, cet, base, k, n):
    """
    ---------- RECEIVER BLOCK PART -----------
    Given a chanel encoded text message and a base which is SYSTEMATIC, k and n, checks if the message
    is part of the code and if not, trys to correct it. If it can correct, returns the corrected message.
    Retruns a JSON.
    """
    json_result = {
        'cet': cet,
        'syndrome': '',
        'from_code': '',
        'error': '',
        'corrected': cet,
        'original': '',
    }

    y_vector = createVector(cet)
    # control_matrix = createControlMatrix(base)
    syndrome = calculateSyndrome(control_matrix, y_vector)
    json_result['syndrome'] = str(matrixStringify(syndrome))
    if (isSyndromeFromCode(syndrome)):
        json_result['from_code'] = 'true'
    else:
        json_result['from_code'] = 'false'
        list_of_errors = createListOfErrors(base)
        error = lookForError(syndrome, list_of_errors)
        json_result['error'] = str(error)
        x = correctError(cet, error)
        json_result['corrected'] = str(x)

    json_result['original'] = removeRedundancy(json_result['corrected'], k, n)
    
    return json_result

def removeRedundancy(a, k, n):
    """
    Given a string of bytes a, removes the redundant part, preparing it for decoding.
    """
    remove = k-n
    new_string = a[:remove]
    return new_string

def generateNoiseString(n):
    """
    Given a length n, returns a string of lenth n with ONE bit 1 and the other 0 
    randomply sorted. 
    """
    s = []
    for i in range (n):
        s.append(str(1))
    a = random.randint(0, n-1)
    s[a] = str(0)
    s = matrixStringify(s)
    return s

def ANDGate(x, y):
    result = ""
    for i, element in enumerate(x):
        result += str(int(x[i])*int(y[i]))
    return result

def makeNoiseSequence(cet, n):
    """
    Given a chanel encodeg text cet, randomly generates a noise pattern to apply to the
    cet and simulate interferences during the transmision process.
    """
    noise_indicator = len(cet) - int(len(cet) / 2.5) # indicator for how many blocs have to be manipulated

    temp_cet = cet # make a copy of cet
    noise_masks = [] # arr to store noise masks
    for i in range(noise_indicator):
        noise_masks.append(generateNoiseString(n))

    # randomly define which message blocs will be manipulated
    index_array = []
    for i in range(noise_indicator):
        put = False
        while put==False:
            a=random.randint(0, n-1)
            if a not in index_array:
                index_array.append(a)
                put = True
    index_array= sorted(index_array)

    result = []
    for i, element in enumerate(temp_cet):
        if i in index_array:
            result.append(ANDGate(element, noise_masks[0]))
            noise_masks.remove(noise_masks[0])
        else:
            result.append(element)
    return result

def deltaAnalysys(cntMatrix, n, k):
    zero_threshold = n-k
    # convert into np matrix and transpose, to get matrix columns as rows
    # for easier analysis
    control_matrix_int = matrixStringToInt(cntMatrix)
    control_matrix_np = np.array(control_matrix_int)
    control_matrix_transposade = control_matrix_np.transpose()
    control_matrix_transposade = npArrayToMatrix(control_matrix_transposade)
    print(control_matrix_transposade)
    # create list 
    control_matrix_rows_list = []
    for element in control_matrix_transposade:
        b = ""
        for item in element:
            b += str(item)
        control_matrix_rows_list.append(b)

    # look for delta = 1 (column in H matrix = 0)
    for element in control_matrix_rows_list:
        if (element.count('0') == zero_threshold):
            return 1
    # look for delta = 2 (2 equal columns in H matrix)
    #stringify elements and append to list
    list_stringified = []
    for element in control_matrix_rows_list:
        list_stringified.append(matrixStringify(element))
    for i, element in enumerate(list_stringified):
        for j, element2 in enumerate(list_stringified):
            if (element == element2) and (i != j):
                print(element, " ", element2)
                return 2

    #else return 3
    return 3
        



def runLinearCode():
    """
    ---------- MAIN PROGRAM -----------
    Returns: JSON, json_result.
    """
    json_result = {
        'input_text': '',
        'g_systematic': '',
        'fet': '',
        'delta': '',
        'noise': 'false',
        'code_blocs': {},
        'decoded_text': '',
    }

    # Read params from JSON file
    with open("params.json") as json_data_file:
        data = json.load(json_data_file)
    
    # parameters ----------------
    n = int(data['code_length'])
    k = int(data['code_dimension'])
    input_text = str(data['input_text'])
    json_result['input_text'] = input_text

    a = createMatrix(str(data['a_matrix']).split(','))
    generator_matrix = createGeneratorMatrixFromAMatrix(a, k)
    base = getBase(generator_matrix)

    m_allow_noise = True if (int(data['noise']) == 1) else False
    # ---------------------------

    generator_matrix = createGeneratorMatrix(base)
    if (isSystematic(generator_matrix, base)):
        print("GENERATOR MATRIX SYSTEMATIC")
        json_result['g_systematic'] = 'true'
    else:
        print("GENERATOR MATRIX NOT SYSTEMATIC")
        json_result['g_systematic'] = 'false'

    # font encoding
    font_encoded_text = stringify(asciiToBinary(input_text))
    json_result['fet'] = font_encoded_text
    print(font_encoded_text)

    # channel encoding
    channel_encoded_text = channelEncoding(font_encoded_text, generator_matrix, k)
    print(channel_encoded_text)

    # SIMULATE TRANSMISSION
    if (m_allow_noise):
        json_result['noise'] = 'true'
        channel_encoded_text = makeNoiseSequence(channel_encoded_text, n)

    # control matrix creation and checking
    control_matrix = createControlMatrix(base)
    m_delta = int(deltaAnalysys(control_matrix, n, k))
    json_result['delta'] = str(m_delta)

    # error cheking and decoding
    decode_array = []
    for i, element in enumerate(channel_encoded_text):
        blocs_json = checkErrorCorrect(control_matrix, element, base, k, n)
        blocs_json['id'] = i
        json_result['code_blocs'][i] = blocs_json
        decode_array.append(blocs_json['original'])
        print(blocs_json)

    decoded_font_text = matrixStringify(decode_array)
    decoded_text = binaryToASCII(decoded_font_text)
    decoded_text= decoded_text.replace("\u0000", "")
    json_result['decoded_text'] = str(decoded_text)

    return json_result






        



    



# if __name__ == "__main__":

    # # parameters ----------------
    # n = 8
    # k = 4
    # input_text = "HOLA"
    # base = ["10000110", "01001010", "00101110", "00011101"]
    # m_allow_noise = True
    # # ---------------------------

    # # font encoding
    # font_encoded_text = stringify(asciiToBinary(input_text))
    # print(font_encoded_text)

    # generator_matrix = createGeneratorMatrix(base)
    # if (isSystematic(generator_matrix, base)):
    #     print("GENERATOR MATRIX SYSTEMATIC")
    # else:
    #     print("GENERATOR MATRIX NOT SYSTEMATIC")

    # # channel encoding
    # channel_encoded_text = channelEncoding(font_encoded_text, generator_matrix, k)
    # print(channel_encoded_text)

    # # SIMULATE TRANSMISSION
    # if (m_allow_noise):
    #     channel_encoded_text = makeNoiseSequence(channel_encoded_text, n)

    # # error cheking
    # for element in channel_encoded_text:
    #     json_result = checkErrorCorrect(element, base)
    #     print(json_result)

    # a = createMatrix('0110,1010,1110,1101'.split(','))
    # generator_matrix = createGeneratorMatrixFromAMatrix(a, 4)
    # base = getBase(generator_matrix)