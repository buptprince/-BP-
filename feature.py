from  PIL import Image
import numpy as np
def get_bin_table(threshold=140):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
 
    return table
image=Image.open('C:/Users/Li/Desktop/2.jpg')
image=image.resize((400,400))
imgry=image.convert('L')
table = get_bin_table()
out = imgry.point(table, '1')
out.show()
gdata=out.getdata()
gdata=np.array(gdata)
rdata=gdata.reshape(out.height,out.width)
data=np.matrix(rdata)
result=np.matrix(np.zeros([20,20]))
print(data)
for m in range(0,20):
    for n in range(0,20):
        z=0;
        for i in range(20*m,20*(m+1)):
            for j in range(20*n,20*(n+1)):
                if(data[i,j]==0):
                   z+=1;
        print(z)
        if(z>5):
             result[m,n]=1;
        else:
             result[m,n]=0;
print(result)

f=open('C:/Users/Li/Desktop/quizz.txt','a')


for p in range(0,20):
    for q in range(0,20): 
        f.write(str(result[p,q]))
        f.write('   ');
f.write('\n')
f.close()


        