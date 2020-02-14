#!/usr/bin/env python
import rypto
import sys
import large_prime
import binascii



def main():
	N=402394248802762560784459411647796431108620322919897426002417858465984510150839043308712123310510922610690378085519407742502585978563438101321191019034005392771936629869360205383247721026151449660543966528254014636648532640397857580791648563954248342700568953634713286153354659774351731627683020456167612375777
	e1=3
	e2=0x10001

	c1=4020137574131575546540268502595841326627069047574502831387774931737219358054228401772587980633053000
	c2=170356929377044754324767086491413709789303946387160918939626824506821140429868670769571821346366209258416985269309515948776691067548265629489478628756185802183547222688698309731374342109385922509501909728895585636684978295199882599818258590851085977232207148101448845575681189389906429149193460620083999406237

	g,x,y = rypto.egcd(e1,e2) #Euclidean algorightm
	i = rypto.mulinv(c2,N) #multiplicative inverse of C2 because y is -1
	test = (rypto.mod_exp(c1,x,N)*rypto.mod_exp(i,-y,N))%N #plain = (c1^a) * (i^-b) %N

	
	answer = rypto.standard(hex(test)).decode("hex")
	print answer



if __name__ == "__main__":
	main()