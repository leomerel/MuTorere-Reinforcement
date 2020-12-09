class Case :

	def __init__(self,id,color):
		self.id = id
		self.color = color

if __name__ == '__main__':

	totalList = []

	colorList = ['o','b','w']

	#case 1
	for a in colorList:
		#case 2
		for b in colorList :
			#case 3
			for c in colorList :
				#case 4
				for d in colorList :
					#case 5
						for e in colorList:
							#case 6
							for f in colorList :
								#case 7
								for g in colorList :
									#case 8
									for h in colorList :
										#case 9
										for i in colorList :

											countList = [a,b,c,d,e,f,g,h,i]

											if countList.count('o') != 1 :
												continue

											if countList.count('b') != 4 :
												continue

											if countList.count('w') != 4 :
												continue

											totalList.append([[Case(7,g),Case(8,h),Case(9,i)],[Case(4,d),Case(5,e),Case(6,f)],[Case(1,a),Case(2,b),Case(3,c)]])
