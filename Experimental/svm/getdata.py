tweets=[]
tags=[]
tag_names=['trump_positive','trump_negative','hillary_positive','hillary_negative','bernie_positive','bernie_negative','cruz_positive','cruz_negative','republican_positive','republican_negative','democrat_positive','democrat_negative','neutral']
with open("../python/annotated2/annotated.csv.sortedaf") as f:
    for line in f:
        parta=line.split(",")
        tweets.append(parta[12])
        if parta[6]=="1":
            tags.append(2) #hillary_positive
        elif parta[6]=="-1":
            tags.append(3) #hillary_negative
        elif parta[7] == "1":
            tags.append(4) #bernie_positive
        elif parta[7] == "-1":
            tags.append(5) #bernie_negative
        elif parta[8] == "1":
            tags.append(0) #trump_positive
        elif parta[8] == "-1":
            tags.append(1) #trump_negative
        elif parta[9] == "1":
            tags.append(6) #cruz_positive
        elif parta[9] == "-1":
            tags.append(7) #cruz_negative
        elif parta[10] == "1":
            tags.append(8)  #republican_positive
        elif parta[10] == "-1":
            tags.append(9)  #republican_negative
        elif parta[11] == "1":
            tags.append(10)  #democrat_positive
        elif parta[11] == "-1":
            tags.append(11)  #democrat_negative
        else:
            tags.append(12)
print(set(tags))

