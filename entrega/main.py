import sys
import random
from copy import deepcopy
import tree
from half import half_and_half, tree_val, fitness, new_gene, random_node, evolution_cycle
from math import sqrt, log
import pandas as pd
from functools import reduce
from matplotlib import pyplot as plt, rcParams, ticker, colors, colorbar

# Individual related entries, population size and max tree depth
pop_size = sys.argv[1]
max_depth = sys.argv[2]

# Crossing and mutation chances
cross_chance = sys.argv[3]
mut_chance = sys.argv[4]

# Tamanho do subconjunto do torneio
k_tournament = sys.argv[5]
# Generation limits
max_gen = sys.argv[6]

# Elitism used
elite = sys.argv[7]

# Caminho do arquivo de entrada, train
path = sys.argv[8]

# Caminho do arquivo de entrada, teste
path_teste = sys.argv[9]

# O que esta sendo variado
alter = sys.argv[10]

# O caso usado, premiliminar(20) ou final
case = sys.argv[11]

if(case == '20'):
	premiliminar = True # Determinar se e o teste final ou nao
else:
	premiliminar = False # Determinar se e o teste final ou nao

df = pd.read_csv(path, header=None)
cols = df.columns # Gets number of dataframe columns
x_vals=[] # (X...Xn) values (list of lists)
y_saida=[]# Y values
x_nums = len(cols)-1 # Number of X Variables
for i in range(len(cols)-1):
	x_vals.append(df.iloc[:, i].tolist())

y_saida = df.iloc[:, len(cols)-1].tolist()

media_best = [] # Media fitness melhores individuos de cada teste
media_worse = []# Media fitness piores individuos de cada teste
media_filhos = []# Media num de filhos com fitness melhor que a media da fitness dos pais
media_repeats = []# Media num de individuos iguais
desvio_best = [] # Desvio padrao fitness melhores individuos de cada teste
desvio_worse = []# Desvio padrao fitness piores individuos de cada teste
desvio_filhos = []# Desvio padrao num de filhos com fitness melhor que a media da fitness dos pais
desvio_repeats = []# Desvio padrao num de individuos iguais
seeds = [0,8,16]
if(case == '20'):
	num_t = 20
else:
	num_t = 3
for i in range(0, num_t):
	if(case == '20'):
		random.seed(i)
	else:
		random.seed(seeds[i])
	old_gen = half_and_half(int(pop_size),int(max_depth), x_nums)
	# Initial gen fitness
	for t in old_gen:
	    t.fit = (fitness(x_vals, y_saida, t))

	# Roda para o Train
	last_gen = evolution_cycle(old_gen, max_gen, pop_size, k_tournament,
	                           mut_chance, cross_chance, elite, x_nums, x_vals, y_saida)

	df = pd.read_csv(path_teste, header=None)
	cols = df.columns # Gets number of dataframe columns
	x_vals=[] # (X...Xn) values (list of lists)
	y_saida=[]# Y values
	x_nums = len(cols)-1 # Number of X Variables
	for j in range(len(cols)-1):
		x_vals.append(df.iloc[:, j].tolist())

		y_saida = df.iloc[:, len(cols)-1].tolist()

	# Roda com os melhores de cada geracao da execucao anterior(do train)
	#print('teste = ', i)
	final = evolution_cycle(last_gen[1], max_gen, pop_size, k_tournament,
							mut_chance, cross_chance, elite, x_nums, x_vals, y_saida)
	if(premiliminar == False):

		final_one = [x.fit for x in final[1]]
		final_two = [x.fit for x in final[2]]

		media_best.append(final_one)
		media_worse.append(final_two)
		media_filhos.append(final[3])
		media_repeats.append(final[4])

	elif(premiliminar == True):
		mb = 0
		for n in final[1]:
			mb = mb + n.fit
		mb = mb/len(final[1])
		media_best.append(mb)
		#print(media_best)
		db = 0
		for n in final[1]:
			db = db + ((n.fit - media_best[i])**2)/len(final[1])
		#print(db)
		desvio_best.append(sqrt(db))

		mw = 0
		for n in final[2]:
			mw = mw + n.fit
		mw = mw/len(final[1])
		media_worse.append(mw)
		dw = 0
		for n in final[2]:
			dw = dw + ((n.fit - media_worse[i])**2)/len(final[2])
		desvio_worse.append(sqrt(dw))

		mf = 0
		for n in final[3]:
			mf = mf + n
		mf = mf/len(final[1])
		media_filhos.append(reduce(lambda x, y: x + y, final[3])/ len(final[3]))
		d_f = 0
		for n in final[3]:
			d_f = d_f + ((n - media_filhos[i])**2)/len(final[3])
		desvio_filhos.append(sqrt(d_f))

		mr = 0
		for n in final[4]:
			mr = mr + n
		mr = mr/len(final[4])
		media_repeats.append(mr)
		dr = 0
		for n in final[4]:
			dr = dr + ((n - media_repeats[i])**2)/len(final[4])
		desvio_repeats.append(sqrt(dr))

