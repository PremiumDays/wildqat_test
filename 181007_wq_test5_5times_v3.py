import numpy as np
import wildqat as wq
import matplotlib.pyplot as plt

a = wq.opt()

Days = 1 #講習の日程数 2日から1日に減らした(180924)
Booth = 3 #教室のブース数
Time = 5 #一日当たりのコマ数

Mt = 2 #講師の数

#########################################
#太郎　E 1科目
#花子　M 1科目
#次郎　E, M 2科目
#########################################
Ms= 1 + 1 + 2 

#行列の数
N = Days * Booth * Time   #縦のほう。時間の概念。
M = Mt + 2 * Ms + 4  #1:2の役割を生徒に持たせる #左、右、生徒、講師のcellを追加してみる。9/24


#定数の定義
A = 10 #絶対に超えてほしくない値
E = 0 #これなんやったっけ
B = 5 #できれば超えてほしくない値
C = 0 #生徒と講師の関連づけのところの定数
D = 0
#クロネッカーデルタを定義
def delta(i, j):
    if(i == j):
        return 1
    else:
        return 0
#行列Jを計算
J = np.zeros((N, M, N, M), dtype = np.int8) #np.float64がもともと

#ルール0 講師、生徒のスケジュールの導入（h, 自己相関相互作用の項）　生徒、講師がダメなところに1が入るとペナルティ。
## 一旦スケジュールに関しては考慮しないことにする。つまり、生徒も講師もどこに入ってもよい。
#import xlrd
#book = xlrd.open_workbook('180716時間割example_5times_v1.xlsx')
#sheet1 = book.sheet_by_index(0)

#h = np.zeros((N,M), dtype = np.int8)

#for j in range(M):
#    for i in range(N):
#	    h[i,j] += sheet1.cell(i+2,j+3).value

#for j1 in range(M):
#    for i1 in range(N):
#        J[i1, j1, i1, j1] += A * h[i1,j1]

####ルール0はここまで####
		
#ルール0.1 同じコマ、別ブースに同じ講師が存在してはならない OK!180923
for j1 in range(Mt):
    for i1 in range(Days * Time):
        J[i1*Booth + 0, j1, i1*Booth + 1, j1] += A
        J[i1*Booth + 0, j1, i1*Booth + 2, j1] += A
        J[i1*Booth + 1, j1, i1*Booth + 2, j1] += A

#ルール0.1 同じコマ、別ブースに太郎が存在してはならない。科目が別でもダメ。 OK!180923
for i3 in range(Days * Time):
    for i1 in range(i3*3+0,i3*3+3):
        for j1 in range(2,4):
            for i2 in range(i3*3+0,i3*3+3):
                for j2 in range(2,4):
                    if i1 < i2:
                        J[i1, j1, i2, j2] += A
                    elif i1 == i2 and j1 < j2:
                        J[i1, j1, i2, j2] += A

#ルール0.1 同じコマ、別ブースに花子が存在してはならない。科目が別でもダメ。 OK!180923					
for i3 in range(Days * Time):
    for i1 in range(i3*3+0,i3*3+3):
        for j1 in range(4,6):
            for i2 in range(i3*3+0,i3*3+3):
                for j2 in range(4,6):
                    if i1 < i2:
                        J[i1, j1, i2, j2] += A
                    elif i1 == i2 and j1 < j2:
                        J[i1, j1, i2, j2] += A
					
#ルール0.1 同じコマ、別ブースに次郎が存在してはならない。科目が別でもダメ。 OK!180923
for i3 in range(Days * Time):
    for i1 in range(i3*3+0,i3*3+3):
        for j1 in range(6,10):
            for i2 in range(i3*3+0,i3*3+3):
                for j2 in range(6,10):
                    if i1 < i2:
                        J[i1, j1, i2, j2] += A
                    elif i1 == i2 and j1 < j2:
                        J[i1, j1, i2, j2] += A
					
#ルール1:講師がかぶるとペナルティ OK!180923
for i1 in range(N):
    J[i1, 0, i1, 1] += A
				
#ルール2:講師の出勤にはコストがかかる
for i1 in range(N):
    for j1 in range(Mt):
        for i2 in range(N):
            for j2 in range(Mt):
                J[i1, j1, i2, j2] += B * delta(i1, i2) * delta(j1, j2)
				
#ルール3:各コマ、各ブースにおいて「左」コマに生徒がかぶってはいけない OK!180923 →ルール3.6とかぶせられるので省略
#for i1 in range(N):
#    for j1 in range(Ms-1): 
#        for j2 in range(j1+1, Ms):
#            J[i1,j1*2+2,i1,j2*2+2]+=A

