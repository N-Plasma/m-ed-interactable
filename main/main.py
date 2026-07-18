from pyscript import when, web, display, document
import time

validnum = ['-','0','1','2','3','4','5','6','7','8','9']
validdecode = ['|','0','1','2','3','4','5','6','7','8','9']

def display_regular(input, clr=None, bld:bool=False):
    if input != None:
        div = document.getElementById('output')
        if not clr and bld == False:
            div.innerHTML = f'<span>{input}</span>'
        elif not clr and bld == True:
            div.innerHTML = f"<span style='font-weight:bold;'>{input}</span>"
        elif clr and not bld:
            div.innerHTML = f"<span style='color: {clr};'>{input}</span>"
        elif clr and bld == True:
            div.innerHTML = f"<span style='color: {clr};font-weight:bold;'>{input}</span>"

def display_error(input):
    if input != None:
        div = document.getElementById('output')
        div.innerHTML = f"<span style='font-weight:bold;color: #FF5733;'>{input}</span>"
        time.sleep(2.5)
        display_regular('Awaiting Output...')

def encdec(mode,input,mod):
    if mode != None and input != None and mod != None:

        if mode == 0 and mod == 0:
            
            roughout = ''.join(str(ord(c)) for c in input)
            if roughout != None:
                output = roughout
            else:
                return(False)
        
        elif mode == 0 and mod != 0:
            
            roughout = '|'.join(str(ord(c)*mod) for c in input)
            if roughout != None:
                output = roughout
            else:
                return(False)

        elif mode == 1:

            parts = [p for p in input.split("|") if p]
            try:
                nums = [int(p) for p in parts]
            except ValueError:
                return(False)

            try:
                chars = [chr(n // mod) for n in nums]
            except Exception:
                return(False)

            roughout = "".join(chars)
            if isinstance(roughout, str) and roughout != None:
                output = roughout
            else:
                return(False)

        else:
            return(False)
        
    else:
        return(False)
    
    if output != None:
        return(output)
    else:
        return(False)

def inout(mode,keymode,key,input):
    if mode and keymode and key and input:
        
        if keymode == 'Ascii':
            keyref = encdec(0,key,0)
        elif keymode == 'Direct':
            keyref = int(key)
        else:
            ValueError
        
        if mode == 'Encode':
            output = encdec(0,input,keyref)
            display_regular(output)
        elif mode == 'Decode':
            output = encdec(1,input,keyref)
            display_regular(output)
        else:
            ValueError

display_regular('Awaiting Input...','limegreen',True)
time.sleep(0.5)
start = document.querySelector("#start-button")
start.removeAttribute("disabled")
time.sleep(0.024)
upl = document.querySelector("#upl")
upl.removeAttribute("disabled")

@when("click", "#start-button")
def handle_click(event):
    
    keyin = web.page['key']
    keyref = keyin.value
    textin = web.page['input']
    textref = textin.value
    
    if not keyref:
        display_error('Key Cannot be blank')
    else:
        if not textref:
            display_error('Input Cannot be blank')
        else:
            modeunr = document.querySelector("input[name='mode']:checked")
            keymodeunr = document.querySelector("input[name='keymode']:checked")

            mode = modeunr.value
            keymode = keymodeunr.value
            
            if keymode == 'Ascii':
                try:
                    keyref.encode('ascii')
                except Exception:
                    display_error('Key Must be ACSII only in current mode')
                else:
                    display_regular('Processing Inputs...')
                    inout(mode,keymode,keyref,textref)
            
            elif keymode == 'Direct':
                if all(c in validnum for c in keyref) == False:
                    display_error('Key Must be Numbers only in current mode')
                elif keyref.startswith('-0'):
                    display_error('Key Must not start with -0 in current mode')
                    display_regular('Processing Inputs...')
                    if mode == 'Decode' and all(c in validdecode for c in textref) == False:
                        display_error('Invalid Characters for Decode')
                    else:
                        inout(mode,keymode,keyref,textref)