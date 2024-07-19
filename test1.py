#崩铁抽卡概率，简略版本，自测使用。2024-7-10
#-*-coding:utf-8-*- 
import io 
import sys 
import numpy as np 
import random 
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
import re
import matplotlib.pyplot as plt

def test1(golad_number):
    golddict={} # 定义出金的字典，记录抽数和大小保底情况。
    gold = 0 # 定义出金数量（包含歪了的）
    up = 0 # 定义当期up
    changzhu = 0 # 定义常驻出金
    bichu = False # 定义大小保底
    count = 0 # 定义保底抽数(90抽必出金)
    choushu = 0 # 定义抽取抽数
    for i in range(1,9000): # 循环多次，直到达到预期出金数。
      if up ==golad_number:
             choushu = i # 记录抽数
             break # 出金完毕，跳出循环
      count = count+1 # 保底抽数加1
      if count==90: # 90抽必出金
         # print("count = 90, 必出金！")
         gold = gold +1 # 出货，加1个金
         if bichu == True: # 大保底，加1个up金
            up = up+1
            bichu = False # 出货后，大小保底失效
            golddict[i] = "大保底"
            count = 0 # 保底抽数归零
            # print("恭喜你在"+str(i)+"抽究极大保底出up金了！")
            continue # 跳出本次循环，开始下一轮        
         elif bichu == False: # 小保底，50%概率出up
               j = random.randint(1,2) # 随机生成1或2，1为up，2为常驻
               if j==1:
                  up = up+1
                  golddict[i] = "小保底up金"
                  count = 0 # 保底抽数归零
                  # print("恭喜你在"+str(i)+"究极大保底小保底出up金了！")
                  continue # 跳出本次循环，开始下一轮     
               else:
                  changzhu = changzhu+1 # 出货后，常驻出金加1个
                  bichu = True # 出货后，大保底生效
                  golddict[i] = "常驻"
                  count = 0 # 保底抽数归零
                  # print("恭喜，你在究极大保底出常驻金了！")
                  continue # 跳出本次循环，开始下一轮
            
      chuhuolv = random.randint(1,1000) # 随机生成1-1000之间的数字,包含1和1000(这个版本不计算软概率提升情况)
      if chuhuolv<=6 : # 1-6点，出金1个,概率为0.6%      
         gold = gold+1 # 出货，加1个金
         if bichu == True: # 大保底，加1个up金
            up = up+1
            bichu = False # 出货后，大小保底失效
            golddict[i] = "大保底"
            count = 0 # 保底抽数归零
            # print("恭喜，你在第"+str(i)+"抽大保底出up金了！")

         elif bichu == False: # 小保底，50%概率出up
               j = random.randint(1,2) # 随机生成1或2，1为up，2为常驻
               if j==1:
                  up = up+1
                  golddict[i] = "小保底up金"
                  count = 0 # 保底抽数归零
                  # print("恭喜，你在第"+str(i)+"抽小保底出up金了！")
               else:
                  changzhu = changzhu+1 # 出货后，常驻出金加1个
                  bichu = True # 出货后，大保底生效
                  golddict[i] = "常驻"
                  count = 0 # 保底抽数归零
                  # print("恭喜，你在第"+str(i)+"抽出常驻金了！")
    return choushu;

