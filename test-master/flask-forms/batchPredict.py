import sys
import pandas as pd

print(sys.argv[1])
csv = sys.argv[1]

dataf = pd.read_csv(csv)

reviews = dataf.review.to




def getTopic(review):
	msg = []
	    x = nmf.transform(vectorizer.transform([review]))[0]
	    print(x, x.sum())
	    my_dict = {}
	    for index, item in enumerate(x):
	        my_dict[index] = x[index]
	    IssueMap={0: "Other issue", 1:"Other issue",2: "Camera Issue", 3: "Other Issue", 4: "Other Issue", 5: "OS / Software Issue", 6: "Other issue", 7: "Other issue", 8: "Other issue", 
	    9: "Other Issue", 10: "Physical Damage/Broken Issue", 11: 15,12: 10, 13: "Broken Issue", 14: 18, 15: 18, 16: "Payment Issue", 
	    17: "Button Issue", 18: "Battery Issue", 19: 21, 20: 8,21: "Audio Issue", 22: "Connectivity Issue", 
	    23: "Cursor/Tracking issue", 24: "Video Issue", 25: 24, 26: "Modify subscription/ Payment issue", 
	    27: "Wifi Internet Connectivity issue", 28: "Password/Reset issue", 29: "other"
	    }
	    a1_sorted_keys = sorted(my_dict, key=my_dict.get, reverse=True)
	    i = 1
	    for r in a1_sorted_keys:
	        if(i<3 and my_dict[r]>0.0):
	            #print(r, my_dict[r])
	            str = (IssueMap[r],round(my_dict[r]*100,2),"%")
	            msg.append(str)
	            i=i+1
	    return msg

