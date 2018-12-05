

"""生成创建guest的sql脚本，为性能测试做准备"""

f = open('guests.txt', 'w')
for i in range(1, 3001):
    str_i = str(i)
    name = 'lisa' + str_i
    phone = 13812340000 + i
    email = 'lisa' + str_i + '@mail.com'
    sql = 'INSERT INTO sign_guest (real_name,phone,email,sign,event_id) ' \
          'VALUES("'+name+'",'+str(phone)+',"'+email+'",0,1);'
    f.write(sql)
    f.write('\n')
f.close()
