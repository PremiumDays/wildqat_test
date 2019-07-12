import numpy as np
import wildqat as wq
import matplotlib.pyplot as plt

a = wq.opt()
#a.qubo = [[0,1,-2],[0,0,-2],[0,0,3]] #ここでqubo入れる
N = 4  #行の設定
M = 10 #列の設定
#行列Jを設定
J = np.zeros((N, M, N, M), dtype = np.float32)
#定数の定義
A = 10 #ペナルティの値
B = 3 #できれば超えてほしくない値

#クロネッカーデルタを定義
def delta(i, j):
    if(i == j):
        return 1
    else:
        return 0

#ルール1:講師A, Bは同時に存在できない
for i1 in range(N):
    J[i1, 0, i1, 1] +=  A

#ルール2:ブースLに太郎と次郎は同時に存在できない
for i1 in range(N):
    J[i1, 2, i1, 4] +=  A

#ルール3:ブースRに太郎と次郎は同時に存在できない
for i1 in range(N):
    J[i1, 3, i1, 5] +=  A
	
#ルール4:ブースLとRをを太郎は同一時間に占有できない	
for i1 in range(N):
    J[i1, 2, i1, 3] +=  A	

#ルール5:ブースLとRをを次郎は同一時間に占有できない	
for i1 in range(N):
    J[i1, 4, i1, 5] +=  A
	
#ルール6:生徒がいるときは必ず講師がいる。3体問題に置き換えて解いていく
## x_j=6 :x_j=0とx_j=1(講師Aと講師B)のOR関数
for i1 in range(N):
    J[i1, 0, i1, 0] += A
    J[i1, 1, i1, 1] += A
    J[i1, 6, i1, 6] += A
    J[i1, 0, i1, 1] += A
    J[i1, 0, i1, 6] -= 2 * A
    J[i1, 1, i1, 6] -= 2 * A    

for i1 in range(N):
## x_j=7 :x_j=2とx_j=4(ブースL)のOR関数
    J[i1, 2, i1, 2] += A
    J[i1, 4, i1, 4] += A
    J[i1, 7, i1, 7] += A
    J[i1, 2, i1, 4] += A
    J[i1, 2, i1, 7] -= 2 * A
    J[i1, 4, i1, 7] -= 2 * A  	
## x_j=8 :x_j=3とx_j=5(ブースR)のOR関数
    J[i1, 3, i1, 3] += A
    J[i1, 5, i1, 5] += A
    J[i1, 8, i1, 8] += A
    J[i1, 3, i1, 5] += A
    J[i1, 3, i1, 8] -= 2 * A
    J[i1, 5, i1, 8] -= 2 * A  	
## x_j=9 :x_j=7とx_j=8(ブースLとブースR)のOR関数
    J[i1, 7, i1, 7] += A
    J[i1, 8, i1, 8] += A
    J[i1, 9, i1, 9] += A
    J[i1, 7, i1, 8] += A
    J[i1, 7, i1, 9] -= 2 * A
    J[i1, 8, i1, 9] -= 2 * A  	

## 講師と生徒が一方だけいる場合はNG。両方いるか、両方いないときのみOKの関数
## つまり(x_6-x_9)^2 の値が正(1）になるとペナルティ
for i1 in range(N):
    J[i1, 6, i1, 6] += A
    J[i1, 6, i1, 9] -= 2 * A
    J[i1, 9, i1, 9] += A  
							
#ルール7;太郎は3コマの授業をとる(J=2, 3)。
for i1 in range(N):
    for j1 in range(2,4):
        for i2 in range(N):
            for j2 in range(2,4):
                J[i1, j1, i2, j2] -= 5 * A * delta(i1, i2) * delta(j1, j2) 
                if i1 < i2 or j1 < j2:
                    J[i1, j1, i2, j2] += 2 * A

#ルール8;次郎は2コマの授業をとる(J=4, 5)。
for i1 in range(N):
    for j1 in range(4,6):
        for i2 in range(N):
            for j2 in range(4,6):
                J[i1, j1, i2, j2] -= 3 * A * delta(i1, i2) * delta(j1, j2) 
                if i1 < i2 or j1 < j2:
                    J[i1, j1, i2, j2] += 2 * A

	
#ルール2:講師の出勤にはコストがかかる
for i1 in range(N):
    for j1 in range(2):
        for i2 in range(N):
            for j2 in range(2):
                J[i1, j1, i2, j2] += B * delta(i1, i2) * delta(j1, j2)
				
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
#plt.plot(a.E)
#plt.show()