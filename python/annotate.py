
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

hillaryPositive = ["hillary2016","imwithher","hillary","clinton2016", "hilaryclinton","hilary2016","billclinton"]
hillaryNegative = ["fuckhilary","notwithher"]
berniePositive = ["feelthebern", "stillsanders", "berniesanders2016", "berniesanders", "berniesandersforpresident", "voteforbernie","canadiansforbernie", "bernie2016", "bernie"]
bernieNegative = []
trumpPositive = ["donaldtrump","trump2016","trumptrain","trumprally","mrtrump","letsmakeamericagreatagain","presidenttrump","makeamericagreatagain","trumpforpresident","alwaystrump", "trump"]
trumpNegative = ["makeamericahateagain","drumpf","makedonalddrumpfagain","dumptrump","fucktrump","trumpisachump"]
cruzPositive = ["tedcruz", "cruz2016", "cruz","cruztovictory","cruzcrew"]
cruzNegative = []
gopNuetral = ["republicans","conservatives""republican","gop","republicanparty"]
demNuetral = ["democrats"]
nuetral = ["presidentialelection","demdebate","gopdebate","aipac2016","2016presidentialelection","presidentialelection2016"]

file_names = ["final_data.csv"]
out_file_name = "annotated.csv"

def getValue(tag, positiveTags, negativeTags):
    if tag in positiveTags:
        return "1"
    elif tag in negativeTags:
        return "-1"
    return "0"

fh = open(out_file_name, 'w')

for file_name in file_names:

    with open(file_name) as f:
        content = f.readlines()

    for line in content:
        parts = line.split(",")
        fh.write(parts[0] + "," + parts[1] + "," + parts[2] + "," + parts[3] + "," + parts[4] + "," + parts[5] + "," + getValue(parts[1], hillaryPositive, hillaryNegative) + "," + getValue(parts[1], berniePositive, bernieNegative) + "," + getValue(parts[1], trumpPositive, trumpNegative) + "," + getValue(parts[1], cruzPositive, cruzNegative) + "," + getValue(parts[1], gopNuetral, []) + "," + getValue(parts[1], demNuetral, []) + "," + parts[12])

fh.close