#ルール3.5:各コマ、各ブースにおいて「右」コマに生徒がかぶってはいけない OK!180923　→ルール3.7とかぶせられるので省略
#for i1 in range(N):
#    for j1 in range(Ms-1):
#        for j2 in range(j1+1, Ms):
#           J[i1, j1*2+3, i1, j2*2+3] += A
		   
#ルール3.6:左のコマに誰かがいると [Mt + 2 * Ms]番目のcellが1、だれもいないと0になる。なお、左コマに二人以上いてもペナルティとなる。 OK!180924
for i1 in range(N):
    for j1 in range(Mt, Mt+2*Ms+1, 2):
        for j2 in range(j1, Mt+2*Ms+1, 2):
           J[i1, j1, i1, j2] += A * delta(j1, j2)	

for i1 in range(N):
    for j1 in range(Mt, Mt+2*Ms-1, 2):
        for j2 in range(j1, Mt+2*Ms-1, 2):
            if j1 < j2:
                J[i1, j1, i1, j2] += 2 * A

for i1 in range(N):
    for j1 in range(Mt, Mt+2*Ms-1, 2):
        J[i1, j1, i1, Mt+2*Ms] -= 2 * A

#ルール3.6:右のコマに誰かがいると [Mt + 2 * Ms + 1]番目のcellが1、だれもいないと0になる。なお、右コマに二人以上いてもペナルティとなる。 OK!180924
for i1 in range(N):
    for j1 in range(Mt+1, Mt+2*Ms+2, 2):
        for j2 in range(j1, Mt+2*Ms+2, 2):
           J[i1, j1, i1, j2] += A * delta(j1, j2)	

for i1 in range(N):
    for j1 in range(Mt+1, Mt+2*Ms, 2):
        for j2 in range(j1, Mt+2*Ms, 2):
            if j1 < j2:
                J[i1, j1, i1, j2] += 2 * A

for i1 in range(N):
    for j1 in range(Mt+1, Mt+2*Ms, 2):
        J[i1, j1, i1, Mt+2*Ms+1] -= 2 * A

#ブースL[Mt + 2 * Ms]とR[Mt + 2 * Ms+1]のOR関数 OK!180924
for i1 in range(N):		
    J[i1, Mt + 2 * Ms, i1, Mt + 2 * Ms] += A
    J[i1, Mt + 2 * Ms+1, i1, Mt + 2 * Ms+1] += A
    J[i1, Mt + 2 * Ms+2, i1, Mt + 2 * Ms+2] += A
    J[i1, Mt + 2 * Ms, i1, Mt + 2 * Ms+1] += A
    J[i1, Mt + 2 * Ms, i1, Mt + 2 * Ms+2] -= 2 * A
    J[i1, Mt + 2 * Ms+1, i1, Mt + 2 * Ms+2] -= 2 * A  	

# (講師Aと講師B)のOR関数 OK!180924
for i1 in range(N):		
    J[i1, 0, i1, 0] += A
    J[i1, 1, i1, 1] += A
    J[i1, Mt + 2 * Ms+3, i1, Mt + 2 * Ms+3] += A
    J[i1, 0, i1, 1] += A
    J[i1, 0, i1, Mt + 2 * Ms+3] -= 2 * A
    J[i1, 1, i1, Mt + 2 * Ms+3] -= 2 * A 
	
## 講師と生徒が一方だけいる場合はNG。両方いるか、両方いないときのみOKの関数 OK!180924
for i1 in range(N):
    J[i1, Mt + 2 * Ms+2, i1, Mt + 2 * Ms+2] += A
    J[i1, Mt + 2 * Ms+2, i1, Mt + 2 * Ms+3] -= 2 * A
    J[i1, Mt + 2 * Ms+3, i1, Mt + 2 * Ms+3] += A  	
				
#ルール4.1;太郎は3コマのEをとる(J=2, 3)。 OK!180924
for i1 in range(N):
    for j1 in range(2,4):
        for i2 in range(N):
            for j2 in range(2,4):
                J[i1, j1, i2, j2] -= 5 * A * delta(i1, i2) * delta(j1, j2)	
                if i1 < i2:
                    J[i1, j1, i2, j2] += 2 * A
                elif i1 == i2 and j1 < j2:
                    J[i1, j1, i2, j2] += 2 * A
				
