# -*- coding: utf-8 -*-
import os
import sys

is_try_run = 0

##################################################
red = ""
yellow = ""
green = ""
blue = ""
clear = ""
##################################################
def run(encode):
    try:
        spl = encode.split(' ')
        if spl[0] == 'print':
            print(' '.join(spl[1:]))
        elif spl[0] == 'new':
            if len(spl) < 2:
                print(f'{red}error!{clear}')
                return
            # Ensure 'disk' directory exists
            os.makedirs('disk', exist_ok=True)
            filepath = os.path.join('disk', spl[1])
            with open(filepath, 'w', encoding='utf-8') as f:
                if len(spl) > 2:
                    f.write(' '.join(spl[2:]))
            if os.path.exists(filepath):
                print(f"{green}finish!{filepath}{clear}")
            else:
                print('error!')
        elif spl[0] == 'del':
            if len(spl) < 2:
                print(f'{red}error!{clear}')
                return
            filepath = os.path.join('disk', spl[1])
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"{green}del finish! {filepath}{clear}")
            else:
                print(f"{red}error:file is not in {filepath}{clear}")
        elif spl[0] == 'read':
            if len(spl) < 2:
                print(f'{red}error!{clear}')
                return
            filepath = os.path.join('disk', spl[1])
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"{spl[1]} content:")
                    print(content,f'{clear}')
            else:
                print(f"{red}error:file is not in {filepath}{clear}")
        elif spl[0] == 'change':
            if len(spl) < 3:
                print(f'{red}error!{clear}')
                return
            filepath = os.path.join('disk', spl[1])
            if os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(' '.join(spl[2:]))
                print(f"{green}{spl[1]}change finish!{clear}")
            else:
                print(f"{red}error:file is not in {filepath}{clear}")
        elif spl[0] == 'run':
            try:
                file_to_run = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'disk', ' '.join(spl[1:]))
                os.system(f'start "" "{file_to_run}"')
                print(f'{green}finish!{clear}')
            except Exception as e:
                print(f"{red}error:{e}{clear}")
        elif spl[0] == 'help':
            print(f"""{blue}
                    ---------command---------
                          print [output]
                      new [file_name] [write]
                      del [del_file_name]
                       read [read_file_name]
                change [change_file_name] [new_input]
                       run [run_file_name]
                              help
                        python [file]
                              exit{clear}""")

        elif spl[0] == 'python':
            try:
                with open('disk\\' + ' '.join(spl[1:]), 'r', encoding='utf-8') as f:
                    content = ''.join(f.readlines())
                    print('\n')
                print (' '.join(spl[1:]),f'{clear}')
                print (' '.join(spl[1:]),f'{clear}')
                print(f'{blue}----------------------------------------------------------------------------{clear}')
                exec(content)
                print(f'{blue}----------------------------------------------------------------------------{clear}\n\n')
            except Exception as e:
                print(f"{red}error:{e}{clear}")
        elif spl[0] == 'IDE':
            os.system("start D:\ConsoleOS\Disk\PIDE.exe")
        elif spl[0] == 'exit':
            print('exit!')
            sys.exit()
        elif spl[0] == '':
            print('')
        else:
            print(f'{red}error!{clear}')
    except Exception as e:
        print(f"{red}error:{e}{clear}")

if is_try_run:
    run(input())
version = 'consoleOS v1.1'
data = '2025/7/3'


print(f"{blue}{version}{clear}")
print(f"{blue}{data}{clear}")
while True:
    run(input(f'{yellow}>>> '))