def test2(golad_number):
    golddict={} # 定义出金的字典，记录抽数和大小保底情况。
    gold = 0 # 定义出金数量（包含歪了的）
    up = 0 # 定义当期up
    changzhu = 0 # 定义常驻出金
    bichu = False # 定义大小保底
    count = 0 # 定义保底抽数(90抽必出金)
    choushu = 0 # 定义抽取抽数
    for i in range(1,9000): # 循环多次，直到达到出金预期数
      if up ==golad_number:
             choushu = i # 记录抽数
             break # 出金完毕，跳出循环
      count = count+1 # 保底抽数加1
      if count==80: # 80抽必出金
         gold = gold +1 # 出货，加1个金
         if bichu == True: # 大保底，加1个up金
            up = up+1
            bichu = False # 出货后，大小保底失效
            golddict[i] = "大保底"
            count = 0 # 保底抽数归零
            continue # 跳出本次循环，开始下一轮        
         elif bichu == False: # 小保底，50%概率出up
               j = random.random()   # 随机生成[0.0,1.0) 之间的数字
               if j<=0.75:
                  up = up+1
                  golddict[i] = "小保底up金"
                  count = 0 # 保底抽数归零
                  continue # 跳出本次循环，开始下一轮     
               else:
                  changzhu = changzhu+1 # 出货后，常驻出金加1个
                  bichu = True # 出货后，大保底生效
                  golddict[i] = "常驻"
                  count = 0 # 保底抽数归零                  
                  continue # 跳出本次循环，开始下一轮
            
      chuhuolv = random.randint(1,1000) # 随机生成1-1000之间的数字,包含1和1000(这个版本不计算软概率提升情况)
      if chuhuolv<=6 : # 1-6点，出金1个,概率为0.6%      
         gold = gold+1 # 出货，加1个金
         if bichu == True: # 大保底，加1个up金
            up = up+1
            bichu = False # 出货后，大小保底失效
            golddict[i] = "大保底"
            count = 0 # 保底抽数归零

         elif bichu == False: # 小保底，50%概率出up
               j = random.random()   # 随机生成[0.0,1.0) 之间的数字
               if j<=0.75:
                  up = up+1
                  golddict[i] = "小保底up金"
                  count = 0 # 保底抽数归零     
               else:
                  changzhu = changzhu+1 # 出货后，常驻出金加1个
                  bichu = True # 出货后，大保底生效
                  golddict[i] = "常驻"
                  count = 0 # 保底抽数归零        
    return choushu;

def deal_array(arr):      
    # 处理数组，去除重复元素，并排序
    arr = np.unique(arr)
    unique, counts = np.unique(arr, return_counts=True)
    min = np.min(arr)
    max = np.max(arr)
    p1 = np.sum((arr>=0)&(arr<=200))/len(arr) *100
    p2 = np.sum((arr>=201)&(arr<=400))/len(arr)*100
    p3 = np.sum((arr>=401)&(arr<=600))/len(arr)*100
    p4 = np.sum((arr>=601)&(arr<=800))/len(arr)*100
    p5 = np.sum((arr>=801)&(arr<=1000))/len(arr)*100
    p6 = np.sum(arr>=1001)/len(arr)*100
    print("出货概率：")
    print("0-200："+"%.2f"%p1+"%")
    print(f"201-400："+"%.2f"%p2+"%")
    print(f"401-600："+"%.2f"%p3+"%")
    print(f"601-800："+"%.2f"%p4+"%")
    print(f"801-1000："+"%.2f"%p5+"%")
    print(f"1001以上："+"%.2f"%p6+"%")
   #  print("平均值"+str(np.average(arr)))
    print("最小值"+str(np.amin(arr)))
    print("最大值"+str(np.amax(arr)))
    print("中位数"+str(np.median(arr)))
   #  print("标准差"+str(np.std(arr))) 
    
    return;


def main():
    arr = np.array([])
    number = 10000; # 定义抽取次数
    print("开始测试，共抽取"+str(number)+"次")
    for i in range(1,number):
      a = test1(7)
      b = test2(1)
      c = a+b
      arr = np.append(arr,c)     
    deal_array(arr)
    # 计算每个元素出现的频率
   #  unique, counts = np.unique(arr, return_counts=True)
   #  frequencies = dict(zip(unique, counts))
   #  # 绘制分布图
   #  plt.bar([i for i in frequencies.keys()], [i for i in frequencies.values()])
   #  plt.title('Element Frequency')
   #  plt.xlabel('Element')
   #  plt.ylabel('Frequency')
   #  plt.show()
if __name__ == '__main__':
    main()
    