tests = []
if(premiliminar == False):
	for i in range(int(max_gen)):
		tests.append(i)

elif(premiliminar == True):
	for i in range(int(case)):
		tests.append(i)


if(premiliminar == False):
	rcParams['figure.figsize'] = (18,15)
	fig, (ax, ax2, ax3, ax4) = plt.subplots(4, 2)
	ax = plt.subplot2grid((2, 2), (0, 0))
	ax2 = plt.subplot2grid((2, 2), (0, 1))
	ax3 = plt.subplot2grid((2, 2), (1, 0))
	ax4 = plt.subplot2grid((2, 2), (1, 1))

################################plos bests######################################
	N = ax.plot(tests, media_best[0], color='red', marker='o')
	N = ax.plot(tests, media_best[1], color='green', marker='*')
	N = ax.plot(tests, media_best[2], color='blue', marker='^')

	ax.set_title('Melhores Indivíduos nos 3 melhores testes',size=12)
	ax.set_ylabel('Fitness', size=12)
	ax.set_xlabel("Geração", size=12)

	ax.grid(linestyle='--', linewidth=0.5)
	major_ticks = tests
	ax.set_xticks(major_ticks)

	for item in ax.get_xticklabels():
	    item.set_rotation(90)

################################plos worse######################################
	N = ax2.plot(tests, media_worse[0], color='red', marker='o')
	N = ax2.plot(tests, media_worse[1], color='green', marker='*')
	N = ax2.plot(tests, media_worse[2], color='blue', marker='^')

	ax2.set_title('Piores Indivíduos nos 3 melhores testes',size=12)
	ax2.set_ylabel('Fitness', size=12)
	ax2.set_xlabel("Geração", size=12)

	ax2.grid(linestyle='--', linewidth=0.5)
	major_ticks = tests
	ax2.set_xticks(major_ticks)

	for item in ax2.get_xticklabels():
	    item.set_rotation(90)

################################plos filhos######################################
	N = ax3.plot(tests, media_filhos[0], color='red', marker='o')
	N = ax3.plot(tests, media_filhos[1], color='green', marker='*')
	N = ax3.plot(tests, media_filhos[2], color='blue', marker='^')

	ax3.set_title('Filhos com fitness melhor que a média dos pains, nos 3 melhores testes',size=12)
	ax3.set_ylabel('Num. de filhos', size=12)
	ax3.set_xlabel("Geração", size=12)

	ax3.grid(linestyle='--', linewidth=0.5)
	major_ticks = tests
	ax3.set_xticks(major_ticks)

	for item in ax3.get_xticklabels():
	    item.set_rotation(90)

################################plos filhos######################################
	N = ax4.plot(tests, media_repeats[0], color='red', marker='o')
	N = ax4.plot(tests, media_repeats[1], color='green', marker='*')
	N = ax4.plot(tests, media_repeats[2], color='blue', marker='^')

	ax4.set_title('Individuos repetidos, nos 3 melhores testes',size=12)
	ax4.set_ylabel('Num. de Individuos', size=12)
	ax4.set_xlabel("Geração", size=12)

	ax4.grid(linestyle='--', linewidth=0.5)
	major_ticks = tests
	ax4.set_xticks(major_ticks)

	for item in ax4.get_xticklabels():
	    item.set_rotation(90)


