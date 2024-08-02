import streamlit as st
#from sympy import symbols, Eq, solve
from fractions import Fraction
from itertools import combinations, chain


def solve_linear_equation(a, b, c):
    # Calculate the coefficient of x
    coefficient = b + 2 * c

    # Check if coefficient is zero to avoid division by zero
    if coefficient == 0:
        raise ValueError("Coefficient is zero; equation has no unique solution.")

    # Solve for x
    x = (1 - a) / coefficient
    return x


st.title('Islamisk fordeling af arv')

# User input for gender
køn = st.radio(
    'Hvad er dit køn?',
    options=['Mand', 'Kvinde']
)

# User input for marital status
gift = st.radio(
    'Er du gift?',
    options=['Ja', 'Nej']
)

# User input for dad
far = st.radio(
    'Er din far i live?',
    options=['Ja', 'Nej']
)

# User input for mum
mor = st.radio(
    'Er din mor i live?',
    options=['Ja', 'Nej']
)

# User input for number of sons
N_sønner = st.number_input(
    'Hvor mange sønner har du?',
    min_value=0,
    value=0
)

# User input for number of daughters
N_døtre = st.number_input(
    'Hvor mange døtre har du?',
    min_value=0,
    value=0
)

    


elements = []

if far.lower() == 'ja':
    elements.append('Far')
    
if mor.lower() == 'ja':
    elements.append('Mor')
    
if gift.lower() == 'ja' and køn.lower() == 'mand':
    elements.append('Kone')
    
elif gift.lower() == 'ja' and køn.lower() == 'kvinde':
    elements.append('Mand')
    
N_børn = N_sønner + N_døtre



D = {}

for e in elements:
    D[e]=0
for i in range(N_sønner):
    key = 'Søn %s' % (i+1)
    D[key]=0
for j in range(N_døtre):
    key = 'Datter %s' % (j+1)
    D[key]=0
    
    
# Hvis der ingen børn er        
if N_børn == 0:  
    if 'Kone' in elements:
        D['Kone'] += 1/4      
    
    Rest = 1-sum(D.values())
    if 'Far' in elements and 'Mor' in elements:
        D['Far'] += 2/3*Rest
        D['Mor'] += 1/3*Rest
    elif 'Far' in elements and 'Mor' not in elements:    
        D['Far'] += Rest
    elif 'Mor' in elements and 'Far' not in elements:    
        D['Mor'] += Rest

# Hvis der er børn
else:
    
    if 'Kone' in elements:
        D['Kone'] += 1/8
    
    if 'Mor' in elements:
        D['Mor'] += 1/6
              
    if 'Far' in elements:
        D['Far'] += 1/6


    # Hvis der er sønner og evt. døtre, skal sønner hver have 2x mere end døtre:
    if N_sønner > 0:      
        t = sum(D.values())   
        

        # Solve the equation
        x = solve_linear_equation(t, N_døtre, N_sønner)


        for elem in D:
            if 'Søn' in elem:
                D[elem]=2*x
            if 'Datter' in elem:
                D[elem]=x
                
    # Hvis der kun er døtre, skal de dele 1/2
    # Og hvis der er en far, skal han så have resten
    # Og hvis ingen far, men mor, skal døtre dele 3/4 og mor får 1/4
    # Og hvis der heller ingen mor er, får døtre resten
    elif N_døtre>0:
        hver = 0.5/N_døtre
        for elem in D:
            if 'Datter' in elem:
                D[elem]=hver
        Rest = 1-sum(D.values())
        if 'Far' in elements:
            D['Far'] += Rest
        elif 'Mor' in elements:
            D['Mor'] += 1/4*Rest
            hver2 = 3/4*Rest/N_døtre
            for elem in D:
                if 'Datter' in elem:
                    D[elem]+=hver2
        else:
            hver3 = Rest/N_døtre
            for elem in D:
                if 'Datter' in elem:
                    D[elem]+=hver3

# Hvis der kun er én kone, mor eller far:    
if len(elements) == 1 and N_børn == 0:
    D[elements[0]] = 1
    
# Hvis der kun er ét barn
elif len(elements) == 0 and N_børn == 1:
    D[[x for x in D][0]] = 1

for element in D:
    st.write('%s:  %s el. %s%%' % (element,Fraction(D[element]).limit_denominator(100),round(D[element]*100,3)))

st.write('')
if N_sønner>0:
    vals_sønner = [D[key] for key in D.keys() if 'Søn' in key]
    st.write('Sønner samlet: %s%%' % (round(100*sum(vals_sønner),3)))
if N_døtre>0:
    vals_døtre = [D[key] for key in D.keys() if 'Datter' in key]
    st.write('Døtre samlet: %s%%' % (round(100*sum(vals_døtre),3)))
if 'Far' in elements or 'Mor' in elements:
    vals_forældre = [D[key] for key in D.keys() if 'Far' in key or 'Mor' in key]
    st.write('Forældre samlet: %s%%' % (round(100*sum(vals_forældre),3)))
    
st.write('Sum total: %s%%' % (round(sum(D.values())*100,3)))