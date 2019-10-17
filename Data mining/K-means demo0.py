import numpy as np

x = np.linspace(0,99,100)
y = np.linspace(100,199,100)

k = 2
n = len(x)
# 1.选初始类中心
center0 = np.array([x[0],y[0]])
center1 = np.array([x[1],y[1]])

while True:
    # 2.求距离
    dis = np.zeros([n,k+1])#n行n列
    for i in range(n):
        dis[i, 0] = np.sqrt((x[i] - center0[0]) ** 2 + (y[i] - center0[1]) ** 2)
        dis[i, 1] = np.sqrt((x[i] - center1[0]) ** 2 + (y[i] - center1[1]) ** 2)
        dis[i, 2] = np.argmin(dis[i,:2]) # 3.归类
    # 4.求新类中心
    index0 = dis[:,2]==0
    index1 = dis[:,2]==1
    center0_new = np.array([x[index0].mean(),y[index0].mean()])
    center1_new = np.array([x[index1].mean(),y[index1].mean()])

    # 5.判定，类中心是否变化
    if all((center0 == center0_new)&(center1 == center1_new)):
        break
    center0 = center0_new
    center1 = center1_new
print(dis)