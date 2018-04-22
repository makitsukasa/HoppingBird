import random as rand
import numpy as np

def main():
	FIRST_1_CHANCE = 0.2
	GENE_NUM = 10
	INDIVISUAL_NUM = 10
	GENERATION_NUM = 10

	MUTATION_CHANCE = 0.02

	"""
	deme = []
	for i in range(INDIVISUAL_NUM):
		deme.append([])
		for g in range(GENE_NUM):
			deme[i].append(1 if rand.random() < FIRST_1_CHANCE else 0)
	"""
	deme = [[1 if rand.random() < FIRST_1_CHANCE else 0 for g in range(GENE_NUM)]
			for i in range(INDIVISUAL_NUM)]

	deme.sort(key = lambda x : sum(x), reverse = True)


	print("0 th generation")
	for i in range(INDIVISUAL_NUM):
		for g in range(GENE_NUM):
			print(deme[i][g], end = "")
		print(" (", sum(deme[i]), ")")
	print()

	for generation in range(GENERATION_NUM):
		new_deme = []

		# step 1  choose 2 parents
		parents = deme[:2:]
		for i in range(2):
			new_deme.append(parents[i])

		# step 2  generate 8 children
		for i in range(INDIVISUAL_NUM - 2):
			new_indivisual = []
			for g in range(GENE_NUM):
				# step 2-1  crossover
				new_gene = parents[0][g] if rand.random() < 0.5 else parents[1][g]		
				# step 2-2  mutation
				if rand.random() < MUTATION_CHANCE:
					new_gene = 1 - new_gene 

				new_indivisual.append(new_gene)

			new_deme.append(new_indivisual)

		# step 3  evaluate
		new_deme.sort(key = lambda x : sum(x), reverse = True)

		# step 4  update
		deme = new_deme[::]
		
		# (step 5  print)
		print(generation + 1, "th generation")
		for i in range(INDIVISUAL_NUM):
			for g in range(GENE_NUM):
				print(deme[i][g], end = "")
			print(" (", sum(deme[i]), ")")
		print()


if __name__ == '__main__':
	main()