elif(premiliminar == True):
	rcParams['figure.figsize'] = (18,30)
	fig, (ax, ax2, ax3, ax4, ax5, ax6, ax7, ax8) = plt.subplots(8, 2)
	ax = plt.subplot2grid((4, 2), (0, 0))
	ax2 = plt.subplot2grid((4, 2), (0, 1))
	ax3 = plt.subplot2grid((4, 2), (1, 0))
	ax4 = plt.subplot2grid((4, 2), (1, 1))
	ax5 = plt.subplot2grid((4, 2), (2, 0))
	ax6 = plt.subplot2grid((4, 2), (2, 1))
	ax7 = plt.subplot2grid((4, 2), (3, 0))
	ax8 = plt.subplot2grid((4, 2), (3, 1))

	fig.suptitle('Alterando'+alter, size=15)

	#################################Plot Best######################################
	N = ax.plot(tests, media_best, color='red', marker='o')

	ax.set_title('Media dos Melhores Individuos',size=12)
	ax.set_ylabel('Media Fitness', size=12)
	ax.set_xlabel("Teste", size=12)

	ax.grid(linestyle='--', linewidth=0.5)
	major_ticks = tests
	ax.set_xticks(major_ticks)

	for item in ax.get_xticklabels():
	    item.set_rotation(90)

	N = ax2.plot(tests, desvio_best, color='red', marker='o')

	ax2.set_title('Desvio Padrao dos Melhores Individuos',size=12)
	ax2.set_ylabel('Desvio Padrao Fitness', size=12)
	ax2.set_xlabel("Teste", size=12)

	ax2.grid(linestyle='--', linewidth=0.5)
	major_ticks = tests
	ax2.set_xticks(major_ticks)

	for item in ax2.get_xticklabels():
	    item.set_rotation(90)
	######################################Plot worse###############################
	N = ax3.plot(tests, media_worse, color='green', marker='o')

	ax3.set_title('Media dos Piores Individuos',size=12)
	ax3.set_ylabel('Media Fitness', size=12)
	ax3.set_xlabel("Teste", size=12)

	ax3.grid(linestyle='--', linewidth=0.5)
	major_ticks = tests
	ax3.set_xticks(major_ticks)

	for item in ax3.get_xticklabels():
	    item.set_rotation(90)

	N = ax4.plot(tests, desvio_worse, color='green', marker='o')

	ax4.set_title('Desvio Padrao dos Piores Individuos',size=12)
	ax4.set_ylabel('Desvio Padrao Fitness', size=12)
	ax4.set_xlabel("Teste", size=12)

	ax4.grid(linestyle='--', linewidth=0.5)
	major_ticks = tests
	ax4.set_xticks(major_ticks)

	for item in ax4.get_xticklabels():
	    item.set_rotation(90)
	#####################################Plot Filhos###############################
	N = ax5.plot(tests, media_filhos, color='blue', marker='o')

	ax5.set_title('Media do Numero de Filhos com fitness melhor que a media dos pais',size=12)
	ax5.set_ylabel('Media Num. Filhos', size=12)
	ax5.set_xlabel("Teste", size=12)

	ax5.grid(linestyle='--', linewidth=0.5)
	major_ticks = tests
	ax5.set_xticks(major_ticks)

	for item in ax5.get_xticklabels():
	    item.set_rotation(90)

	N = ax6.plot(tests, desvio_filhos, color='blue', marker='o')

	ax6.set_title('Desvio Padrao do Numero de Filhos com fitness melhor que a media dos pais',size=12)
	ax6.set_ylabel('Desvio Padrao Num. Filhos', size=12)
	ax6.set_xlabel("Teste", size=12)

	ax6.grid(linestyle='--', linewidth=0.5)
	major_ticks = tests
	ax6.set_xticks(major_ticks)

	for item in ax6.get_xticklabels():
	    item.set_rotation(90)
	####################################Plot Repeats################################
	N = ax7.plot(tests, media_repeats, color='black', marker='o')

	ax7.set_title('Media do Numero de individuos repetidos',size=12)
	ax7.set_ylabel('Num. Individuos', size=12)
	ax7.set_xlabel("Teste", size=12)

	ax7.grid(linestyle='--', linewidth=0.5)
	major_ticks = tests
	ax7.set_xticks(major_ticks)

	for item in ax7.get_xticklabels():
	    item.set_rotation(90)

	N = ax8.plot(tests, desvio_repeats, color='black', marker='o')

	ax8.set_title('Desvio Padrao do Numero de individuos repetidos',size=12)
	ax8.set_ylabel('Desvio Padrao Num. Individuos', size=12)
	ax8.set_xlabel("Teste", size=12)

	ax8.grid(linestyle='--', linewidth=0.5)
	major_ticks = tests
	ax8.set_xticks(major_ticks)

	for item in ax8.get_xticklabels():
	    item.set_rotation(90)


fig.savefig(alter, dpi=75)
