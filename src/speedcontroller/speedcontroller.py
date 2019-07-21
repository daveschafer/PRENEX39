##Libraries##
import mc_communication as mc

def main():
  print("="*50)
  print("Speed Controller Started")
  print("="*50)
  print("="*50)
  print()
  helper()
  print("*******************************")
  print("Init MC Connection")
  initMC()
  print("*******************************")
  commandInterpreter()


def helper():
    print("Folgende Commandos stehen zur verfuegung:\n \
      help - Hilfsmenu\n \
      init - Kommunikation zu MC starten (nach Stromunterbruch) \n \
      speedcustom x - Speed Prozentual setzen (0...100) \n \
      speed01 - Set Speed 1 \n \
      speed02 - Set Speed 2 \n \
      speed03 - Set Speed 3 \n \
      speed04 - Set Speed 4 \n \
      stop - Stopt den Motor Sofort \n \
      rollup - Seilwinde auf \n \
      rolldown - Seilwinde ab \n \
      loadup - Aufladeprozess Kran starten \n \
      getticks - Ticks vom Linesensor abfragen \n \
      status - get current MC status \n \
                   ")
    print("-"*45)


def commandInterpreter():
    print("-"*50)
    commandinput = input("Please enter command (q to quit): ")
    parseCommand(commandinput)

def initMC():
    #send mc command
    mc.preempt_serial_buffer()
    return


def parseCommand(commandinput):

    
    if (commandinput == "help"):
        print("[Command] help called")
        helper()
        return commandInterpreter()
    
    if (commandinput == "stop"):
        print("[Command] stop called")
        mc.uart_send_stop()
        return commandInterpreter()

    if (commandinput == "speed01"):
        print("[Command] speed01 called")
        mc.uart_send_speed01()
        return commandInterpreter()

    if (commandinput == "speed02"):
        print("[Command] speed02 called")
        mc.uart_send_speed02()
        return commandInterpreter()

    if (commandinput == "speed03"):
        print("[Command] speed03 called")
        mc.uart_send_speed03()
        return commandInterpreter()

    if (commandinput == "speed04"):
        print("[Command] speed04 called")
        mc.uart_send_speed04()
        return commandInterpreter()

    if (commandinput == "rollup"):
        print("[Command] rollup called")
        mc.uart_send_rollUp()
        return commandInterpreter()

    if (commandinput == "rolldown"):
        print("[Command] rolldown called")
        mc.uart_send_rollDown()
        return commandInterpreter()

    if (commandinput == "getticks"):
        print("[Command] getticks called")
        mc.uart_get_ticks()
        return commandInterpreter()

    if (commandinput == "status"):
        print("[Command] status called")
        mc.uart_get_mc_status()
        return commandInterpreter()

    if (commandinput == "loadup"):
        print("[Command] loadup called")
        mc.uart_send_auflademodus()
        return commandInterpreter()

    if (commandinput == "init"):
        print("[Command] init called")
        initMC()
        return commandInterpreter()


    if (commandinput == "q"):
        print("Quit Program")
        exit()
    
    ##check for speedcustom:
    if (find_text(commandinput,"speedcustom") > -1):
        print("[Command] speedcustom called")
        customspeed = commandinput.split(" ", 1)
        try:
            customspeed = customspeed[1]
            mc.uart_send_speedcustom(customspeed)
        except:
            print("Please set customspeed!")
            commandInterpreter()
        print("Customspeed: %s"%customspeed)
        return commandInterpreter()

    else:
        print("Not a valid command")
        commandInterpreter()

    

#Returns -1 if not found and position Integer (between 0 and endless) if found
def find_text(text, searchword):
    return text.find(searchword)

if __name__== "__main__":
  main()