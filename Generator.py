#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#Make sure that umlauts and so on are possible

if __name__ == '__main__':    
    #String for text to speech and number which is the name
    #Note that 48 to 58 and 65 to 91 is used for numerals and letters
    listOfStrings=[
    ("Test 1 2 3",0),
    ("Hello!",90)
    ]
    
    import os
    if not os.path.exists('output'):
        os.makedirs('output')
    os.chdir('output')
    
    #Add numerals as in ASCII
    for i in range(48,58):
        listOfStrings.append((str(i-48),i))
    
    #Add letters as in ASCII
    for i in range(65,91):
        #https://stackoverflow.com/questions/12797067/how-can-i-do-a-1-b-in-python
        listOfStrings.append((chr(ord('a') + i - 65),i))
    
    import pyttsx3    
    engine = pyttsx3.init()
    
    #Choose the right one for your machine and your language.
    #See https://stackoverflow.com/questions/65977155/change-pyttsx3-language
    #To find out the available voices:
    #for voice in engine.getProperty('voices'):
    #    print(voice) 
    
    engine.setProperty('voice',"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_DE-DE_HEDDA_11.0")
    
    codeString="#ifndef VOICEOUTPUTNUMBERS_H\n#define VOICEOUTPUTNUMBERS_H\n\n//Start: Autogenerated assignment of sound files\n"
    
    for name,number in listOfStrings:
        engine.save_to_file(name, str(number)+'.wav')
        
        #Skip code generation for numerals and letters.
        if 48<=number<58 or 65<=number<91:
            continue
        
        #Umlauts,� and !? can not be used in C-code.
        name=name.replace(" ","_")
        name=name.replace("�","ae")
        name=name.replace("�","oe")
        name=name.replace("�","ue")
        name=name.replace("�","ss")
        name=name.replace("!","")
        name=name.replace("?","")
        
        codeString=codeString+"#define " + name + " " + str(number) + "\n"
        
    codeString=codeString+"//End: Autogenerated assignment of sound files\n\n#endif /* VOICEOUTPUTNUMBERS_H */\n"
    
    with open("voiceOutputNumbers.h", "w") as f:
        f.write(codeString)
    
    engine.runAndWait()