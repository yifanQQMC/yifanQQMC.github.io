import os

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
                print(f'{red}错误:缺少文件名{clear}')
                return
            # Ensure 'disk' directory exists
            os.makedirs('disk', exist_ok=True)
            filepath = os.path.join('disk', spl[1])
            with open(filepath, 'w', encoding='utf-8') as f:
                if len(spl) > 2:
                    f.write(' '.join(spl[2:]))  # 可选：支持创建文件时直接写入内容
            if os.path.exists(filepath):  # 修复：此判断应在with块外部
                print(f"{green}成功建立文件: {filepath}{clear}")
            else:
                print('失败')
        elif spl[0] == 'del':
            if len(spl) < 2:
                print(f'{red}错误：缺少文件名{clear}')
                return
            filepath = os.path.join('disk', spl[1])
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"{green}成功删除: {filepath}{clear}")
            else:
                print(f"{red}文件不存在: {filepath}{clear}")
        elif spl[0] == 'read':
            if len(spl) < 2:
                print(f'{red}错误：缺少文件名{clear}')
                return
            filepath = os.path.join('disk', spl[1])
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"文件 {spl[1]} 的内容:")
                    print(content,f'{clear}')
            else:
                print(f"{red}文件不存在: {filepath}{clear}")
        elif spl[0] == 'change':
            if len(spl) < 3:
                print(f'{red}错误：缺少文件名或新内容{clear}')
                return
            filepath = os.path.join('disk', spl[1])
            if os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(' '.join(spl[2:]))
                print(f"{green}成功更改文件 {spl[1]} 的内容{clear}")
            else:
                print(f"{red}文件不存在: {filepath}{clear}")
        elif spl[0] == 'run':
            try:
                # 修复：os.system参数拼接问题，避免路径和文件名之间没有分隔符
                file_to_run = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'disk', ' '.join(spl[1:]))
                os.system(f'start "" "{file_to_run}"')
                print(f'{green}成功打开文件{clear}')
            except Exception as e:
                print(f"{red}打开出现问题：{e}{clear}")
        elif spl[0] == 'help':
            print(f"""{blue}
                    ---------command---------
                          print [output]
                      new [file_name] [write]
                      del [delect_file_name]
                       read [read_file_name]
                change [change_file_name] [new_input]
                       run [run_file_name]
                         help_chinese
                              help
                        python [file]{clear}""")
        elif spl[0] == 'help_chinese':
            print(f"""{blue}
                     print text              输出
                     new file value          建立文件
                     del file                删除文件
                     read file               读取文件
                     change file value       重写内容
                     run                     第三方软件
                     help_chinese            技术帮助
                     python file             运行Python文件{clear}""")
        elif spl[0] == 'python':
            try:
                with open('disk\\' + ' '.join(spl[1:]), 'r', encoding='utf-8') as f:
                    content = ''.join(f.readlines())  # 一次性读取所有行并拼接
                    print('\n')
                print (' '.join(spl[1:]),f'{clear}')
                print (' '.join(spl[1:]),f'{clear}')
                print(f'{blue}----------------------------------------------------------------------------{clear}')
                exec(content)
                print(f'{blue}----------------------------------------------------------------------------{clear}\n\n')
            except Exception as e:
                print(f"{red}出现问题:{e}{clear}")
        elif spl[0] == 'IDE':
            os.system("start PIDE.py")
        elif spl[0] == '':
            print('')
        else:
            print(f'{red}未知命令{clear}')
    except Exception as e:
        print(f"{red}出现问题: {e}{clear}")

if is_try_run:
    run(input())

# print text             输出
#new file value          建立文件
#del file                删除文件
#read file               读取文件
#change file value       重写内容
#run                     第三方软件
#help                    技术帮助
#QQ 3678869403(3852558256)  有bug欢迎上报
#python 3.11
version = 'consoleOS v1.1'
data = '2025/7/3'

#启动
print(f"{blue}{version}{clear}")
print(f"{blue}{data}{clear}")
while True:
    run(input(f'{yellow}>>> '))