#ルール4.2;花子は2コマのMをとる(J=4, 5)。 OK!180924
for i1 in range(N):
    for j1 in range(4,6):
        for i2 in range(N):
            for j2 in range(4,6):
                J[i1, j1, i2, j2] -= 3 * A * delta(i1, i2) * delta(j1, j2)	
                if i1 < i2:
                    J[i1, j1, i2, j2] += 2 * A
                elif i1 == i2 and j1 < j2:
                    J[i1, j1, i2, j2] += 2 * A
				
#ルール4.3;次郎は2コマのEをとる(J=6, 7)。 OK!180924
for i1 in range(N):
    for j1 in range(6,8):
        for i2 in range(N):
            for j2 in range(6,8):
                J[i1, j1, i2, j2] -= 3 * A * delta(i1, i2) * delta(j1, j2)	
                if i1 < i2:
                    J[i1, j1, i2, j2] += 2 * A
                elif i1 == i2 and j1 < j2:
                    J[i1, j1, i2, j2] += 2 * A
			
#ルール4.4;次郎は2コマのMをとる(J=8, 9)。 OK!180924
for i1 in range(N):
    for j1 in range(8,10):
        for i2 in range(N):
            for j2 in range(8,10):
                J[i1, j1, i2, j2] -= 3 * A * delta(i1, i2) * delta(j1, j2)	
                if i1 < i2:
                    J[i1, j1, i2, j2] += 2 * A
                elif i1 == i2 and j1 < j2:
                    J[i1, j1, i2, j2] += 2 * A				

#ルール8:「右」コマに生徒がはいるためには、「左」が埋まっていないといけない。「左」に生徒が入るときには、講師がいないといけない。
#for i1 in range(N):
#    for j1 in range(M):
#        J[i1, j1, i1, j1] +=  A
#    for j1 in range(Mt):
#        for j2 in range(Mt, M, 2):
#            J[i1, j1, i1, j2] -= 2 * A
#    for j1 in range(Mt, M ,2):
#        for j2 in range(Mt+1, M+1, 2):
#            J[i1, j1, i1, j2] -= A
			
#ルール8:講師-生徒相互作用。講師は、生徒が入っていないところでも入ってよいバージョン。
#for i1 in range(N):
#    for j1 in range(2, M):
#        J[i1, j1, i1, j1] +=  C
#    for j1 in range(Mt):
#        for j2 in range(2, 16, 2):
#            J[i1, j1, i1, j2] -= C
#    for j1 in range(Mt):
#        for j2 in range(3, 17, 2):
#            J[i1, j1, i1, j2] -= C		

#ルール9: 講師のコマが1→0、0→1になるときにペナルティが生じる
#for j1 in range(Mt):
#    for id in range(Days):
#        for it in range(Time-1):
#            for i1 in range(3):
#                J[id*Time*Booth + it * 3 + i1 , j1, id*Time*Booth + it * 3 + i1, j1] += B
#                J[id*Time*Booth + it * 3 + i1+3 , j1, id*Time*Booth + it * 3 + i1+3, j1] += B
#                for i2 in range(3, 6):
#                    J[id*Time*Booth + it * 3 + i1 , j1, id*Time*Booth + it * 3 + i2, j1] -= 2 * B	
			
#Qの計算
a.qubo = np.empty((N*M,N*M), dtype = np.float32)
x = 0
for i1 in range(N):
    for j1 in range(M):
        y = 0
        for i2 in range(N):
            for j2 in range(M):
                a.qubo[x,y] = J[i1,j1,i2,j2]
                y = y + 1
        x = x + 1
print(a.qubo)
path_w = 'MinEnergy.txt'
with open(path_w, mode='w') as f:
    f.write(str(10))
	
for loop in range(30):
    Z=a.sa()
    result = np.empty((N, M), dtype = np.int)
    i = 0
    for x in range(N):
        for y in range(M):
            if(Z[i] == 1):
                result[x, y] = 1
            else:
                result[x, y] = 0
            i += 1
    print(result)
    print(a.E[-1])
    path = 'MinEnergy.txt'
    with open(path) as f:
        SoFarMinE = f.read()
    SoFarMinE=float(SoFarMinE)
    if SoFarMinE > a.E[-1] :
        path_w = 'MinEnergy.txt'
        with open(path_w, mode='w') as f:
            f.write(str(a.E[-1]))
        np.savetxt('outputbit.csv',result,delimiter=',')

#np.savetxt('out_schedule_v1.csv',result,delimiter=',')
#plt.plot(a.E)
#plt.show()